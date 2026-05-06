import type { Genius } from '@kurone-kito/dantalion-core';
import type { AppProps } from 'next/app';
import type { VFC } from 'react';
import '../styles/global.css';
import useChangeLanguage from '../hooks/useChangeLanguage';
import '../i18n';

/** Type definition of the required attributes. */
export interface PageProps {
  /** Specifies the genius type. */
  readonly genius?: Genius;
  /** Specifies the language of this page. */
  readonly lang?: string;
}

/** The app root component */
const App: VFC<AppProps<PageProps>> = ({ Component, pageProps }) => {
  const props = pageProps as PageProps;
  useChangeLanguage(props?.lang);
  // eslint-disable-next-line react/jsx-props-no-spreading
  return <Component {...props} />;
};
App.displayName = 'App';

export default App;
