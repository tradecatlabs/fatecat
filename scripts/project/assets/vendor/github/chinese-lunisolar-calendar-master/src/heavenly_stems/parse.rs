use super::{HeavenlyStems, THE_HEAVENLY_STEMS};

/// 用以解析字串的關聯函數。
impl HeavenlyStems {
    /// 透過甲、乙、丙、丁、戊、己、更、辛、壬、葵等字串來取得 `HeavenlyStems` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::HeavenlyStems;
    /// assert_eq!(HeavenlyStems::Fifth, HeavenlyStems::parse_str("戊").unwrap());
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Option<Self> {
        let s = s.as_ref();

        for (i, &t) in THE_HEAVENLY_STEMS.iter().enumerate() {
            if s == t {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }
        }

        None
    }
}
