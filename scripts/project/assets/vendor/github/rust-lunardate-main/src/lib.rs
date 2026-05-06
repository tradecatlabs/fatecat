// this file is derived from lunar project.
//
// lunar project:
//   Copyright (C) 1988,1989,1991,1992,2001 Fung F. Lee and Ricky Yeung
//   Licensed under GPLv2.
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software Foundation,
// Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//
use chrono::{Datelike, Duration, Local, NaiveDate};
use lazy_static::lazy_static;
use std::ops::{Add, Sub};
use std::{error, fmt, time};

lazy_static! {
    static ref START_DATE: NaiveDate = NaiveDate::from_ymd_opt(1900, 1, 31).unwrap();
    static ref YEAR_DAYS: Vec<u32> = {
        let mut days = Vec::with_capacity(150);
        for year_info in &YEAR_INFOS {
            days.push(year_info_to_year_day(*year_info));
        }
        days
    };
}

const YEAR_INFOS: [u32; 200] = [
    /* encoding:
                b bbbbbbbbbbbb bbbb
        bit#    1 111111000000 0000
                6 543210987654 3210
                . ............ ....
        month#    000000000111
                M 123456789012   L

    b_j = 1 for long month, b_j = 0 for short month
    L is the leap month of the year if 1<=L<=12; NO leap month if L = 0.
    The leap month (if exists) is long one iff M = 1.
    */
    0x04bd8, /* 1900 */
    0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, /* 1905 */
    0x16554, 0x056a0, 0x09ad0, 0x055d2, 0x04ae0, /* 1910 */
    0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, /* 1915 */
    0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970, /* 1920 */
    0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, /* 1925 */
    0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566, /* 1930 */
    0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, /* 1935 */
    0x186e3, 0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0, /* 1940 */
    0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, /* 1945 */
    0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0, /* 1950 */
    0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, /* 1955 */
    0x052d0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6, /* 1960 */
    0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, /* 1965 */
    0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0, /* 1970 */
    0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, /* 1975 */
    0x0d558, 0x0b540, 0x0b5a0, 0x195a6, 0x095b0, /* 1980 */
    0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, /* 1985 */
    0x06d40, 0x0af46, 0x0ab60, 0x09570, 0x04af5, /* 1990 */
    0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, /* 1995 */
    0x05ac0, 0x0ab60, 0x096d5, 0x092e0, 0x0c960, /* 2000 */
    0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, /* 2005 */
    0x0abb7, 0x025d0, 0x092d0, 0x0cab5, 0x0a950, /* 2010 */
    0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, /* 2015 */
    0x0a5b0, 0x15176, 0x052b0, 0x0a930, 0x07954, /* 2020 */
    0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, /* 2025 */
    0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, 0x05aa0, /* 2030 */
    0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, /* 2035 */
    0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0, /* 2040 */
    0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, /* 2045 */
    0x0aa50, 0x1b255, 0x06d20, 0x0ada0, 0x14b63, /* 2050 */
    0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, /* 2055 */
    0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0, 0x092e0, /* 2060 */
    0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, /* 2065 */
    0x05d55, 0x056a0, 0x0a6d0, 0x055d4, 0x052d0, /* 2070 */
    0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, /* 2075 */
    0x055a0, 0x0aba4, 0x0a5b0, 0x052b0, 0x0b273, /* 2080 */
    0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, /* 2085 */
    0x04b60, 0x0a570, 0x054e4, 0x0d160, 0x0e968, /* 2090 */
    0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, /* 2095 */
    0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252, /* 2099 */
];

/// `LunarDate` related errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
    /// Year out of range
    YearOutOfRange,
    /// Month out of range
    MonthOutOfRange,
    /// Day out of range
    DayOutOfRange,
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter) -> Result<(), fmt::Error> {
        match *self {
            Error::YearOutOfRange => write!(f, "year out of range"),
            Error::MonthOutOfRange => write!(f, "month out of range"),
            Error::DayOutOfRange => write!(f, "day out of range"),
        }
    }
}

impl error::Error for Error {
    fn description(&self) -> &str {
        match *self {
            Error::YearOutOfRange => "year out of range",
            Error::MonthOutOfRange => "month out of range",
            Error::DayOutOfRange => "day out of range",
        }
    }
}

fn year_info_to_year_day(year_info: u32) -> u32 {
    let mut res: u32 = 29 * 12;
    let mut leap = false;
    if year_info % 16 != 0 {
        leap = true;
        res += 29;
    }
    let mut year_info = year_info / 16;
    let inc = i32::from(leap);
    for _ in 0..(12 + inc) {
        if year_info % 2 == 1 {
            res += 1;
        }
        year_info /= 2;
    }
    res
}

fn enum_month(year: u32) -> Result<Vec<(u32, u32, bool)>, Error> {
    let mut months: Vec<(u32, bool)> = (1..13).map(|x| (x, false)).collect();
    let leap_month = year % 16;
    if leap_month == 0 {
    } else if leap_month <= 12 {
        months.insert(leap_month as usize, (leap_month, true));
    } else {
        return Err(Error::YearOutOfRange);
    }
    let mut ret = Vec::with_capacity(months.len());
    for (month, is_leap_month) in months {
        let days = if is_leap_month {
            (year >> 16) % 2 + 29
        } else {
            (year >> (16 - month)) % 2 + 29
        };
        ret.push((month, days, is_leap_month));
    }
    Ok(ret)
}

fn calc_month_day(year: u32, offset: u32) -> Result<(u32, u32, bool), Error> {
    let mut month = 0;
    let mut is_leap_month = false;
    let mut offset = offset;
    for (month_, days, leap_month) in enum_month(year)?.into_iter() {
        month = month_;
        is_leap_month = leap_month;
        if offset < days {
            break;
        }
        offset -= days;
    }
    Ok((month, offset + 1, is_leap_month))
}

fn calc_days(year_info: u32, month: u32, day: u32, is_leap_month: bool) -> Result<u32, Error> {
    let mut res = 0;
    for (_month, _days, leap_month) in enum_month(year_info)? {
        if _month == month && is_leap_month == leap_month {
            if day >= 1 && day <= _days {
                res += day - 1;
                return Ok(res);
            } else {
                return Err(Error::DayOutOfRange);
            }
        }
        res += _days;
    }
    Err(Error::MonthOutOfRange)
}

/// Represents a lunar date
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct LunarDate {
    year: i32,
    month: u32,
    day: u32,
    is_leap_month: bool,
}

impl LunarDate {
    /// Construct a new `LunarDate` struct
    #[inline]
    pub fn new(year: i32, month: u32, day: u32, is_leap_month: bool) -> Self {
        Self {
            year,
            month,
            day,
            is_leap_month,
        }
    }

    /// Construct a new `LunarDate` from solar date
    pub fn from_solar_date(year: i32, month: u32, day: u32) -> Result<Self, Error> {
        // TODO: the Error variant isn't a good choice, maybe add a new one?
        let solar_date = NaiveDate::from_ymd_opt(year, month, day).ok_or(Error::YearOutOfRange)?;
        Self::from_naive_date(&solar_date)
    }

    /// Construct a new `LunarDate` from `chrono`'s `NaiveDate`
    #[inline]
    pub fn from_naive_date(date: &NaiveDate) -> Result<Self, Error> {
        let offset = date.signed_duration_since(*START_DATE).num_days();
        Self::from_offset(offset as u32)
    }

    /// Return lunar year
    #[inline]
    pub fn year(&self) -> i32 {
        self.year
    }

    /// Return lunar month
    #[inline]
    pub fn month(&self) -> u32 {
        self.month
    }

    /// Return lunar day
    #[inline]
    pub fn day(&self) -> u32 {
        self.day
    }

    /// Is leap month?
    #[inline]
    pub fn is_leap_month(&self) -> bool {
        self.is_leap_month
    }

    /// Convert `LunarDate` to solar date
    pub fn to_solar_date(&self) -> Result<NaiveDate, Error> {
        let mut offset = 0;
        if self.year < 1900 || self.year >= 1900 + YEAR_INFOS.len() as i32 {
            return Err(Error::YearOutOfRange);
        }
        let year_index = self.year as usize - 1900;
        for i in 0..year_index {
            offset += YEAR_DAYS[i];
        }
        offset += calc_days(
            YEAR_INFOS[year_index],
            self.month,
            self.day,
            self.is_leap_month,
        )?;
        Ok(*START_DATE + Duration::days(offset as i64))
    }

    /// Return lunar date of solar date of today
    #[inline]
    pub fn today() -> Result<Self, Error> {
        let date = Local::now();
        Self::from_solar_date(date.year(), date.month(), date.day())
    }

    fn from_offset(offset: u32) -> Result<Self, Error> {
        let mut offset = offset;
        let mut index = 0;
        for (idx, year_day) in YEAR_DAYS.iter().enumerate() {
            index = idx;
            if offset < *year_day {
                break;
            }
            offset -= *year_day;
        }
        let year = 1900 + index;
        let year_info = YEAR_INFOS[index];
        let (month, day, is_leap_month) = calc_month_day(year_info, offset)?;
        Ok(LunarDate {
            year: year as i32,
            month,
            day,
            is_leap_month,
        })
    }

    /// Adds some duration to the current lunar date
    ///
    /// Returns `None` when it will result in overflow.
    pub fn checked_add(self, rhs: time::Duration) -> Option<LunarDate> {
        if let Ok(rhs) = Duration::from_std(rhs) {
            if let Ok(date) = self.to_solar_date() {
                return date
                    .checked_add_signed(rhs)
                    .and_then(|ref dt| LunarDate::from_naive_date(dt).ok());
            }
        }
        None
    }

    /// Subtracts some duration to the current lunar date
    ///
    /// Returns `None` when it will result in overflow.
    pub fn checked_sub(self, rhs: time::Duration) -> Option<LunarDate> {
        if let Ok(rhs) = Duration::from_std(rhs) {
            if let Ok(date) = self.to_solar_date() {
                return date
                    .checked_sub_signed(rhs)
                    .and_then(|ref dt| LunarDate::from_naive_date(dt).ok());
            }
        }
        None
    }
}

impl Add<Duration> for LunarDate {
    type Output = LunarDate;

    #[inline]
    fn add(self, rhs: Duration) -> Self::Output {
        let date = self.to_solar_date().unwrap() + rhs;
        LunarDate::from_naive_date(&date).unwrap()
    }
}

impl Add<time::Duration> for LunarDate {
    type Output = LunarDate;

    #[inline]
    fn add(self, rhs: time::Duration) -> Self::Output {
        self + Duration::from_std(rhs).unwrap()
    }
}

impl Sub<Duration> for LunarDate {
    type Output = LunarDate;

    #[inline]
    fn sub(self, rhs: Duration) -> Self::Output {
        let date = self.to_solar_date().unwrap() - rhs;
        LunarDate::from_naive_date(&date).unwrap()
    }
}

#[allow(clippy::suspicious_arithmetic_impl)]
impl Sub<time::Duration> for LunarDate {
    type Output = LunarDate;

    #[inline]
    fn sub(self, rhs: time::Duration) -> Self::Output {
        self + Duration::from_std(rhs).unwrap()
    }
}

impl Sub<LunarDate> for LunarDate {
    type Output = Duration;

    #[inline]
    fn sub(self, rhs: LunarDate) -> Self::Output {
        self.to_solar_date().unwrap() - rhs.to_solar_date().unwrap()
    }
}

impl Sub<NaiveDate> for LunarDate {
    type Output = Duration;

    #[inline]
    fn sub(self, rhs: NaiveDate) -> Self::Output {
        self.to_solar_date().unwrap() - rhs
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_solar_date() {
        let date = LunarDate::from_solar_date(1976, 10, 1).unwrap();
        assert_eq!(date, LunarDate::new(1976, 8, 8, true));
        assert_eq!(date.year(), 1976);
        assert_eq!(date.month(), 8);
        assert_eq!(date.day(), 8);
        assert!(date.is_leap_month());
    }

    #[test]
    fn test_to_solar_date() {
        let ld = LunarDate::new(1976, 8, 8, true);
        let sd = ld.to_solar_date().unwrap();
        assert_eq!(sd.year(), 1976);
        assert_eq!(sd.month(), 10);
        assert_eq!(sd.day(), 1);
    }

    #[test]
    fn test_before_leap_month() {
        let ld = LunarDate::from_solar_date(2017, 6, 28).unwrap();
        assert_eq!(ld.year(), 2017);
        assert_eq!(ld.month(), 6);
        assert_eq!(ld.day(), 5);
        assert_eq!(ld.is_leap_month(), false);
    }

    #[test]
    fn test_leap_month() {
        let ld = LunarDate::from_solar_date(2017, 7, 28).unwrap();
        assert_eq!(ld.year(), 2017);
        assert_eq!(ld.month(), 6);
        assert_eq!(ld.day(), 6);
        assert_eq!(ld.is_leap_month(), true);
    }

    #[test]
    fn test_after_leap_month() {
        let ld = LunarDate::from_solar_date(2017, 8, 28).unwrap();
        assert_eq!(ld.year(), 2017);
        assert_eq!(ld.month(), 7);
        assert_eq!(ld.day(), 7);
        assert_eq!(ld.is_leap_month(), false);
    }

    #[test]
    fn test_year_out_of_range() {
        let ld = LunarDate::new(2100, 1, 1, false);
        let sd = ld.to_solar_date();
        assert_eq!(sd, Err(Error::YearOutOfRange));
    }

    #[test]
    fn test_month_out_of_range() {
        let ld = LunarDate::new(2004, 13, 1, false);
        let sd = ld.to_solar_date();
        assert_eq!(sd, Err(Error::MonthOutOfRange));
    }

    #[test]
    fn test_day_out_of_range() {
        let ld = LunarDate::new(2004, 1, 30, false);
        let sd = ld.to_solar_date();
        assert_eq!(sd, Err(Error::DayOutOfRange));
    }
}
