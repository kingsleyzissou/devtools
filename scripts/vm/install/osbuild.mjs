#!/usr/bin/env zx

import { info } from '../../utilities/echo.mjs';

/*-----------------------------------------------------------------------------
 | Set environment variables
 ----------------------------------------------------------------------------*/

const OSBUILD_DIR = path.join('projects', 'osbuild');

/*-----------------------------------------------------------------------------
 | Configure ssh
 ----------------------------------------------------------------------------*/

const host = argv.host || 'localvm';
const port = argv.port || 2222;

const _ = ssh(host, { port });

/*-----------------------------------------------------------------------------
 | Installation steps
 ----------------------------------------------------------------------------*/

const gitClean = async () => {
  info('Cleaning git tree...');
  await _`cd ${OSBUILD_DIR}; git clean -xdf`;
  await _`cd ${OSBUILD_DIR}; git commit . -m wip --allow-empty`;
};

const buildDeps = async () => {
  info('Building dependencies...');
  await _`cd ${OSBUILD_DIR}; sudo dnf -y builddep osbuild.spec`;
};

const build = async () => {
  info('Building...');
  await _`cd ${OSBUILD_DIR}; make rpm`;
};

const install = async () => {
  info('Installing rpm...');
  await _`cd ${OSBUILD_DIR}; sudo dnf install -y rpmbuild/RPMS/noarch/*.rpm`;
};

/*-----------------------------------------------------------------------------
| Main
-----------------------------------------------------------------------------*/

const main = async () => {
  await gitClean();
  await buildDeps();
  await build();
  await install();
};

export { main as osbuild };
