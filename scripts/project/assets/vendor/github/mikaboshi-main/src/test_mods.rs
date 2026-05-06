/**
 * Modules used ONLY from tests.
 */
use chrono::naive::{NaiveDate, NaiveDateTime};
use serde::{Deserialize, Serialize};
use std::convert::From;

#[derive(
    Serialize, Deserialize, Debug, Copy, Clone,
)]
pub struct DateParams {
    pub year: i32,
    pub month: u32,
    pub day: u32,
}

impl From<DateParams> for NaiveDate {
    fn from(params: DateParams) -> Self {
        NaiveDate::from_ymd(
            params.year,
            params.month,
            params.day,
        )
    }
}

#[derive(
    Serialize, Deserialize, Debug, Copy, Clone,
)]
pub struct DateTimeParams {
    pub year: i32,
    pub month: u32,
    pub day: u32,
    pub hour: u32,
    pub minute: u32,
    pub second: u32,
    pub nanosecond: u32,
    pub zone: i32,
}

impl From<DateTimeParams> for NaiveDateTime {
    fn from(params: DateTimeParams) -> Self {
        NaiveDate::from_ymd(
            params.year,
            params.month,
            params.day,
        )
        .and_hms(
            params.hour,
            params.minute,
            params.second,
        )
    }
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct XiaGuaTuParams {
    pub unpan_xing_center: usize,
    pub unpan_xing_order: Vec<usize>,
    pub xiang_xing_direction: String,
    pub xiang_xing_sector: usize,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct ShengSiParams {
    pub unpan_id: usize,
    pub unpan_xing_chart: Vec<usize>,
}
