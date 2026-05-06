use core::str::FromStr;

use super::{LunarYear, LunarYearError};
use crate::{EarthlyBranch, HeavenlyStems, Zodiac};

impl FromStr for LunarYear {
    type Err = LunarYearError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s)
    }
}

impl From<LunarYear> for HeavenlyStems {
    #[inline]
    fn from(value: LunarYear) -> Self {
        value.to_heavenly_stems()
    }
}

impl From<LunarYear> for EarthlyBranch {
    #[inline]
    fn from(value: LunarYear) -> Self {
        value.to_earthly_branch()
    }
}

impl From<LunarYear> for Zodiac {
    #[inline]
    fn from(value: LunarYear) -> Self {
        value.to_zodiac()
    }
}

impl AsRef<str> for LunarYear {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
