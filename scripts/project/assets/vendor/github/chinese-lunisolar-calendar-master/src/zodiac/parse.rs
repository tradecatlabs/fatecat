use super::{Zodiac, THE_ZODIAC_SIGNS};

/// 用以解析字串的關聯函數。
impl Zodiac {
    /// 透過鼠、牛、虎、兔、龍、蛇、馬、羊、猴、雞、狗、豬等字串來取得 `Zodiac` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::Zodiac;
    /// assert_eq!(Zodiac::Dragon, Zodiac::parse_str("龍").unwrap());
    /// assert_eq!(Zodiac::Dragon, Zodiac::parse_str("龙").unwrap());
    /// ```
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Option<Self> {
        let s = s.as_ref();

        for (i, t) in THE_ZODIAC_SIGNS.iter().enumerate() {
            if s == t.0 || s == t.1 {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }
        }

        None
    }
}
