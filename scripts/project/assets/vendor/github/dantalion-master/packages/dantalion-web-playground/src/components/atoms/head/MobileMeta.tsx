import type { VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the web app name. */
  readonly appName?: string;
  /** Specifies the theme color. */
  readonly color?: string;
  /** Specifies the short description. */
  readonly description?: string;
  /** Specifies the base URL. */
  readonly baseUrl?: string;
}

/** The component of metadata for mobile browser. */
const MobileMeta: VFC<Props> = ({
  appName,
  color,
  description,
  baseUrl = '',
}) => (
  <>
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="default" />
    {!!appName && <meta name="apple-mobile-web-app-title" content={appName} />}
    {!!color && (
      <>
        <meta name="msapplication-navbutton-color" content={color} />
        <meta name="msapplication-TileColor" content={color} />
      </>
    )}
    {!!baseUrl && <meta name="msapplication-starturl" content={baseUrl} />}
    {!!description && (
      <meta name="msapplication-tooltip" content={description} />
    )}
    <meta
      name="msapplication-config"
      content={`${baseUrl}/favicons/browserconfig.xml`}
    />
  </>
);
MobileMeta.displayName = 'MobileMeta';

export default MobileMeta;
