const flush = () => {
  process.stderr.write(' '.repeat(process.stdout.columns - 1) + '\r');
};

export { flush };
