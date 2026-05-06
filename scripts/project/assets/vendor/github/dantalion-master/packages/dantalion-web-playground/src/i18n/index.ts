import { createTAsync } from '@kurone-kito/dantalion-i18n';
import { initReactI18next } from 'react-i18next';
import en from './en.json';
import ja from './ja.json';

createTAsync({ additions: { en, ja }, use: initReactI18next });
