/**
 * 만세력(萬歲曆) 계산 라이브러리
 * Korean Saju (Four Pillars) and Manseryeok calculation library
 *
 * @author Yoohyojun
 * @license MIT
 */

// ===== 상수 정의 =====

/** 천간 (Heavenly Stems) */
export const HEAVENLY_STEMS = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계'] as const;

/** 천간 한자 */
export const HEAVENLY_STEMS_HANJA = [
  '甲',
  '乙',
  '丙',
  '丁',
  '戊',
  '己',
  '庚',
  '辛',
  '壬',
  '癸',
] as const;

/** 지지 (Earthly Branches) */
export const EARTHLY_BRANCHES = [
  '자',
  '축',
  '인',
  '묘',
  '진',
  '사',
  '오',
  '미',
  '신',
  '유',
  '술',
  '해',
] as const;

/** 지지 한자 */
export const EARTHLY_BRANCHES_HANJA = [
  '子',
  '丑',
  '寅',
  '卯',
  '辰',
  '巳',
  '午',
  '未',
  '申',
  '酉',
  '戌',
  '亥',
] as const;

/** 음양 (Yin/Yang) */
export const YIN_YANG = ['양', '음'] as const;

/** 오행 (Five Elements) */
export const FIVE_ELEMENTS = ['목', '화', '토', '금', '수'] as const;

// ===== 타입 정의 =====

export type HeavenlyStem = (typeof HEAVENLY_STEMS)[number];
export type EarthlyBranch = (typeof EARTHLY_BRANCHES)[number];
export type YinYang = (typeof YIN_YANG)[number];
export type FiveElement = (typeof FIVE_ELEMENTS)[number];

/** 사주의 한 기둥을 나타내는 인터페이스 */
export interface Pillar {
  heavenlyStem: HeavenlyStem;
  earthlyBranch: EarthlyBranch;
}

/** 사주팔자 전체를 나타내는 인터페이스 */
export interface FourPillars {
  year: Pillar; // 연주
  month: Pillar; // 월주
  day: Pillar; // 일주
  hour: Pillar; // 시주
}

/** 생년월일시 정보 */
export interface BirthInfo {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  isLunar?: boolean; // true면 음력, false/undefined면 양력
  isLeapMonth?: boolean; // 음력 윤달 여부
}

/** 음력 날짜 정보 */
export interface LunarDate {
  year: number;
  month: number;
  day: number;
  isLeapMonth: boolean;
}

/** 양력 날짜 정보 */
export interface SolarDate {
  year: number;
  month: number;
  day: number;
}

// ===== 음력 데이터 =====

/** 1900-2100년 음력 데이터 (출처: 한국천문연구원) */
const LUNAR_DATA = [
  0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2, 0x04ae0,
  0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970, 0x0a4b0,
  0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566, 0x0d4a0, 0x0ea50,
  0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0,
  0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0,
  0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260,
  0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558,
  0x0b540, 0x0b6a0, 0x195a6, 0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46,
  0x0ab60, 0x09570, 0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5,
  0x092e0, 0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
  0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930, 0x07954,
  0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, 0x05aa0, 0x076a3,
  0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0, 0x056d0, 0x055b2,
  0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0, 0x14b63, 0x09370, 0x049f8, 0x04970,
  0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0, 0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0,
  0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4, 0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50,
  0x055a0, 0x0aba4, 0x0a5b0, 0x052b0, 0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60,
  0x0a570, 0x054e4, 0x0d160, 0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0,
  0x0d150, 0x0f252, 0x0d520,
];

// ===== 음력 계산 관련 함수 =====

/** 음력 연도의 총 일수를 계산 */
const getLunarYearDays = (year: number): number => {
  let sum = 348; // 평년 기본 일수 (29.5 * 12 ≈ 354일에서 6일을 뺀 값)

  // 각 월의 대소월 여부를 비트 연산으로 확인
  for (let i = 0x8000; i > 0x8; i >>= 1) {
    sum += LUNAR_DATA[year - 1900] & i ? 1 : 0;
  }

  return sum + getLeapMonthDays(year);
};

/** 음력 연도의 윤달 위치를 반환 (0이면 윤달 없음) */
const getLeapMonth = (year: number): number => LUNAR_DATA[year - 1900] & 0xf;

/** 음력 연도의 윤달 일수를 반환 */
const getLeapMonthDays = (year: number): number => {
  const leapMonth = getLeapMonth(year);
  if (leapMonth) {
    return LUNAR_DATA[year - 1900] & 0x10000 ? 30 : 29;
  }
  return 0;
};

/** 음력 특정 월의 일수를 반환 */
const getLunarMonthDays = (year: number, month: number): number =>
  LUNAR_DATA[year - 1900] & (0x10000 >> month) ? 30 : 29;

// ===== 음력/양력 변환 함수 =====

/**
 * 음력을 양력으로 변환
 */
export function lunarToSolar(
  year: number,
  month: number,
  day: number,
  isLeapMonth: boolean,
): SolarDate {
  const baseDate = new Date(1900, 0, 31);
  let offset = 0;

  // 1900년부터 해당 연도까지의 일수 계산
  for (let i = 1900; i < year; i++) {
    offset += getLunarYearDays(i);
  }

  // 해당 연도의 월까지의 일수 계산
  const leapMonth = getLeapMonth(year);
  let isLeap = false;

  for (let i = 1; i < month; i++) {
    if (leapMonth > 0 && i === leapMonth && !isLeap) {
      offset += getLeapMonthDays(year);
      isLeap = true;
      i--;
    } else {
      offset += getLunarMonthDays(year, i);
    }
  }

  // 윤달인 경우 처리
  if (isLeapMonth && leapMonth === month) {
    offset += getLunarMonthDays(year, month);
  }

  // 일수 더하기
  offset += day - 1;

  const solarDate = new Date(baseDate.getTime() + offset * 86400000);
  return {
    year: solarDate.getFullYear(),
    month: solarDate.getMonth() + 1,
    day: solarDate.getDate(),
  };
}

/**
 * 양력을 음력으로 변환
 */
export function solarToLunar(year: number, month: number, day: number): LunarDate {
  const baseDate = new Date(1900, 0, 31);
  const targetDate = new Date(year, month - 1, day);
  const offset = Math.floor((targetDate.getTime() - baseDate.getTime()) / 86400000);

  let lunarYear = 1900;
  let remainingDays = offset;

  // 음력 연도 계산
  for (let i = 1900; i < 2100 && remainingDays > 0; i++) {
    const yearDays = getLunarYearDays(i);
    if (remainingDays < yearDays) {
      lunarYear = i;
      break;
    }
    remainingDays -= yearDays;
  }

  // 음력 월 계산
  const leapMonth = getLeapMonth(lunarYear);
  let lunarMonth = 1;
  let isLeapMonth = false;

  for (let i = 1; i <= 12 && remainingDays > 0; i++) {
    let monthDays: number;

    if (leapMonth > 0 && i === leapMonth + 1 && !isLeapMonth) {
      monthDays = getLeapMonthDays(lunarYear);
      isLeapMonth = true;
      i--;
    } else {
      monthDays = getLunarMonthDays(lunarYear, i);
      isLeapMonth = false;
    }

    if (remainingDays < monthDays) {
      lunarMonth = i;
      break;
    }
    remainingDays -= monthDays;
  }

  const lunarDay = remainingDays + 1;

  return { year: lunarYear, month: lunarMonth, day: lunarDay, isLeapMonth };
}

// ===== 절기 계산 =====

/** 절기 계산을 위한 기본 데이터 */
const SOLAR_TERM_BASE = [
  5.4055, 20.12, 3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83,
  7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94,
];

/**
 * 특정 절기의 날짜를 계산
 * @param year 연도
 * @param termIndex 절기 인덱스 (0-23)
 */
const getSolarTermDate = (year: number, termIndex: number): Date => {
  const century = Math.floor(year / 100);
  const yearInCentury = year % 100;

  const termCoeff = 0.2422;
  const leapYearAdjust = Math.floor(yearInCentury / 4) - Math.floor(century / 4);

  const day = Math.floor(SOLAR_TERM_BASE[termIndex] + termCoeff * yearInCentury + leapYearAdjust);

  const month = Math.floor(termIndex / 2);

  return new Date(year, month, day);
};

// ===== 사주 계산 함수들 =====

/**
 * 연주 계산
 */
const getYearPillar = (year: number): Pillar => ({
  heavenlyStem: HEAVENLY_STEMS[(year - 4) % 10],
  earthlyBranch: EARTHLY_BRANCHES[(year - 4) % 12],
});

/**
 * 월주 계산 (절기 기준)
 */
const getMonthPillar = (year: number, month: number, day: number): Pillar => {
  const date = new Date(year, month - 1, day);

  // 입춘 기준으로 연도 조정
  const lichunDate = getSolarTermDate(year, 2); // 입춘은 3번째 절기 (0-indexed)
  let adjustedYear = year;
  if (date < lichunDate) {
    adjustedYear = year - 1;
  }

  // 절기 기준으로 월 계산
  let solarTermMonth = 0;
  for (let i = 0; i < 24; i += 2) {
    const termDate = getSolarTermDate(adjustedYear, i);
    if (date >= termDate) {
      solarTermMonth = Math.floor(i / 2) + 1;
    } else {
      break;
    }
  }

  // 월주 천간 계산 (오행 순환 공식)
  const yearStem = (adjustedYear - 4) % 10;
  const yearStemMod5 = yearStem % 5;
  const monthStemIndex = (yearStemMod5 * 2 + solarTermMonth + 1) % 10;

  // 월주 지지 맵핑
  const MONTH_BRANCHES: Record<number, EarthlyBranch> = {
    1: '인',
    2: '묘',
    3: '진',
    4: '사',
    5: '오',
    6: '미',
    7: '신',
    8: '유',
    9: '술',
    10: '해',
    11: '자',
    12: '축',
  };

  return {
    heavenlyStem: HEAVENLY_STEMS[monthStemIndex],
    earthlyBranch: MONTH_BRANCHES[solarTermMonth] || '인',
  };
};

/**
 * 일주 계산 (60갑자 순환)
 */
const getDayPillar = (year: number, month: number, day: number): Pillar => {
  // 기준일: 1992년 10월 24일 = 계유일 (60갑자 9번)
  const BASE_DATE = new Date(1992, 9, 24);
  const BASE_GANJI_NUM = 9;

  const targetDate = new Date(year, month - 1, day);
  const daysDiff = Math.floor((targetDate.getTime() - BASE_DATE.getTime()) / 86400000);

  // 60갑자 순환 계산
  const targetGanjiNum = (((BASE_GANJI_NUM + daysDiff) % 60) + 60) % 60;

  return {
    heavenlyStem: HEAVENLY_STEMS[targetGanjiNum % 10],
    earthlyBranch: EARTHLY_BRANCHES[targetGanjiNum % 12],
  };
};

/**
 * 시주 계산
 *
 * 시간 체계:
 * - 자시(子時): 23:00-01:00
 * - 축시(丑時): 01:00-03:00
 * - 인시(寅時): 03:00-05:00
 * - 묘시(卯時): 05:00-07:00
 * - 진시(辰時): 07:00-09:00
 * - 사시(巳時): 09:00-11:00
 * - 오시(午時): 11:00-13:00
 * - 미시(未時): 13:00-15:00
 * - 신시(申時): 15:00-17:00
 * - 유시(酉時): 17:00-19:00
 * - 술시(戌時): 19:00-21:00
 * - 해시(亥時): 21:00-23:00
 *
 * 분(minute) 처리:
 * - 30분 이전: 해당 시진의 초반
 * - 30분 이후: 다음 시진으로 넘어가는 경계
 * - 예: 5시 30분은 묘시의 중반으로 처리
 */
const getHourPillar = (dayPillar: Pillar, hour: number, minute: number): Pillar => {
  // 시간을 12지지 시간으로 변환 (분 고려)
  let adjustedHour = hour;

  // 23시는 자시로 처리
  if (hour === 23) {
    adjustedHour = 0;
  }

  // 정확한 시진 계산 (분을 고려하여 보정)
  // 각 시진은 2시간이므로, 중간점인 정각 이후 1시간이 지나면 다음 시진에 가까워짐
  const totalMinutes = adjustedHour * 60 + minute;
  const shichen = Math.floor((totalMinutes + 60) / 120) % 12;

  // 일간에 따른 시간 천간 계산 (일간 기준 오행 순환)
  const dayStemIndex = HEAVENLY_STEMS.indexOf(dayPillar.heavenlyStem);
  const hourStemBase = (dayStemIndex % 5) * 2;
  const hourStemIndex = (hourStemBase + shichen) % 10;

  return {
    heavenlyStem: HEAVENLY_STEMS[hourStemIndex],
    earthlyBranch: EARTHLY_BRANCHES[shichen],
  };
};

// ===== 메인 계산 함수 =====

/** 사주 계산 결과 상세 정보 */
export interface FourPillarsDetail extends FourPillars {
  // 각 기둥의 음양오행 (stem: 천간의 오행, branch: 지지의 오행)
  yearElement: { stem: FiveElement; branch: FiveElement };
  monthElement: { stem: FiveElement; branch: FiveElement };
  dayElement: { stem: FiveElement; branch: FiveElement };
  hourElement: { stem: FiveElement; branch: FiveElement };

  // 각 기둥의 음양 (stem: 천간의 음양, branch: 지지의 음양)
  yearYinYang: { stem: YinYang; branch: YinYang };
  monthYinYang: { stem: YinYang; branch: YinYang };
  dayYinYang: { stem: YinYang; branch: YinYang };
  hourYinYang: { stem: YinYang; branch: YinYang };

  // 문자열 표현
  toString: () => string;
  toObject: () => {
    year: string;
    month: string;
    day: string;
    hour: string;
  };

  // 개별 기둥 문자열 (한글)
  yearString: string;
  monthString: string;
  dayString: string;
  hourString: string;

  // 개별 기둥 한자
  yearHanja: string;
  monthHanja: string;
  dayHanja: string;
  hourHanja: string;

  // 한자 포함 객체
  toHanjaObject: () => {
    year: { korean: string; hanja: string };
    month: { korean: string; hanja: string };
    day: { korean: string; hanja: string };
    hour: { korean: string; hanja: string };
  };

  // 한자 문자열
  toHanjaString: () => string;
}

/**
 * 사주팔자를 계산합니다.
 *
 * @param birthInfo 생년월일시 정보
 * @returns 사주팔자 (연주, 월주, 일주, 시주)
 */
export function calculateFourPillars(birthInfo: BirthInfo): FourPillarsDetail {
  const { hour, minute } = birthInfo;
  let { year, month, day } = birthInfo;

  // 음력인 경우 양력으로 변환
  if (birthInfo.isLunar) {
    const solarDate = lunarToSolar(year, month, day, birthInfo.isLeapMonth || false);
    year = solarDate.year;
    month = solarDate.month;
    day = solarDate.day;
  }

  const yearPillar = getYearPillar(year);
  const monthPillar = getMonthPillar(year, month, day);
  const dayPillar = getDayPillar(year, month, day);
  const hourPillar = getHourPillar(dayPillar, hour, minute);

  return {
    year: yearPillar,
    month: monthPillar,
    day: dayPillar,
    hour: hourPillar,

    // 오행 정보
    yearElement: {
      stem: getHeavenlyStemElement(yearPillar.heavenlyStem),
      branch: getEarthlyBranchElement(yearPillar.earthlyBranch),
    },
    monthElement: {
      stem: getHeavenlyStemElement(monthPillar.heavenlyStem),
      branch: getEarthlyBranchElement(monthPillar.earthlyBranch),
    },
    dayElement: {
      stem: getHeavenlyStemElement(dayPillar.heavenlyStem),
      branch: getEarthlyBranchElement(dayPillar.earthlyBranch),
    },
    hourElement: {
      stem: getHeavenlyStemElement(hourPillar.heavenlyStem),
      branch: getEarthlyBranchElement(hourPillar.earthlyBranch),
    },

    // 음양 정보
    yearYinYang: {
      stem: getHeavenlyStemYinYang(yearPillar.heavenlyStem),
      branch: getEarthlyBranchYinYang(yearPillar.earthlyBranch),
    },
    monthYinYang: {
      stem: getHeavenlyStemYinYang(monthPillar.heavenlyStem),
      branch: getEarthlyBranchYinYang(monthPillar.earthlyBranch),
    },
    dayYinYang: {
      stem: getHeavenlyStemYinYang(dayPillar.heavenlyStem),
      branch: getEarthlyBranchYinYang(dayPillar.earthlyBranch),
    },
    hourYinYang: {
      stem: getHeavenlyStemYinYang(hourPillar.heavenlyStem),
      branch: getEarthlyBranchYinYang(hourPillar.earthlyBranch),
    },

    // 문자열 표현 (한글)
    yearString: `${yearPillar.heavenlyStem}${yearPillar.earthlyBranch}`,
    monthString: `${monthPillar.heavenlyStem}${monthPillar.earthlyBranch}`,
    dayString: `${dayPillar.heavenlyStem}${dayPillar.earthlyBranch}`,
    hourString: `${hourPillar.heavenlyStem}${hourPillar.earthlyBranch}`,

    // 한자 표현
    yearHanja: `${HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.indexOf(yearPillar.heavenlyStem)]}${EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.indexOf(yearPillar.earthlyBranch)]}`,
    monthHanja: `${HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.indexOf(monthPillar.heavenlyStem)]}${EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.indexOf(monthPillar.earthlyBranch)]}`,
    dayHanja: `${HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.indexOf(dayPillar.heavenlyStem)]}${EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.indexOf(dayPillar.earthlyBranch)]}`,
    hourHanja: `${HEAVENLY_STEMS_HANJA[HEAVENLY_STEMS.indexOf(hourPillar.heavenlyStem)]}${EARTHLY_BRANCHES_HANJA[EARTHLY_BRANCHES.indexOf(hourPillar.earthlyBranch)]}`,

    toString: function (): string {
      return `${this.yearString}년주, ${this.monthString}월주, ${this.dayString}일주, ${this.hourString}시주`;
    },

    toObject: function (): { year: string; month: string; day: string; hour: string } {
      return {
        year: this.yearString,
        month: this.monthString,
        day: this.dayString,
        hour: this.hourString,
      };
    },

    toHanjaObject: function (): {
      year: { korean: string; hanja: string };
      month: { korean: string; hanja: string };
      day: { korean: string; hanja: string };
      hour: { korean: string; hanja: string };
    } {
      return {
        year: { korean: this.yearString, hanja: this.yearHanja },
        month: { korean: this.monthString, hanja: this.monthHanja },
        day: { korean: this.dayString, hanja: this.dayHanja },
        hour: { korean: this.hourString, hanja: this.hourHanja },
      };
    },

    toHanjaString: function (): string {
      return `${this.yearHanja}年柱, ${this.monthHanja}月柱, ${this.dayHanja}日柱, ${this.hourHanja}時柱`;
    },
  };
}

/**
 * 사주를 한국어 문자열로 변환합니다.
 *
 * @param fourPillars 사주팔자
 * @returns "임신연주, 경술월주, 계유일주, 을묘시주" 형식의 문자열
 */
export function fourPillarsToString(fourPillars: FourPillars): string {
  const { year, month, day, hour } = fourPillars;
  return [
    `${year.heavenlyStem}${year.earthlyBranch}연주`,
    `${month.heavenlyStem}${month.earthlyBranch}월주`,
    `${day.heavenlyStem}${day.earthlyBranch}일주`,
    `${hour.heavenlyStem}${hour.earthlyBranch}시주`,
  ].join(', ');
}

// ===== 음양오행 관련 함수 =====

/**
 * 천간의 음양을 반환합니다.
 */
export function getHeavenlyStemYinYang(stem: HeavenlyStem): YinYang {
  const index = HEAVENLY_STEMS.indexOf(stem);
  return index % 2 === 0 ? '양' : '음';
}

/**
 * 천간의 오행을 반환합니다.
 */
export function getHeavenlyStemElement(stem: HeavenlyStem): FiveElement {
  // noinspection NonAsciiCharacters
  const STEM_ELEMENTS: Record<HeavenlyStem, FiveElement> = {
    갑: '목',
    을: '목',
    병: '화',
    정: '화',
    무: '토',
    기: '토',
    경: '금',
    신: '금',
    임: '수',
    계: '수',
  };
  return STEM_ELEMENTS[stem];
}

/**
 * 지지의 오행을 반환합니다.
 */
export function getEarthlyBranchElement(branch: EarthlyBranch): FiveElement {
  // noinspection NonAsciiCharacters
  const BRANCH_ELEMENTS: Record<EarthlyBranch, FiveElement> = {
    자: '수',
    해: '수',
    인: '목',
    묘: '목',
    사: '화',
    오: '화',
    진: '토',
    술: '토',
    축: '토',
    미: '토',
    신: '금',
    유: '금',
  };
  return BRANCH_ELEMENTS[branch];
}

/**
 * 지지의 음양을 반환합니다.
 */
export function getEarthlyBranchYinYang(branch: EarthlyBranch): YinYang {
  const index = EARTHLY_BRANCHES.indexOf(branch);
  return index % 2 === 0 ? '양' : '음';
}
