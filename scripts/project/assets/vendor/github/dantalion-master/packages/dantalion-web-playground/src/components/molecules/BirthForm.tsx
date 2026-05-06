import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import type {
  ChangeEventHandler,
  FormEventHandler,
  ReactNode,
  ReactNodeArray,
  VFC,
} from 'react';
import Button from '../atoms/Button';
import Input from '../atoms/Input';
import List from '../atoms/List';

/** Type definition of the required attributes. */
export interface Props {
  /** The default birthday value string */
  readonly birthday?: string;
  /** The label for birthday input control */
  readonly birthdayLabel?: string;
  /** The label for button control */
  readonly buttonLabel?: ReactNode;
  /** The form title */
  readonly legendLabel?: ReactNode;
  /** The default nickname value string */
  readonly nickname?: string;
  /** The label for nickname input control */
  readonly nicknameLabel?: string;
  /** The default nickname value string */
  readonly notes?: ReactNodeArray;
  /** Callback to call when the user changes the birthday */
  readonly onChangeBirthday?: ChangeEventHandler<HTMLInputElement>;
  /** Callback to call when the user changes the nickname */
  readonly onChangeNickname?: ChangeEventHandler<HTMLInputElement>;
  /** Callback to call when the user taps to submit button */
  readonly onSubmit?: FormEventHandler<HTMLFormElement>;
}

/** The birthday form component. */
const BirthForm: VFC<Props> = ({
  birthday,
  birthdayLabel,
  buttonLabel,
  legendLabel,
  nickname,
  nicknameLabel,
  onChangeBirthday,
  onChangeNickname,
  onSubmit,
  notes,
}) => (
  <form
    className="nm-flat-gray-300-xs p-6 dark:nm-flat-gray-600-xs md:rounded-3xl"
    onSubmit={onSubmit}
  >
    <fieldset>
      <legend className="font-light text-gray-700 text-xl dark:text-gray-200">
        {legendLabel}
      </legend>
      <Input
        autoComplete="bday"
        defaultValue={birthday}
        enterKeyHint="go"
        id="birthday"
        label={birthdayLabel}
        max="2050-12-31"
        min="1873-02-01"
        name="birthday"
        onChange={onChangeBirthday}
        required
        type="date"
      />
      <Input
        autoComplete="nickname"
        defaultValue={nickname}
        enterKeyHint="go"
        id="nickname"
        label={nicknameLabel}
        maxLength={240}
        name="nickname"
        onChange={onChangeNickname}
        placeholder={nicknameLabel}
        type="text"
      />
      <List className="text-red-900 text-sm dark:text-red-200">{notes}</List>
      <Button>
        <FontAwesomeIcon className="animate-pulse mx-2" icon={faSearch} />
        {buttonLabel}
      </Button>
    </fieldset>
  </form>
);
BirthForm.displayName = 'BirthForm';

export default BirthForm;
