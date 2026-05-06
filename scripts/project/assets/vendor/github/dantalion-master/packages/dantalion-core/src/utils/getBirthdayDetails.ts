/** Details for a month. */
export interface MonthDetails {
  /**
   * Gets 1 if it is January and 0 otherwise.
   * @param febrary Specifies whether to return 1 even in February.
   *
   * If ommited, it's `true`.
   */
  early(febrary?: boolean): number;
  /** The month. */
  month: number;
  /**
   * It contains the month from 3 to 14, with January replaced by 13 and
   * February moved by 14.
   */
  shifted: number;
}

/** Details for a year. */
export interface YearDetails {
  /** A year with four digits. */
  full: number;
  /** Upper two digits of the year */
  hi: number;
  /** Lower two digits of the year */
  lo: number;
}

/** Details for the birthday. */
export interface BirthdayDetails {
  /** A date of the birthday. */
  date: number;
  /** Details for a month. */
  month: MonthDetails;
  /** Details for a year. */
  year: YearDetails;
}

/**
 * Calculate the details of the birthday.
 * @param date Birthday.
 */
export default (date: Date): BirthdayDetails => {
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  const early: MonthDetails['early'] = (containFebrary = true) =>
    month === 1 || (month === 2 && containFebrary) ? 1 : 0;
  return {
    date: date.getDate(),
    month: { early, month, shifted: month + early() * 12 },
    year: { full: year, hi: Math.floor(year * 0.01), lo: year % 100 },
  };
};
