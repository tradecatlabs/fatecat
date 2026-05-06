import { intersection, sortedUniq, without } from "lodash";
import { CharData, GBData, Sex } from "./types";

const composeNums = (
  gbNums: GBData[],
  index: number = 0,
  filters: number[]
) => {
  if (index >= gbNums.length) return [];
  let result: GBData[] = [];
  for (let i = index, cur: GBData; i < gbNums.length; i++) {
    const filteredNums = without(gbNums[i].nums, ...filters);
    if (filteredNums.length === 0) {
      continue;
    }
    cur = { ...gbNums[i], nums: filteredNums };
    result.push(cur);
    const subRes = composeNums(gbNums, i + 1, filters);
    for (let j = 0, subCur; j < subRes.length; j++) {
      subCur = subRes[j];
      const inter = intersection(cur.nums, subCur.nums);
      if (inter.length > 0) {
        result.push({
          desc: cur.desc + " + " + subCur.desc,
          score: cur.score + subCur.score,
          nums: inter,
        });
      }
    }
  }
  return result;
};

export const getGoodNums = (gbNums: GBData[], sex: Sex) => {
  const positiveNums: GBData[] = [];
  const negtiveNums: GBData[] = [];
  gbNums.forEach((data) => {
    if (!data.sex || data.sex === sex) {
      if (data.score < 0) {
        negtiveNums.push(data);
      } else {
        positiveNums.push(data);
      }
    }
  });
  const allNegtiveNums = sortedUniq(negtiveNums.map(({ nums }) => nums).flat());
  const sortedPositiveComposeNums = composeNums(
    positiveNums,
    0,
    allNegtiveNums
  ).sort((a, b) => b.score - a.score);

  const finalComposeNums: GBData[] = [];

  const cache: string[] = [];
  sortedPositiveComposeNums.forEach((obj) => {
    const cacheKey = JSON.stringify(obj.nums);
    if (!cache.includes(cacheKey)) {
      cache.push(cacheKey);
      finalComposeNums.push(obj);
    }
  });
  return finalComposeNums;
};

export function getNameScore(
  params: Record<"surnameData" | "secondNameData" | "lastnameData", CharData>
) {
  const { surnameData, secondNameData, lastnameData } = params;
  const surStks = surnameData.strokes;
  const secdStks = secondNameData.strokes;
  const lastStks = lastnameData.strokes;
  return {
    cosmos: surStks + 1,
    man: surStks + secdStks,
    earth: secdStks + lastStks,
    outside: lastStks + 1,
    total: surStks + secdStks + lastStks,
  };
}
