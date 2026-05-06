use super::{SolarDay, SolarDayError, THE_SOLAR_DAYS};

/// 用以解析字串的關聯函數。
impl SolarDay {
    /// 透過西曆日期字串來取得 `SolarDay` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDay;
    /// assert_eq!(SolarDay::Fifteen, SolarDay::parse_str("十五").unwrap());
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, SolarDayError> {
        let s = s.as_ref();

        for (i, &t) in THE_SOLAR_DAYS.iter().enumerate() {
            if s == t {
                return Ok(unsafe { Self::from_u8_unsafe(i as u8 + 1) });
            }
        }

        Err(SolarDayError)
    }
}
