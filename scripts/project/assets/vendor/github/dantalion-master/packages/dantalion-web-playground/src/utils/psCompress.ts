/* eslint-disable no-bitwise */
import { Personality, types } from '@kurone-kito/dantalion-core';
import { Base64 } from 'js-base64';
import chunk from 'lodash.chunk';

export interface PSWithName extends Personality {
  readonly name?: string;
}

const xor = (list: number[]) => list.reduce((acc, cur) => acc ^ cur, 0xf);

const psFromArray = (array: number[]): Personality => ({
  cycle: array[3] + 1,
  inner: types.genius[array[0]],
  lifeBase: types.lifeBase[array[6]],
  outer: types.genius[array[1]],
  potentials: [types.potential[array[4]], types.potential[array[5]]],
  workStyle: types.genius[array[2]],
});

const psToArray = (ps: Personality) => [
  types.genius.indexOf(ps.inner),
  types.genius.indexOf(ps.outer),
  types.genius.indexOf(ps.workStyle),
  ps.cycle - 1,
  types.potential.indexOf(ps.potentials[0]),
  types.potential.indexOf(ps.potentials[1]),
  types.lifeBase.indexOf(ps.lifeBase),
];

export const decode = (str: string): Personality | undefined => {
  const raw = [...Base64.toUint8Array(str)];
  const src = raw.flatMap((b) => [b & 0xf, (b >> 4) & 0xf]);
  if (!src.length) {
    return undefined;
  }
  const [v, [cd]] = chunk(src, 7);
  return xor(v) === cd ? psFromArray(v) : undefined;
};

export const encode = (ps: Personality): string => {
  const v = psToArray(ps);
  const bytes = chunk([...v, xor(v)], 2).map((byte) =>
    byte.reduce((acc, cur, index) => acc + (cur << (index * 4)), 0)
  );
  return Base64.fromUint8Array(new Uint8Array(bytes), true);
};
