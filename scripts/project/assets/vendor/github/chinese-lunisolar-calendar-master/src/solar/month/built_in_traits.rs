use core::str::FromStr;

use super::{SolarMonth, SolarMonthError};

impl TryFrom<u8> for SolarMonth {
    type Error = SolarMonthError;

    #[inline]
    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Self::from_u8(value)
    }
}

impl TryFrom<u32> for SolarMonth {
    type Error = SolarMonthError;

    #[inline]
    fn try_from(value: u32) -> Result<Self, Self::Error> {
        Self::from_u32(value)
    }
}

impl FromStr for SolarMonth {
    type Err = SolarMonthError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}

impl From<SolarMonth> for u8 {
    #[inline]
    fn from(value: SolarMonth) -> Self {
        value.to_u8()
    }
}

impl From<SolarMonth> for u32 {
    #[inline]
    fn from(value: SolarMonth) -> Self {
        value.to_u32()
    }
}

impl AsRef<str> for SolarMonth {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
