#!/usr/bin/env zx

import { usage } from '../utilities/usage.mjs';
import { getStatus } from './common.mjs';

/*-----------------------------------------------------------------------------
 | Configure ssh
 ----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

$ = ssh(host, { port, verbose: false });

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Compose status'))}
  Check the status of composes on a remote machine.

${chalk.bold('Usage:')}
  ./status.mjs [options]

${chalk.bold('Options:')}
  --host               remote host [default: localvm]
  --port               remote port [default: 2222]
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async () => {
  const composes = await getStatus();
  console.log(composes);
};

await main();
