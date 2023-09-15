#!/usr/bin/env zx

import { assert, usage, errorHandler } from '../utilities/index.mjs';

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Oscap blueprint generator'))}
  Run an oscap scan on a remote machine.

${chalk.bold('Usage:')}
  ./scan.mjs [options]

${chalk.bold('Options:')}
  profile              profile to use
  --distro, -d         datastream distro to use <rhel8|rhel9|centos-8|cs9|fedora>
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

const profile = argv._[0];
const distro = argv.distro || argv.d;

assert(profile == undefined, USAGE_TEXT);
assert(distro == undefined, USAGE_TEXT);

/*-----------------------------------------------------------------------------
| Define constants
-----------------------------------------------------------------------------*/

$.verbose = false;

const DATASTREAM_DIR = '/usr/share/xml/scap/ssg/content';

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const generate = async (flags, datastream) => {
  try {
    await $`sudo oscap xccdf generate fix ${flags} ${datastream}`;
  } catch (error) {
    errorHandler(error);
  }
};

const main = async (profile, distro) => {
  const datastreamPath = path.join(DATASTREAM_DIR, `ssg-${distro}-ds.xml`);
  const flags = ['--profile', profile, '--fix-type', 'blueprint'];
  await generate(flags, datastreamPath);
};

main(profile, distro);
