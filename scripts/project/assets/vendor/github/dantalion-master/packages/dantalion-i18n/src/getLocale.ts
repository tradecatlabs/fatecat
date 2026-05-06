/**
 * Get the locale information from the Intl API.
 * @returns The locale string e.g. `en-US`.
 */
export default (): string => Intl.DateTimeFormat().resolvedOptions().locale;
