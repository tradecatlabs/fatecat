export { default as getLocale } from './getLocale';
export { getDetailMarkdown, getPersonalityMarkdown } from './build';
export {
  Accessors,
  createAccessors,
  default as createAccessorsAsync,
} from './resources/createAccessorsAsync';
export type { DetailAccessor } from './resources/createGenericAccessor';
export {
  default as createTAsync,
  fallbackLng as fallbackLanguage,
  CreateTAsyncOptions,
  locales,
} from './resources/createTAsync';
export type {
  DesctiptionsType,
  DetailsBaseType,
  DetailsType,
  PersonalityDetailBaseType,
  PersonalityDetailType,
  PersonalityType,
  VectorType,
} from './resources/types';
