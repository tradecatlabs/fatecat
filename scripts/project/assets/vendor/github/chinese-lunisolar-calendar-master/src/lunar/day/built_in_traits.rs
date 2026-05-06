use core::str::FromStr;

use super::{LunarDay, LunarDayError};

impl TryFrom<u8> for LunarDay {
    type Error = LunarDayError;

    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Self::from_u8(value)
    }
}

impl FromStr for LunarDay {
    type Err = LunarDayError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}

impl From<LunarDay> for u8 {
    #[inline]
    fn from(value: LunarDay) -> Self {
        value.to_u8()
    }
}

impl AsRef<str> for LunarDay {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
