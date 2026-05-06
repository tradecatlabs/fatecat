use core::str::FromStr;

use chrono::prelude::*;

use super::{SolarDate, SolarDateError, SolarOutOfRangeError};
use crate::{SolarDay, SolarMonth, SolarYear};

impl TryFrom<NaiveDate> for SolarDate {
    type Error = SolarOutOfRangeError;

    #[inline]
    fn try_from(value: NaiveDate) -> Result<Self, Self::Error> {
        Self::from_date(value)
    }
}

impl FromStr for SolarDate {
    type Err = SolarDateError;

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        SolarDate::parse_str(s)
    }
}

impl From<SolarDate> for NaiveDate {
    #[inline]
    fn from(value: SolarDate) -> Self {
        value.to_naive_date()
    }
}

impl From<SolarDate> for SolarYear {
    #[inline]
    fn from(value: SolarDate) -> Self {
        value.to_solar_year()
    }
}

impl From<SolarDate> for SolarMonth {
    #[inline]
    fn from(value: SolarDate) -> Self {
        value.to_solar_month()
    }
}

impl From<SolarDate> for SolarDay {
    #[inline]
    fn from(value: SolarDate) -> Self {
        value.to_solar_day()
    }
}
