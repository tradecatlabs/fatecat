import type { Genius } from '@kurone-kito/dantalion-core';
import { useRouter } from 'next/router';
import type { ParsedUrlQueryInput } from 'querystring';
import { useCallback } from 'react';
import useIsSsr from './useIsSsr';

/** Type definition of the arguments for the routing function. */
export interface RouteProps {
  /** If you need the change inner genius, specify them. */
  readonly genius?: Genius;
  /** If you need the change language, specify them. */
  readonly lang?: string;
  /** If you need the change result, specify them. */
  readonly result?: string;
}

/** Type definition of the routing function. */
export type Route = (props?: RouteProps) => Promise<boolean>;

/** The query elements list to ignore. */
const excludes = Object.freeze(['genius', 'lang']);

/** Detect the language from the query. */
export const useGenius = (): Genius | undefined => {
  const { query } = useRouter();
  const result = query.genius ?? query.lang;
  return typeof result === 'string' &&
    !Number.isNaN(Number.parseInt(result, 10))
    ? (result as Genius)
    : undefined;
};

/** Detect the language from the query. */
export const useLanguage = (): string | undefined => {
  const { query } = useRouter();
  const genius = useGenius();
  const { lang } = query;
  return typeof lang === 'string' && !(genius && genius === lang)
    ? lang
    : undefined;
};

/** Detect the personality result from the query. */
export const useResultQuery = (): string | undefined => {
  const isSsr = useIsSsr();
  const { query } = useRouter();
  return isSsr(true)
    ? Object.keys(query).find((q) => !excludes.includes(q))
    : undefined;
};

/**
 * Create the query parameters for routing.
 * @param props The arguments.
 */
const createQuery = ({
  genius,
  result,
  lang,
}: RouteProps): ParsedUrlQueryInput => ({
  ...(genius && lang ? { genius, lang } : undefined),
  ...((lang || genius) && !(genius && lang)
    ? { lang: lang || genius }
    : undefined),
  ...(result ? { [result]: '' } : undefined),
});

/**
 * Create the path name parameters for routing.
 * @param props The arguments.
 */
const createPathName = ({
  genius,
  lang,
}: Pick<RouteProps, 'genius' | 'lang'>) =>
  `/${lang || genius ? '[lang]' : ''}${lang && genius ? '/[genius]' : ''}`;

/** Create the route function. */
export const useRoute = (): Route => {
  const defaultGenius = useGenius();
  const defaultLang = useLanguage();
  const defaultResult = useResultQuery();
  const router = useRouter();
  return useCallback<Route>(
    ({
      genius = defaultGenius,
      lang = defaultLang,
      result = defaultResult,
    } = {}) =>
      router.push(
        {
          query: createQuery({ genius, lang, result }),
          pathname: createPathName({ genius, lang }),
        },
        undefined,
        { scroll: true, shallow: true }
      ),
    [defaultGenius, defaultLang, defaultResult, router]
  );
};
