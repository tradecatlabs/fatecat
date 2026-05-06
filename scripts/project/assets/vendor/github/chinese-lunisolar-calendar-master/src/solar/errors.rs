use core::fmt::{self, Display, Formatter};
#[cfg(feature = "std")]
use std::error::Error;

/// 超出西曆支援的日期範圍。
#[derive(Debug, Eq, PartialEq)]
pub struct SolarOutOfRangeError;

impl Display for SolarOutOfRangeError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the solar date is out of range")
    }
}

#[cfg(feature = "std")]
impl Error for SolarOutOfRangeError {}

/// 錯誤的西曆年。
#[derive(Debug, Eq, PartialEq)]
pub struct SolarYearError;

impl Display for SolarYearError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the solar year is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for SolarYearError {}

/// 錯誤的西曆月。
#[derive(Debug, Eq, PartialEq)]
pub struct SolarMonthError;

impl Display for SolarMonthError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the solar date is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for SolarMonthError {}

/// 錯誤的西曆日。
#[derive(Debug, Eq, PartialEq)]
pub struct SolarDayError;

impl Display for SolarDayError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the solar day is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for SolarDayError {}

/// 錯誤的西曆年月日。
#[derive(Debug, Eq, PartialEq)]
pub enum SolarDateError {
    OutOfRange,
    YearIncorrect,
    MonthIncorrect,
    DayIncorrect,
}

impl Display for SolarDateError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::OutOfRange => Display::fmt(&SolarOutOfRangeError, f),
            Self::YearIncorrect => Display::fmt(&SolarYearError, f),
            Self::MonthIncorrect => Display::fmt(&SolarMonthError, f),
            Self::DayIncorrect => Display::fmt(&SolarDayError, f),
        }
    }
}

impl From<SolarOutOfRangeError> for SolarDateError {
    #[inline]
    fn from(_: SolarOutOfRangeError) -> Self {
        Self::OutOfRange
    }
}

impl From<SolarYearError> for SolarDateError {
    #[inline]
    fn from(_: SolarYearError) -> Self {
        Self::YearIncorrect
    }
}

impl From<SolarMonthError> for SolarDateError {
    #[inline]
    fn from(_: SolarMonthError) -> Self {
        Self::MonthIncorrect
    }
}

impl From<SolarDayError> for SolarDateError {
    #[inline]
    fn from(_: SolarDayError) -> Self {
        Self::DayIncorrect
    }
}

#[cfg(feature = "std")]
impl Error for SolarDateError {}
