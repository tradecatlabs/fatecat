export enum Sex {
  female,
  male
}

export interface GBData {
  score: number;
  nums: number[];
  desc: string;
  sex?: Sex;
}

export enum Ele {
  wood,
  fire,
  earth,
  metal,
  water,
}

export interface CharData {
  char: string;
  ele: Ele;
  strokes: number;
  sound: string;
}
