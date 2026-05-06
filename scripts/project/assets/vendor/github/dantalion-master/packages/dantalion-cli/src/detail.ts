import { Genius, getDetail, types } from '@kurone-kito/dantalion-core';
import {
  createAccessorsAsync,
  getDetailMarkdown,
} from '@kurone-kito/dantalion-i18n';
import type { Command } from './type';

const command: Command = {
  getDescriptionAsync: async (detail) =>
    getDetailMarkdown(await createAccessorsAsync(), detail as Genius),
  getObject: (detail) => getDetail(detail as Genius) || types.genius,
  alias: 'dt',
  command: 'detail [genius]',
  description:
    'Show detail of genius. If omitted the argument, show a list of genius types.',
};

export default command;
