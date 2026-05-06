import { Reducer, useReducer } from 'react';
import { createContainer } from 'unstated-next';

/** A definition for the identifier is used to store the birthday. */
export const setBirthday = Symbol('setBirthday');

/** A definition for the identifier is used to store the nickname. */
export const setNickname = Symbol('setNickname');

/** Default birthday value. */
const defaultBirthday = '2000-01-01';

/** The type definition of actions key. */
export type FormActionType = typeof setBirthday | typeof setNickname;

/** The type definition of the action. */
export type FormAction = readonly [FormActionType, string | undefined];

/** The type definition of the state data. */
export interface FormState {
  /** The birthday. */
  readonly birthday: string;
  /** The nickname. */
  readonly nickname: string;
}

/**
 * The reducer implementation for stores the birthday data.
 * @param state The current state data.
 * @param action The action data.
 * @returns The new state data.
 */
const formReducer: Reducer<FormState, FormAction> = (
  state,
  [type, payload]
) => {
  switch (type) {
    case setBirthday:
      return { ...state, birthday: payload ?? defaultBirthday };
    case setNickname:
      return { ...state, nickname: payload ?? '' };
    default:
      return state;
  }
};

export default createContainer(() =>
  useReducer(formReducer, { birthday: defaultBirthday, nickname: '' })
);
