import { getLocale, locales } from '@kurone-kito/dantalion-i18n';
import { ChangeEventHandler, useCallback, useMemo, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import { useLanguage, useRoute } from '../../hooks/useQuery';
import Select from '../atoms/Select';

/** The type definition of the source. */
type Source = readonly (readonly [string, string])[];

/** Constant key indicating automatic recognition. */
const autoKey = 'auto';

/** The language list. */
const baseSource: Source = Object.entries(locales);

/** Create the callback on changed control by the user. */
const useOnChange = (): ChangeEventHandler<HTMLSelectElement> => {
  const route = useRoute();
  const { i18n } = useTranslation();
  return useCallback(
    async (e) => {
      e.preventDefault();
      const { value } = e.currentTarget;
      const nextLang = value === autoKey ? undefined : value;
      await route({ lang: nextLang ?? '' });
      await i18n.changeLanguage(nextLang ?? getLocale());
    },
    [i18n, route]
  );
};

/** The language select component. */
const LanguageSelector: VFC = () => {
  const { t } = useTranslation();
  const language = useLanguage() ?? autoKey;
  const onChange = useOnChange();
  const source = useMemo<Source>(
    () => [[autoKey, t('web.language.automatic')], ...baseSource],
    [t]
  );
  return (
    <Select
      defaultValue={language}
      id="language"
      label={t('web.language.name')}
      onChange={onChange}
      source={source}
    />
  );
};
LanguageSelector.displayName = 'LanguageSelector';

export default LanguageSelector;
