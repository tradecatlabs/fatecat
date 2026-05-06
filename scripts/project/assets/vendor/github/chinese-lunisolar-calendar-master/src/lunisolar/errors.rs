use core::fmt::{self, Display, Formatter};
#[cfg(feature = "std")]
use std::error::Error;

use crate::{LunarDayError, LunarMonthError, LunarYearError};

/// 超出農曆支援的日期範圍。
#[derive(Debug, Eq, PartialEq)]
pub struct LunisolarOutOfRangeError;

impl Display for LunisolarOutOfRangeError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the lunisolar date is out of range")
    }
}

#[cfg(feature = "std")]
impl Error for LunisolarOutOfRangeError {}

/// 錯誤的農曆年月日。
#[derive(Debug, Eq, PartialEq)]
pub enum LunisolarDateError {
    OutOfRange,
    YearIncorrect,
    MonthIncorrect,
    DayIncorrect,
}

impl Display for LunisolarDateError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::OutOfRange => Display::fmt(&LunisolarOutOfRangeError, f),
            Self::YearIncorrect => Display::fmt(&LunarYearError, f),
            Self::MonthIncorrect => Display::fmt(&LunarMonthError, f),
            Self::DayIncorrect => Display::fmt(&LunarDayError, f),
        }
    }
}

impl From<LunisolarOutOfRangeError> for LunisolarDateError {
    #[inline]
    fn from(_: LunisolarOutOfRangeError) -> Self {
        Self::OutOfRange
    }
}

impl From<LunarYearError> for LunisolarDateError {
    #[inline]
    fn from(_: LunarYearError) -> Self {
        Self::YearIncorrect
    }
}

impl From<LunarMonthError> for LunisolarDateError {
    #[inline]
    fn from(_: LunarMonthError) -> Self {
        Self::MonthIncorrect
    }
}

impl From<LunarDayError> for LunisolarDateError {
    #[inline]
    fn from(_: LunarDayError) -> Self {
        Self::DayIncorrect
    }
}

#[cfg(feature = "std")]
impl Error for LunisolarDateError {}
