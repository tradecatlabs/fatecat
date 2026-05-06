import { getPersonality } from '@kurone-kito/dantalion-core';
import {
  createAccessorsAsync,
  getPersonalityMarkdown,
} from '@kurone-kito/dantalion-i18n';
import type { Command } from './type';

const command: Command = {
  getDescriptionAsync: async (birthday) =>
    getPersonalityMarkdown(await createAccessorsAsync(), birthday as string),
  getObject: (birthday) => getPersonality(birthday as string),
  alias: 'ps',
  command: 'personality <birthday>',
  description: 'Show personality associated with the specified birthday.',
};

export default command;
