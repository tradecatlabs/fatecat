use super::{LunisolarOutOfRangeError, LunisolarYear};
use crate::{EarthlyBranch, HeavenlyStems, LunarYear, SolarYear, Zodiac};

impl TryFrom<SolarYear> for LunisolarYear {
    type Error = LunisolarOutOfRangeError;

    #[inline]
    fn try_from(value: SolarYear) -> Result<Self, Self::Error> {
        Self::from_solar_year(value)
    }
}

impl From<LunisolarYear> for HeavenlyStems {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_heavenly_stems()
    }
}

impl From<LunisolarYear> for EarthlyBranch {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_earthly_branch()
    }
}

impl From<LunisolarYear> for Zodiac {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_zodiac()
    }
}

impl From<LunisolarYear> for LunarYear {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_lunar_year()
    }
}

impl From<LunisolarYear> for SolarYear {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_solar_year()
    }
}

impl From<LunisolarYear> for u16 {
    #[inline]
    fn from(value: LunisolarYear) -> Self {
        value.to_u16()
    }
}
