/** Type definition of the options for `createTitle` function. */
export interface Options {
  /** Specifies the web app name. */
  readonly appName?: string;
  /** Specifies the page name. */
  readonly pageName?: string;
}

/**
 * Create the title.
 * @param options The options.
 */
const createTitle = ({ appName, pageName }: Options = {}): string =>
  (pageName ? [pageName, appName] : [appName]).join('::');

export default createTitle;
