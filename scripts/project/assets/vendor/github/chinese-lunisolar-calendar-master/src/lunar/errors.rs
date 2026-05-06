use core::fmt::{self, Display, Formatter};
#[cfg(feature = "std")]
use std::error::Error;

/// 錯誤的農曆年。
#[derive(Debug, Eq, PartialEq)]
pub struct LunarYearError;

impl Display for LunarYearError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the lunar year is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for LunarYearError {}

/// 錯誤的農曆月。
#[derive(Debug, Eq, PartialEq)]
pub struct LunarMonthError;

impl Display for LunarMonthError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the lunar date is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for LunarMonthError {}

/// 錯誤的農曆日。
#[derive(Debug, Eq, PartialEq)]
pub struct LunarDayError;

impl Display for LunarDayError {
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str("the lunar day is incorrect")
    }
}

#[cfg(feature = "std")]
impl Error for LunarDayError {}
