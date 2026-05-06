use super::{SolarMonth, SolarMonthError, THE_SOLAR_MONTHS};

/// 用以解析字串的關聯函數。
impl SolarMonth {
    /// 透過西曆月份字串來取得 `SolarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarMonth;
    /// assert_eq!(SolarMonth::May, SolarMonth::parse_str("五月").unwrap());
    /// ```
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, SolarMonthError> {
        let s = s.as_ref();

        for (i, &t) in THE_SOLAR_MONTHS.iter().enumerate() {
            if s == t {
                return Ok(unsafe { Self::from_u8_unsafe(i as u8 + 1) });
            }
        }

        Err(SolarMonthError)
    }
}
