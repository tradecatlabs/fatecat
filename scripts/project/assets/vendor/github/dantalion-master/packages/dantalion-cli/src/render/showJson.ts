/**
 * Render the object to JSON.
 * @param result The object.
 */
export default (result: unknown): void =>
  // eslint-disable-next-line no-console
  console.info(JSON.stringify(result, null, 2));
