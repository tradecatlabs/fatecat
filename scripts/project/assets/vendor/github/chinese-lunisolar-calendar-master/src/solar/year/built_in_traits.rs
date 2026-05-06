use core::str::FromStr;

use super::{SolarOutOfRangeError, SolarYear, SolarYearError};

impl From<u16> for SolarYear {
    #[inline]
    fn from(value: u16) -> Self {
        SolarYear::from_u16(value)
    }
}

impl TryFrom<i32> for SolarYear {
    type Error = SolarOutOfRangeError;

    #[inline]
    fn try_from(value: i32) -> Result<Self, Self::Error> {
        Self::from_i32(value)
    }
}

impl FromStr for SolarYear {
    type Err = SolarYearError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}

impl From<SolarYear> for u16 {
    #[inline]
    fn from(value: SolarYear) -> Self {
        value.to_u16()
    }
}

impl From<SolarYear> for i32 {
    #[inline]
    fn from(value: SolarYear) -> Self {
        value.to_i32()
    }
}
