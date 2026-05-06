use core::str::FromStr;

use chrono::prelude::*;

use super::{LunisolarDate, LunisolarDateError, LunisolarOutOfRangeError};
use crate::{LunarDay, LunarMonth, LunarYear, LunisolarYear, SolarDate, SolarYear};

impl TryFrom<SolarDate> for LunisolarDate {
    type Error = LunisolarOutOfRangeError;

    #[inline]
    fn try_from(value: SolarDate) -> Result<Self, Self::Error> {
        Self::from_solar_date(value)
    }
}

impl TryFrom<NaiveDate> for LunisolarDate {
    type Error = LunisolarOutOfRangeError;

    #[inline]
    fn try_from(value: NaiveDate) -> Result<Self, Self::Error> {
        Self::from_date(value)
    }
}

impl FromStr for LunisolarDate {
    type Err = LunisolarDateError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        LunisolarDate::parse_str(s)
    }
}

impl From<LunisolarDate> for SolarDate {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_solar_date()
    }
}

impl From<LunisolarDate> for NaiveDate {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_naive_date()
    }
}

impl From<LunisolarDate> for SolarYear {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_solar_year()
    }
}

impl From<LunisolarDate> for LunisolarYear {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_lunisolar_year()
    }
}

impl From<LunisolarDate> for LunarYear {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_lunar_year()
    }
}

impl From<LunisolarDate> for LunarMonth {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_lunar_month()
    }
}

impl From<LunisolarDate> for LunarDay {
    #[inline]
    fn from(value: LunisolarDate) -> Self {
        value.to_lunar_day()
    }
}
