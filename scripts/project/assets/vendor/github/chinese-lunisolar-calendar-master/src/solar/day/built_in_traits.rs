use core::str::FromStr;

use super::{SolarDay, SolarDayError};

impl TryFrom<u8> for SolarDay {
    type Error = SolarDayError;

    #[inline]
    fn try_from(value: u8) -> Result<Self, Self::Error> {
        Self::from_u8(value)
    }
}

impl TryFrom<u32> for SolarDay {
    type Error = SolarDayError;

    #[inline]
    fn try_from(value: u32) -> Result<Self, Self::Error> {
        Self::from_u32(value)
    }
}

impl FromStr for SolarDay {
    type Err = SolarDayError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}

impl From<SolarDay> for u8 {
    #[inline]
    fn from(value: SolarDay) -> Self {
        value.to_u8()
    }
}

impl From<SolarDay> for u32 {
    #[inline]
    fn from(value: SolarDay) -> Self {
        value.to_u32()
    }
}

impl AsRef<str> for SolarDay {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
