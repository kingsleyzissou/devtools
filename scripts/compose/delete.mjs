#!/usr/bin/env zx

import { assert, usage, success } from '../utilities/index.mjs';
import { getComposes, getStatus, deleteCompose } from './common.mjs';

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
${chalk.bold(chalk.blue('Delete compose'))}
  Delete a compose request from a remote machine.

${chalk.bold('Usage:')}
  ./delete.mjs [options]

${chalk.bold('Options:')}
  --id=<compose_id>    delete a single compose
  --all                delete all composes
  --failed             delete failed composes
  --finished           delete finished composes
  --host=<host>        remote host [default: localvm]
  --port=<port>        remote port [default: 2222]
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

assert(
  (argv.id || argv.all || argv.failed || argv.finished) === undefined,
  USAGE_TEXT
);

/*-----------------------------------------------------------------------------
| Helper functions
-----------------------------------------------------------------------------*/

const deleteFailed = async () => {
  const composes = await getComposes();
  const failed = composes.find((compose) => compose.body.failed);
  for (const compose of failed.body.failed) {
    const { id } = compose;
    await deleteCompose(id);
  }
};

const deleteFinished = async () => {
  const composes = await getComposes();
  const finished = composes.find((compose) => compose.body.finished);
  for (const compose of finished.body.finished) {
    const { id } = compose;
    await deleteCompose(id);
  }
};

const deleteAll = async () => {
  await deleteFailed();
  await deleteFinished();
};

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async (id, all, finished, failed) => {
  let msg = id ? `compose ${id}` : 'composes';
  await spinner(`Deleting ${msg}...`, async () => {
    if (all) await deleteAll();
    if (id) await deleteCompose(id);
    if (failed) await deleteFailed();
    if (finished) await deleteFinished();
  });
  msg = msg.charAt(0).toUpperCase() + msg.slice(1);
  success(`${msg} deleted`);
  console.log(await getStatus());
};

await main(argv.id, argv.all, argv.finished, argv.failed);
