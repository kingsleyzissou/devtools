#!/usr/bin/env zx

import { assert, error, info, success, usage } from '../utilities/index.mjs';

/*-----------------------------------------------------------------------------
 | Installation scripts
 -----------------------------------------------------------------------------*/

import { osbuild } from './install/osbuild.mjs';
import { composer } from './install/composer.mjs';
import { blueprints } from './install/blueprints.mjs';

/*-----------------------------------------------------------------------------
 | Process environment variables
 ----------------------------------------------------------------------------*/

$.verbose = false;

const pwd = process.cwd();

const PROJECTS_DIR = 'projects';
const COMPONENTS = {
  composer: path.join(pwd, '..', 'osbuild-composer'),
  osbuild: path.join(pwd, '..', 'osbuild'),
  blueprints: path.join(pwd, 'blueprints', 'common'),
  fedora: path.join(pwd, 'blueprints', 'fedora'),
  rhel: path.join(pwd, 'blueprints', 'rhel'),
};

/*-----------------------------------------------------------------------------
 | Parse args & exit early
 -----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Update vm components'))}
  Install local versions of dev projects onto a vm.

${chalk.bold('Usage:')}
  ./update.mjs [options]

${chalk.bold('Options:')}
  --osbuild              sync and install osbuild
  --composer             sync and install composer
  --blueprints           sync and install blueprints
  --distro               distro specific blueprints <fedora|rhel>
  --host=<host>          remote host [default: localvm]
  --port=<port>          remote port [default: 2222]
  --help, -h             print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

const args = argv.composer || argv.osbuild || argv.blueprints;
assert(args === undefined, USAGE_TEXT);

/*-----------------------------------------------------------------------------
 | Helper functions
 -----------------------------------------------------------------------------*/

const sync = (src, dest, host) => {
  host = host || 'localvm';
  // prettier-ignore
  const excluded = ['--exclude', 'bin', '--exclude', 'build', '--exclude', 'rpmbuild',];
  return async () => {
    await $`rsync -a --rsync-path="mkdir -p ${dest} && rsync" ${excluded} --delete-excluded ${src}/ ${host}:${dest}`;
  };
};

const install = (component) => {
  if (component === 'osbuild') {
    return osbuild;
  }
  if (component === 'composer') {
    return composer;
  }
  if (component === 'blueprints') {
    return blueprints;
  }
  return async () => {};
};

const lookupComponents = (key, value) => {
  let src = COMPONENTS[key];
  let dir = src ? key : 'blueprints';
  let component = src ? key : undefined;
  let dest = path.join(PROJECTS_DIR, dir);
  src = src || COMPONENTS[value];
  return {
    src,
    dest,
    component,
    display: component || `${value} blueprints`,
  };
};

const reverseSortArgs = (args) => {
  return Object.keys(args)
    .filter((k) => k != '_')
    .sort()
    .reverse();
};

/*-----------------------------------------------------------------------------
 | Main
 -----------------------------------------------------------------------------*/

const handlePromise = async (p, msg, callback) => {
  await p.then(() => callback(msg)).catch(error);
};

const main = async ({ host, ...args }) => {
  const components = reverseSortArgs(args);
  components.forEach((key) => {
    const value = args[key];
    const { src, dest, component, display } = lookupComponents(key, value);
    const rsync = sync(src, dest, host);
    const installer = install(component);
    spinner(`Installing ${display}`, async () => {
      await handlePromise(rsync(), `Synced ${display}`, info);
      await handlePromise(installer(), `Installed ${display}`, success);
    });
  });
};

await main(argv);
