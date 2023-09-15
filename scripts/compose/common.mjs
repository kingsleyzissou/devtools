import { errorHandler as checkError, flush } from '../utilities/index.mjs';

const deleteCompose = async (id) => {
  try {
    await $`composer-cli compose delete ${id}`;
  } catch (error) {
    errorHandler(error);
  }
};

const getComposes = async () => {
  const { stdout } = await $`composer-cli compose list --json`;
  return JSON.parse(stdout);
};

const getStatus = async () => {
  const { stdout } = await $`composer-cli compose list`;
  return stdout.trim();
};

const findError = (results) => {
  for (const result of results) {
    const { errors } = result.body;
    return errors[0].msg;
  }
  return 'Something went wrong!';
};

const parseError = ({ stdout, stderr }) => {
  // compose errors come through stdout as
  // json formatted strings. Regular errors
  // come through stderr.
  if (stderr) return stderr;
  return `\n${findError(JSON.parse(stdout))}`;
};

const errorHandler = ({ stdout, stderr }) => {
  flush(); // flush spinner
  const e = parseError({ stdout, stderr });
  checkError({ stderr: e });
};

export { deleteCompose, getComposes, getStatus, errorHandler };
