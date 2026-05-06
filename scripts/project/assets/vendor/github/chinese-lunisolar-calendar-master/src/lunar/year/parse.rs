use super::{LunarYear, LunarYearError, THE_LUNAR_YEARS};

/// 用以解析字串的關聯函數。
impl LunarYear {
    /// 透過農曆年份字串來取得 `LunarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year = LunarYear::parse_str("戊戌").unwrap();
    ///
    /// assert_eq!(HeavenlyStems::Fifth, lunar_year.to_heavenly_stems());
    /// assert_eq!(EarthlyBranch::Eleventh, lunar_year.to_earthly_branch());
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, LunarYearError> {
        let s = s.as_ref();

        for (i, &t) in THE_LUNAR_YEARS.iter().enumerate() {
            if s == t {
                return Ok(LunarYear(i as u8));
            }
        }

        Err(LunarYearError)
    }
}
