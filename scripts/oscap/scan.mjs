#!/usr/bin/env zx

import { assert, usage, errorHandler } from '../utilities/index.mjs';

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Oscap scan'))}
  Run an oscap scan on a remote machine.

${chalk.bold('Usage:')}
  ./scan.mjs [options]

${chalk.bold('Options:')}
  profile              profile to use
  --distro, -d         datastream distro to use <rhel8|rhel9|centos-8|cs9|fedora>
  --host=<host>        remote host [default: localvm]
  --port=<port>        remote port [default: 2222]
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

const profile = argv._[0];
const distro = argv.distro || argv.d;

assert(profile == undefined, USAGE_TEXT);
assert(distro == undefined, USAGE_TEXT);

const host = argv.host || 'localvm';
const port = argv.port || 2222;

/*-----------------------------------------------------------------------------
| Define constants
-----------------------------------------------------------------------------*/

const DATASTREAM_DIR = '/usr/share/xml/scap/ssg/content';

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const scan = async (flags, datastream, host, port) => {
  try {
    // prettier-ignore
    const res = await $`ssh -t -q ${host} -p ${port} sudo oscap xccdf eval ${flags} ${datastream}`.nothrow();
    console.log(res.exitCode);
    if (res.exitCode != 2 && res.exitCode != 0) throw res.stdout;
  } catch (error) {
    let e = error.split('\n').slice(-3).join('\n');
    console.log();
    errorHandler({ stderr: e });
  }
};

const main = async ({ host, port, ...args }) => {
  const datastreamPath = path.join(DATASTREAM_DIR, `ssg-${args.distro}-ds.xml`);

  const flags = ['--profile', args.profile];

  if (args.results) {
    flags.push('--results');
    flags.push(args.results);
  }

  if (args.report) {
    flags.push('--report');
    flags.push(args.report);
  }

  if (args.tailoring) {
    flags.push('--tailoring-file');
    flags.push(args.tailoring);
  }

  await scan(flags, datastreamPath, host, port);
};

await main({ ...argv, profile, distro, host, port });
