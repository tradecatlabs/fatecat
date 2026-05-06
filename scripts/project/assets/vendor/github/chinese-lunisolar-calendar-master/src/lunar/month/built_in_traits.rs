use core::str::FromStr;

use super::{LunarMonth, LunarMonthError};

impl FromStr for LunarMonth {
    type Err = LunarMonthError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}
