import type { VFC } from 'react';
import CommonMeta from '../atoms/head/CommonMeta';
import Links from '../atoms/head/Links';
import MobileMeta from '../atoms/head/MobileMeta';
import OpenGraphMeta from '../atoms/head/OpenGraphMeta';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the web app name. */
  readonly appName?: string;
  /** Whether the page is articles. */
  readonly article?: boolean;
  /** Specifies the author name. */
  readonly author?: string;
  /** Specifies the banner height. */
  readonly bannerHeight?: number;
  /** Specifies the banner URL. */
  readonly bannerPath?: string;
  /** Specifies the banner width. */
  readonly bannerWidth?: number;
  /** Specifies the base URL. */
  readonly baseUrl?: string;
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
  /** Specifies the page name. */
  readonly pageName?: string;
}

const HeadContents: VFC<Props> = ({
  appName,
  article,
  author,
  bannerHeight,
  bannerPath,
  bannerWidth,
  baseUrl = '',
  color,
  description,
  keywords,
  pageName,
}) => (
  <>
    <CommonMeta
      appName={appName}
      author={author}
      color={color}
      description={description}
      keywords={keywords}
    />
    <MobileMeta
      appName={appName}
      color={color}
      description={description}
      baseUrl={baseUrl}
    />
    <OpenGraphMeta
      appName={appName}
      article={article}
      bannerHeight={bannerHeight}
      bannerUrl={`${baseUrl}${bannerPath ?? ''}`}
      bannerWidth={bannerWidth}
      pageName={pageName}
    />
    <Links baseUrl={baseUrl} />
  </>
);
HeadContents.displayName = 'HeadContents';

export default HeadContents;
