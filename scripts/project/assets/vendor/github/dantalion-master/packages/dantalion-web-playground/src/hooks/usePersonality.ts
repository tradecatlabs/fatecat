import { getPersonality, Personality } from '@kurone-kito/dantalion-core';
import { Base64 } from 'js-base64';
import { FormEventHandler, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import type { FormState } from '../stores/FormReducer';
import { decode, encode } from '../utils/psCompress';
import { useResultQuery, useRoute } from './useQuery';

/** The splitter that between to personality code and nickname. */
export const spliter = '~';

/** It's the React custom hook which it decodes to personality code. */
export const usePSDecoder = (): readonly [Personality | undefined, string] => {
  const [pb = '', nb] = (useResultQuery() ?? '').split(spliter);
  const { t } = useTranslation();
  return [
    decode(pb),
    (nb && Base64.decode(nb)) || t('web.result.nickname'),
  ] as const;
};

/**
 * It's the React custom hook which it encodes to personality code
 * and redirects.
 * @param props Specifies the store object.
 */
export const usePSRedirection = ({
  birthday,
  nickname,
}: FormState): FormEventHandler<HTMLFormElement> => {
  const route = useRoute();
  return useCallback(
    async (e) => {
      e.preventDefault();
      const ps = getPersonality(birthday);
      const n = Base64.encode(nickname, true);
      return (
        ps &&
        route({
          genius: ps.inner,
          result: `${encode(ps)}${n && `${spliter}${n}`}`,
        })
      );
    },
    [birthday, nickname, route]
  );
};
