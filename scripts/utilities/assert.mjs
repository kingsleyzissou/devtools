import { error } from './echo.mjs';

const assert = async (condition, msg, level, code) => {
  if (condition) {
    if (!level) {
      console.log(chalk.white(msg));
      process.exit(code || 2);
    }
    error(msg);
    process.exit(code || 1);
  }
};

export { assert };
