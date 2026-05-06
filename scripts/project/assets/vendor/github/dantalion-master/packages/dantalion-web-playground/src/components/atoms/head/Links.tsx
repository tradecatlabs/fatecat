import type { VFC } from 'react';

/** Type definition of the required attributes. */
export interface Props {
  /** Specifies the base URL. */
  readonly baseUrl?: string;
}

/** The root path. */
const root = '/';

/** The links list component. */
const Links: VFC<Props> = ({ baseUrl = '' }) => {
  const rootUrl = baseUrl || root;
  return (
    <>
      <link rel="author" href="https://kit.black/" />
      <link
        rel="apple-touch-icon"
        sizes="180x180"
        href={`${baseUrl}/favicons/apple-touch-icon.png`}
      />
      <link rel="bookmark" href={rootUrl} />
      <link rel="canonical" href={rootUrl} />
      <link rel="first" href={rootUrl} />
      <link
        rel="icon"
        type="image/png"
        sizes="32x32"
        href={`${baseUrl}/favicons/favicon-32x32.png`}
      />
      <link
        rel="icon"
        type="image/png"
        sizes="194x194"
        href={`${baseUrl}/favicons/favicon-194x194.png`}
      />
      <link
        rel="icon"
        type="image/png"
        sizes="192x192"
        href={`${baseUrl}/favicons/android-chrome-192x192.png`}
      />
      <link
        rel="icon"
        type="image/png"
        sizes="16x16"
        href={`${baseUrl}/favicons/favicon-16x16.png`}
      />
      <link rel="manifest" href={`${baseUrl}/favicons/site.webmanifest`} />
      <link
        rel="mask-icon"
        href={`${baseUrl}/favicons/safari-pinned-tab.svg`}
        color="#374151"
      />
      <link rel="shortcut icon" href={`${baseUrl}/favicons/favicon.ico`} />
    </>
  );
};
Links.displayName = 'Links';

export default Links;
