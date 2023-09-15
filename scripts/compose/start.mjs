#!/usr/bin/env zx

import { assert, usage, success, info } from '../utilities/index.mjs';
import { errorHandler } from './common.mjs';

/*-----------------------------------------------------------------------------
| Configure ssh
-----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

let shell = $;
$ = ssh(host, { port, verbose: false });

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const USAGE_TEXT = `
${chalk.bold(chalk.blue('Start compose'))}
  Start a compose request on a remote machine.

${chalk.bold('Usage:')}
  ./start.mjs [options]

${chalk.bold('Options:')}
  --blueprint=<name>   the blueprint to build
  --wait               wait for compose to finish
  --type=<image_type>  image type [default: qcow2]
  --host=<host>        remote host [default: localvm]
  --port=<port>        remote port [default: 2222]
  --help, -h           print help
`;

if (argv.help || argv.h) {
  usage(USAGE_TEXT);
}

assert(argv.blueprint === undefined, USAGE_TEXT);

/*-----------------------------------------------------------------------------
| Helper functions
-----------------------------------------------------------------------------*/

const findId = (results) => {
  for (const result of results) {
    const { build_id } = result.body;
    return build_id;
  }
  throw 'No id found';
};

const findStatus = (results) => {
  for (const result of results) {
    const { queue_status } = result.body;
    if (queue_status) {
      return queue_status;
    }
  }
  throw 'Unknown error';
};

const checkStatus = async (id) => {
  try {
    const { stdout } = await $`composer-cli compose info ${id} --json`;
    return findStatus(JSON.parse(stdout));
  } catch (e) {
    errorHandler(e);
  }
};

const waitForCompose = async (id) => {
  while (true) {
    const status = await checkStatus(id);
    if (status == 'FINISHED') {
      success(`Compose finished: ${id}`);
      break;
    }
    if (status == 'FAILED') {
      errorHandler({ stderr: `Compose failed: ${id}` });
    }
    sleep(1000);
  }
};

const copyComposeIdToClipboard = async (id) => {
  shell`wl-copy ${id}`.nothrow();
  shell`pkill wl-copy`.nothrow();
};

const startCompose = async (blueprint, type = 'qcow2', callback) => {
  try {
    const res = await $`composer-cli compose --json start ${blueprint} ${type}`;
    const id = findId(JSON.parse(res.stdout));
    copyComposeIdToClipboard(findId(JSON.parse(res.stdout)));
    callback(`Compose started: ${id}`);
    return id;
  } catch (e) {
    errorHandler(e);
  }
};

/*-----------------------------------------------------------------------------
| Usage
-----------------------------------------------------------------------------*/

const main = async (blueprint, type = 'qcow2', wait = false) => {
  spinner('Starting compose...', async () => {
    const cb = wait ? info : success;
    const id = await startCompose(blueprint, type, cb);
    if (wait) {
      await waitForCompose(id);
    }
  });
};

await main(argv.blueprint, argv.type, argv.wait);
