use super::{EarthlyBranch, THE_EARTHLY_BRANCHES};

/// 用以解析字串的關聯函數。
impl EarthlyBranch {
    /// 透過子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥等字串來取得 `EarthlyBranch` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!(EarthlyBranch::Fifth, EarthlyBranch::parse_str("辰").unwrap());
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Option<Self> {
        let s = s.as_ref();

        for (i, &t) in THE_EARTHLY_BRANCHES.iter().enumerate() {
            if s == t {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }
        }

        None
    }
}
