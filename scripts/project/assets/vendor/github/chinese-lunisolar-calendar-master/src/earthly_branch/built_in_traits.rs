use core::str::FromStr;

use chrono::prelude::*;

use super::EarthlyBranch;
use crate::Zodiac;

impl TryFrom<char> for EarthlyBranch {
    type Error = ();

    #[inline]
    fn try_from(value: char) -> Result<Self, Self::Error> {
        Self::from_char(value).ok_or(())
    }
}

impl From<Zodiac> for EarthlyBranch {
    #[inline]
    fn from(value: Zodiac) -> Self {
        Self::from_zodiac(value)
    }
}

impl From<NaiveTime> for EarthlyBranch {
    #[inline]
    fn from(value: NaiveTime) -> Self {
        Self::from_time(value)
    }
}

impl FromStr for EarthlyBranch {
    type Err = ();

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s).ok_or(())
    }
}

impl From<EarthlyBranch> for char {
    #[inline]
    fn from(value: EarthlyBranch) -> Self {
        value.to_char()
    }
}

impl AsRef<str> for EarthlyBranch {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
