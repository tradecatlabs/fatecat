/** true when running inside `node --test` (Node.js test runner) */
export const IS_NODE_TEST_RUNTIME = process.execArgv.some((arg) => arg.startsWith('--test'));
