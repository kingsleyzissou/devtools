const info = (msg) => {
  const header = chalk.blue('[ Info ]');
  echo(header, msg);
};

const error = (msg) => {
  const header = chalk.red('[ Error ]');
  echo(header, msg);
};

const success = (msg) => {
  const header = chalk.green('[ Success ]');
  echo(header, msg);
};

const echo = (header, msg) => {
  console.log(`${chalk.bold(header)} ${msg}`);
};

export { info, error, success };
