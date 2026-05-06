import type { VFC } from 'react';
import createTitle from '../../../utils/createTitle';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the web app name. */
  readonly appName?: string;
  /** Whether the page is articles. */
  readonly article?: boolean;
  /** Specifies the banner height. */
  readonly bannerHeight?: number;
  /** Specifies the banner URL. */
  readonly bannerUrl?: string;
  /** Specifies the banner width. */
  readonly bannerWidth?: number;
  /** Short description of the document (limit to 150 characters) */
  readonly description?: string;
  /** Specifies the page name. */
  readonly pageName?: string;
}

/** The component of metadata for social site. */
const OpenGraphMeta: VFC<Props> = ({
  appName,
  article,
  bannerHeight,
  bannerUrl,
  bannerWidth,
  description,
  pageName = appName,
}) => (
  <>
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:creator" content="@kurone_kito" />
    {!!description && <meta name="twitter:description" content={description} />}
    {!!bannerUrl && <meta name="twitter:image" content={bannerUrl} />}
    {!!pageName && (
      <meta name="twitter:title" content={createTitle({ appName, pageName })} />
    )}
    {!!description && <meta property="og:description" content={description} />}
    {!!bannerUrl && (
      <>
        <meta property="og:image" content={bannerUrl} />
        {!!bannerHeight && (
          <meta property="og:image:height" content={`${bannerHeight}`} />
        )}
        {!!bannerWidth && (
          <meta property="og:image:width" content={`${bannerWidth}`} />
        )}
      </>
    )}
    {!!appName && <meta property="og:site_name" content={appName} />}
    {!!pageName && <meta property="og:title" content={pageName} />}
    <meta property="og:type" content={article ? 'article' : 'website'} />
    <meta property="op:markup_version" content="v1.0" />
  </>
);
OpenGraphMeta.displayName = 'OpenGraphMeta';

export default OpenGraphMeta;
