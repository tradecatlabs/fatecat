import { ChangeEventHandler, useCallback, useMemo, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import useIsSsr from '../../hooks/useIsSsr';
import Select from '../atoms/Select';

/** The type definition of the source. */
type Source = readonly (readonly [string, string])[];

/** Constant keys. */
const keys = ['automatic', 'light', 'dark'] as const;

/** Create the callback on changed control by the user. */
const useOnChange = (): ChangeEventHandler<HTMLSelectElement> => {
  return useCallback(async (e) => {
    const root = window.document.getElementsByTagName('html')[0];
    switch (e.currentTarget.value) {
      case 'automatic':
        localStorage.removeItem('theme');
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
          root.classList.add('dark');
        } else {
          root.classList.remove('dark');
        }
        break;
      case 'dark':
        localStorage.theme = 'dark';
        root.classList.add('dark');
        break;
      case 'light':
        localStorage.theme = 'light';
        root.classList.remove('dark');
        break;
      default:
        break;
    }
    e.preventDefault();
  }, []);
};

/** The appearance select component. */
const AppearanceSelector: VFC = () => {
  const { t } = useTranslation();
  const isSsr = useIsSsr();
  const onChange = useOnChange();
  const source = useMemo<Source>(
    () => keys.map((key) => [key, t(`web.appearance.${key}`)]),
    [t]
  );
  return isSsr() ? null : (
    <Select
      defaultValue={!('theme' in localStorage) ? undefined : localStorage.theme}
      id="appearance"
      label={t('web.appearance.name')}
      onChange={onChange}
      source={source}
    />
  );
};
AppearanceSelector.displayName = 'AppearanceSelector';

export default AppearanceSelector;
