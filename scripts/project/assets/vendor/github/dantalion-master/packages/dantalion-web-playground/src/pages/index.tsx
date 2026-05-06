import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import Template from '../components/templates/Template';
import type { PageProps } from './_app';

/** The index page component */
const Page: NextPage<PageProps> = () =>
  useRouter().isFallback ? <>Loading...</> : <Template />;
Page.displayName = 'Index';

export default Page;
