use core::str::FromStr;

use super::Zodiac;
use crate::EarthlyBranch;

impl TryFrom<char> for Zodiac {
    type Error = ();

    #[inline]
    fn try_from(value: char) -> Result<Self, Self::Error> {
        Self::from_char(value).ok_or(())
    }
}

impl From<EarthlyBranch> for Zodiac {
    #[inline]
    fn from(value: EarthlyBranch) -> Self {
        Self::from_earthly_branch(value)
    }
}

impl FromStr for Zodiac {
    type Err = ();

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s).ok_or(())
    }
}
