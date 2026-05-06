import { LunarHour } from "tyme4ts";

import type { ZiWeiRuntime } from "../context";
import type {
  CreateZiWeiLunisolarParams,
  CreateZiWeiSolarParams,
  NatalByStemBranchCalculateParams,
} from "../typings";

import { _calculateNatalByStemBranch, calculateNatal } from "../services/natal";
import {
  calculateHourByIndex,
  calculateLunisolarDateBySolar,
  calculateNatalDateBySolar,
  calculateZiWeiDate,
} from "../utils/calendar";
import { getLunisolarDateText, getSolarDateText } from "../utils/format";
import { normalizeDateByTimezone } from "../utils/timezone";
import { calculateTrueSolarTime } from "../utils/trueSolarTime";

export const calculateNatalBySolar =
  (params: CreateZiWeiSolarParams) => (runtime: ZiWeiRuntime) => {
    const {
      name,
      gender,
      date,
      language,
      longitude,
      useTrueSolarTime = true,
      timezone = 8,
      referenceDate,
    } = params;
    if (language) runtime.i18n.setCurrentLanguage(language);

    const globalConfigs = runtime.configs;
    const normalizedDate = normalizeDateByTimezone(date, timezone);
    let currentSolarDate: Date = normalizedDate;

    const trueSolarTime = calculateTrueSolarTime(normalizedDate, longitude ?? 116.38333, timezone);

    if (useTrueSolarTime) {
      currentSolarDate = trueSolarTime;
    }

    const lunarHour = calculateLunisolarDateBySolar(currentSolarDate);
    const { stemKey, branchKey, monthIndex, day, hourIndex } = calculateNatalDateBySolar({
      date: lunarHour,
      globalConfigs,
    });

    return calculateNatal(
      runtime,
      {
        name,
        gender,
        monthIndex,
        day,
        hourIndex,
        birthYear: lunarHour.getYear(),
        birthYearStemKey: stemKey,
        birthYearBranchKey: branchKey,
        solarDate: getSolarDateText(normalizedDate),
        solarDateByTrue: useTrueSolarTime ? getSolarDateText(currentSolarDate) : undefined,
        lunisolarDate: getLunisolarDateText(lunarHour, hourIndex, runtime.i18n),
        sexagenaryCycleDate: lunarHour.getEightChar().toString(),
      },
      referenceDate,
    );
  };

export const calculateNatalByLunisolar =
  ({ name, gender, date, language, referenceDate }: CreateZiWeiLunisolarParams) =>
  (runtime: ZiWeiRuntime) => {
    if (language) runtime.i18n.setCurrentLanguage(language);
    const [year, month, days, currentHourIndex] = date.split("-").map(Number);
    const [hour, minute, second] = calculateHourByIndex(currentHourIndex);
    const lunarHour = LunarHour.fromYmdHms(year, month, days, hour, minute, second);
    const solarTime = lunarHour.getSolarTime();
    const { stemKey, branchKey, monthIndex, day, hourIndex } = calculateZiWeiDate(date);

    return calculateNatal(
      runtime,
      {
        name,
        gender,
        monthIndex,
        day,
        hourIndex,
        birthYear: lunarHour.getYear(),
        birthYearStemKey: stemKey,
        birthYearBranchKey: branchKey,
        solarDate: getSolarDateText(solarTime),
        solarDateByTrue: undefined,
        lunisolarDate: getLunisolarDateText(lunarHour, hourIndex, runtime.i18n),
        sexagenaryCycleDate: lunarHour.getEightChar().toString(),
      },
      referenceDate,
    );
  };

export const calculateNatalByStemBranch =
  ({
    birthYearStemKey,
    branchKey,
    mainPalaceBranchKey,
    language,
  }: NatalByStemBranchCalculateParams) =>
  (runtime: ZiWeiRuntime) => {
    if (language) runtime.i18n.setCurrentLanguage(language);
    // 根据指定的地支位置来计算星辰排列
    return _calculateNatalByStemBranch(runtime, {
      birthYearStemKey,
      branchKey,
      mainPalaceBranchKey,
    });
  };
