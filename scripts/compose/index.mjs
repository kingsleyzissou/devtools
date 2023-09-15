#!/usr/bin/env zx

if (argv.status) {
  await $`./status.mjs`;
  process.exit(0);
}
