import { error } from './echo.mjs';

const errorHandler = ({ stderr }) => {
  if (stderr) {
    error(stderr);
    process.exit(1);
  }
};

export { errorHandler };
