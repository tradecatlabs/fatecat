import type { Meta, Story } from '@storybook/react';
import { useCallback } from 'react';
import BirthForm, { Props } from './BirthForm';

export default Object.freeze<Meta>({
  argTypes: {
    onChangeBirthday: { action: 'onChangeBirthday' },
    onChangeNickname: { action: 'onChangeNickname' },
    onSubmit: { action: 'onSubmit' },
  },
  component: BirthForm,
  title: `molecules/${BirthForm.displayName}`,
});

const Template: Story<Props> = ({
  birthday,
  birthdayLabel,
  buttonLabel,
  legendLabel,
  nickname,
  nicknameLabel,
  notes,
  onChangeBirthday,
  onChangeNickname,
  onSubmit,
}) => (
  <BirthForm
    birthday={birthday}
    birthdayLabel={birthdayLabel}
    buttonLabel={buttonLabel}
    legendLabel={legendLabel}
    nickname={nickname}
    nicknameLabel={nicknameLabel}
    notes={notes}
    onChangeBirthday={onChangeBirthday}
    onChangeNickname={onChangeNickname}
    onSubmit={useCallback(
      (e) => {
        e.preventDefault();
        onSubmit?.(e);
      },
      [onSubmit]
    )}
  />
);

export const Default = Template.bind({});
Default.args = {
  birthday: '2000-01-01',
  birthdayLabel: 'BirthdayLabel',
  buttonLabel: 'ButtonLabel',
  legendLabel: 'LegendLabel',
  nickname: 'Nickname',
  nicknameLabel: 'NicknameLabel',
  notes: ['Foo', 'Bar', 'Qux'],
};
