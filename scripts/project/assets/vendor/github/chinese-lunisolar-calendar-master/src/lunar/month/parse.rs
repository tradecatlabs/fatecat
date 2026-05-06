use super::{LunarMonth, LunarMonthError, THE_LUNAR_MONTHS};

/// 用以解析字串的關聯函數。
impl LunarMonth {
    /// 透過農曆月份字串來取得 `LunarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::LunarMonth;
    ///
    /// assert_eq!(LunarMonth::Twelfth, LunarMonth::parse_str("臘月").unwrap());
    /// assert_eq!(
    ///     LunarMonth::LeapTwelfth,
    ///     LunarMonth::parse_str("闰腊月").unwrap()
    /// );
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, LunarMonthError> {
        let s = s.as_ref();

        for (i, t) in THE_LUNAR_MONTHS.iter().enumerate().take(24) {
            if s == t.0 || s == t.1 {
                return if i >= 12 {
                    Ok(unsafe { Self::from_u8_raw_unsafe((i as u8 - 12) + 101) })
                } else {
                    Ok(unsafe { Self::from_u8_raw_unsafe(i as u8 + 1) })
                };
            }
        }

        macro_rules! extra {
            ($i:expr, $variant:ident) => {{
                let t = THE_LUNAR_MONTHS[$i];

                if s == t.0 || s == t.1 {
                    return Ok(LunarMonth::$variant);
                }
            }};
        }

        extra!(24, First);
        extra!(25, Eleventh);
        extra!(26, Twelfth);
        extra!(27, LeapFirst);
        extra!(28, LeapEleventh);
        extra!(29, LeapTwelfth);
        extra!(30, LeapTwelfth);

        Err(LunarMonthError)
    }
}
