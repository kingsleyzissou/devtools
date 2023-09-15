#!/usr/bin/env zx

import { info } from '../../utilities/echo.mjs';

/*-----------------------------------------------------------------------------
 | Set environment variables
 ----------------------------------------------------------------------------*/

const REPO_DIR = path.join(path.sep, 'etc', 'osbuild-composer', 'repositories');
const BIN_DIR = path.join(path.sep, 'usr', 'libexec', 'osbuild-composer');
const COMPOSER_DIR = path.join('projects', 'composer');

/*-----------------------------------------------------------------------------
 | Configure ssh
 ----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

const _ = ssh(host, { port });

/*-----------------------------------------------------------------------------
 | Installation steps
 ----------------------------------------------------------------------------*/

const stopService = async () => {
  info('Stopping composer service...');
  await _`sudo systemctl stop osbuild-composer`;
};

const build = async () => {
  info('Building composer binaries...');
  await _`mkdir -p ${COMPOSER_DIR}/bin`;
  await _`cd ${COMPOSER_DIR}; go build -o bin/ ./cmd/osbuild-composer`;
  await _`cd ${COMPOSER_DIR}; go build -o bin/ ./cmd/osbuild-worker`;
};

const install = async () => {
  info('Installing composer...');
  await _`sudo rm -rf ${BIN_DIR}`;
  await _`cd ${COMPOSER_DIR}; sudo make install`;
};

const copyRepos = async () => {
  info('Copying repositories...');
  await _`sudo rm -rf ${REPO_DIR}`;
  await _`sudo mkdir -p ${REPO_DIR}`;
  await _`sudo cp -r ${COMPOSER_DIR}/test/data/repositories/* ${REPO_DIR}`;
};

const startService = async () => {
  info('Starting composer service...');
  await _`sudo systemctl start osbuild-composer`;
};

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async () => {
  await stopService();
  await build();
  await install();
  await copyRepos();
  await startService();
};

export { main as composer };
