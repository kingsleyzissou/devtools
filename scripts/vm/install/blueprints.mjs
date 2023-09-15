#!/usr/bin/env zx

import { info } from '../../utilities/echo.mjs';

/*-----------------------------------------------------------------------------
 | Set environment variables
 ----------------------------------------------------------------------------*/

const BLUEPRINTS_DIR = path.join('projects', 'blueprints');

/*-----------------------------------------------------------------------------
 | Configure ssh
 ----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

const _ = ssh(host, { port });

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async (directory = BLUEPRINTS_DIR) => {
  info('Pushing blueprints...');
  await _`composer-cli blueprints push ${directory}/*`;
  const { stdout } = await _`composer-cli blueprints list`;
  info(`Blueprints list:\n${stdout.trim()}`);
};

export { main as blueprints };
