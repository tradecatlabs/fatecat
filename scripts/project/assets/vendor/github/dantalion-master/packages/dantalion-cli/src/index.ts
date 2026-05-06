#!/usr/bin/env node

import commander from 'commander';
import { version } from '../package.json';
import detail from './detail';
import personality from './personality';
import showJson from './render/showJson';
import showMd from './render/showMd';

[detail, personality].forEach(
  ({ getDescriptionAsync, getObject, alias, command, description }) =>
    commander
      .command(command)
      .alias(alias)
      .option('-r, --raw', 'Returns the raw JSON')
      .description(description)
      .action(async (arg, { raw }) =>
        !raw
          ? showMd(await getDescriptionAsync(arg))
          : showJson(await getObject(arg))
      )
);

commander.version(version);
commander.parse(process.argv);
if (process.argv.length < 1) {
  commander.help();
}
