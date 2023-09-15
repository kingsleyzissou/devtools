#!/usr/bin/env zx

import { assert, usage, success } from '../utilities/index.mjs';
import { deleteCompose, getStatus, errorHandler } from './common.mjs';

/*-----------------------------------------------------------------------------
| Configure ssh
-----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

$ = ssh(host, { port, verbose: false });

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Cancel compose'))}
  Cancel and delete a compose from a remote machine.

${chalk.bold('Usage:')}
  ./cancel.mjs [options]

${chalk.bold('Options:')}
  --id=<compose_id>    delete a single compose
  --host=<host>        remote host [default: localvm]
  --port=<port>        remote port [default: 2222]
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

assert(argv.id === undefined, USAGE_TEXT);

/*-----------------------------------------------------------------------------
| Helper functions
-----------------------------------------------------------------------------*/

const cancel = async (id) => {
  try {
    await $`composer-cli compose cancel ${id}`;
  } catch (error) {
    errorHandler(error);
  }
};

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async (id) => {
  await spinner('Canceling compose...', async () => await cancel(id));
  await spinner('Deleting compose...', async () => await deleteCompose(id));
  success('Compose canceled and deleted');
  console.log(await getStatus());
};

await main(argv.id);
