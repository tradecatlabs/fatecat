import { ChangeEventHandler, useCallback, VFC } from 'react';
import { useTranslation } from 'react-i18next';
import MoleculesBirthForm from '../molecules/BirthForm';
import { usePSRedirection } from '../../hooks/usePersonality';
import FormReducer, {
  setBirthday,
  setNickname,
} from '../../stores/FormReducer';

/** The birthday form component. */
const BirthForm: VFC = () => {
  const { t } = useTranslation();
  const [state, action] = FormReducer.useContainer();
  return (
    <MoleculesBirthForm
      birthday={state.birthday}
      birthdayLabel={t('web.form.birthday')}
      buttonLabel={t('web.form.submit')}
      legendLabel={t('web.form.legend')}
      nickname={state.nickname}
      nicknameLabel={t('web.form.nickname')}
      notes={t('web.form.notes', { returnObjects: true })}
      onChangeBirthday={useCallback<ChangeEventHandler<HTMLInputElement>>(
        (e) => action([setBirthday, e.currentTarget.value]),
        [action]
      )}
      onChangeNickname={useCallback<ChangeEventHandler<HTMLInputElement>>(
        (e) => action([setNickname, e.currentTarget.value]),
        [action]
      )}
      onSubmit={usePSRedirection(state)}
    />
  );
};
BirthForm.displayName = 'BirthForm';

export default BirthForm;
