#!/usr/bin/env zx

import { info, assert, usage, toggleVerbosity } from '../utilities/index.mjs';

/*-----------------------------------------------------------------------------
| Parse args & exit early
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Start a vm'))}
  Run a local vm for development.

${chalk.bold('Usage:')}
  ./start.mjs [options]

${chalk.bold('Options:')}
  --distro, -d           distro to boot up <fedora|rhel|centos>
  --image, -i            use a local image to boot instead
  --arch=<arch>          architecture [default: x86_64]
  --help, -h             print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

const arch = argv.arch || 'x86_64';
const distro = argv.distro || argv.d;
const image = argv.image || argv.i;

assert((distro || image) === undefined, USAGE_TEXT); // either must be defined
assert((distro && image) !== undefined, USAGE_TEXT); // both cannot be defined

/*-----------------------------------------------------------------------------
| Process environment variables
-----------------------------------------------------------------------------*/

$.verbose = false;

process.env = {
  ...process.env,
  ...(await fs.readJson('./.env.json')),
};

const { SSH_KEY, OVERLAY_DIR, SCRATCH_DIR, XDG_RUNTIME_DIR } = process.env;

/*-----------------------------------------------------------------------------
| Define constants
-----------------------------------------------------------------------------*/

const DATA_DIR = path.join(XDG_RUNTIME_DIR, 'osbuild-vm', 'data');
const MAC_ADDRESS = 'FE:0B:6E:22:3D:00';

const PORTS = [
  { host: 2222, guest: 22 },
  { host: 8180, guest: 80 },
  { host: 8443, guest: 443 },
  { host: 9091, guest: 9090 },
];

const parsePorts = (image) => {
  if (image) return 'hostfwd=tcp::2223-:22';
  // prettier-ignore
  return PORTS.map(({ host, guest }) => {
    return `hostfwd=tcp::${host}-:${guest}`
  }).join(',');
};

const QEMU_ARGS = [
  '-m',
  '16G',
  '-smp',
  '8',
  '-netdev',
  `user,id=net0,net=10.0.2.0/24,${parsePorts(image)}`,
  '-device',
  `virtio-net-pci,netdev=net0,mac=${MAC_ADDRESS}`,
  '-nographic',
];

/*-----------------------------------------------------------------------------
| Helper functions
-----------------------------------------------------------------------------*/

const metadata = (distro) =>
  YAML.stringify({
    'instance-id': 'osbuild-vm',
    'local-hostname': `${distro}-vm`,
  });

const userdata = ({ yum_repos }) =>
  YAML.stringify({
    users: [
      {
        name: 'kingsley',
        gecos: 'GZ',
        ssh_authorized_keys: [SSH_KEY],
        ssh_pwauth: true,
        sudo: 'ALL=(ALL) NOPASSWD:ALL',
        groups: 'wheel',
      },
    ],
    chpasswd: {
      list: 'kingsley:password42\n',
      expire: false,
    },
    repo_update: true,
    repo_upgrade: 'all',
    manage_reolv_conf: true,
    resolv_conf: {
      nameservers: ['10.38.5.26', '10.0.2.3'],
    },
    run_cmd: [
      'git config --global user.email "testvm@osbuild.org"',
      'git config --global user.name "kingsley"',
    ],
    yum_repos,
  });

const getGuestImage = async (arch, distro) => {
  const images = await fs.readJson('./config/guest-images.json');
  const guest = images[arch][distro];
  assert(guest === undefined, 'Distro and arch are not supported');
  return path.join(SCRATCH_DIR, guest);
};

const waitforSSH = async (port) => {
  while (true) {
    try {
      await $`ssh -p ${port} localvm exit`.quiet();
      sleep(1000);
      break;
    } catch (e) {
      sleep(1000);
    }
  }
  await $`ssh -p ${port} localvm journalctl -fa`;
};

/*-----------------------------------------------------------------------------
| Overlay functions
-----------------------------------------------------------------------------*/

const loadRepos = async (distro) => {
  if (distro.includes('rhel8')) {
    return await fs.readJson('./config/rhel8-repos.json');
  }
  if (distro.includes('rhel9')) {
    return await fs.readJson('./config/rhel9-repos.json');
  }
  return {};
};

const getOverlay = async (image) => {
  const { name } = path.parse(image);
  const overlay = path.join(OVERLAY_DIR, `${name}.overlay.qcow2`);
  return {
    path: overlay,
    exists: await fs.pathExists(overlay),
  };
};

const makeOverlay = async (image, overlay) => {
  info('Making overlay');
  await $`qemu-img create -q -o backing_file=${image},backing_fmt=qcow2 -f qcow2 ${overlay}`;
  await $`qemu-img resize -q ${overlay} 100G`;
};

const makeUserData = async (distro) => {
  info('Making userdata');
  const { yum_repos } = await loadRepos(distro);
  await fs.writeFile(
    path.join(DATA_DIR, 'user-data'),
    `#cloud-config\n---\n${userdata({ yum_repos })}`
  );
};

const makeMetadata = async (distro) => {
  info('Making metadata');
  await fs.writeFile(
    path.join(DATA_DIR, 'meta-data'),
    `---\n${metadata(distro)}`
  );
};

const generateIso = async (distro) => {
  info('Generating iso');
  await $`mkdir -p ${DATA_DIR}`;
  const iso = path.join(DATA_DIR, 'composer-init.iso');
  await makeUserData(distro);
  await makeMetadata(distro);
  await $`mkisofs -input-charset utf-8 -output ${iso} -volid cidata -joliet -rock -quiet ${DATA_DIR}/user-data ${DATA_DIR}/meta-data`;
  return iso;
};

const getIso = async (image, overlay, distro) => {
  if (overlay.exists) return;
  await makeOverlay(image, overlay.path);
  return await generateIso(distro);
};

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const constructArgs = async (arch, overlay, iso) => {
  const arch_args = await fs.readJson('./config/arch-args.json');
  const iso_args = iso ? ['-drive', `file=${iso},format=raw`] : [];
  const qcow_args = ['-drive', `file=${overlay},format=qcow2`];
  return [...arch_args[arch], ...qcow_args, ...iso_args, ...QEMU_ARGS];
};

const getArgs = async (arch, distro, image) => {
  // simple image doesn't need iso
  if (image) return await constructArgs(arch, image, undefined);
  // get overlay and iso
  const guest = await getGuestImage(arch, distro);
  const overlay = await getOverlay(guest);
  const iso = await getIso(guest, overlay, distro);
  return await constructArgs(arch, overlay.path, iso);
};

const main = async (arch, distro, image) => {
  const params = await getArgs(arch, distro, image);
  const port = image ? 2223 : 2222;
  toggleVerbosity();
  $`qemu-system-x86_64 ${params}`.stdio('pipe');
  await waitforSSH(port);
};

await main(arch, distro, image);
