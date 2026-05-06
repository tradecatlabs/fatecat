import type { VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the web app name. */
  readonly appName?: string;
  /** Specifies the author name. */
  readonly author?: string;
  /** Specifies the theme color. */
  readonly color?: string;
  /**
   * Specifies the short description of the document.
   *
   * (limit to 150 characters)
   */
  readonly description?: string;
  /** Specifies the keywords. */
  readonly keywords?: readonly string[];
}

/** The minimum metadata component. */
const CommonMeta: VFC<Props> = ({
  appName,
  author,
  color,
  description,
  keywords,
}) => (
  <>
    <script
      type="text/javascript"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: process.env.applyDarkMode ?? '' }}
    />
    <meta httpEquiv="cleartype" content="on" />
    <meta httpEquiv="x-ua-compatible" content="ie=Edge" />
    {!!appName && <meta name="application-name" content={appName} />}
    {!!author && <meta name="author" content={author} />}
    <meta name="color-scheme" content="light dark" />
    <meta name="coverage" content="Worldwide" />
    {!!description && <meta name="description" content={description} />}
    <meta name="format-detection" content="telephone=no" />
    {!!keywords?.length && <meta name="keywords" content={keywords.join()} />}
    <meta name="rating" content="General" />
    <meta name="referer" content="same-origin" />
    <meta name="SKYPE_TOOLBAR" content="SKYPE_TOOLBAR_PARSER_COMPATIBLE" />
    {!!color && <meta name="theme-color" content={color} />}
  </>
);
CommonMeta.displayName = 'CommonMeta';

export default CommonMeta;
