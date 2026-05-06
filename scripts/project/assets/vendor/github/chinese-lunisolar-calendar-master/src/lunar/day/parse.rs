use super::{LunarDay, LunarDayError, THE_LUNAR_DAYS};

/// 用以解析字串的關聯函數。
impl LunarDay {
    /// 透過農曆日期字串來取得 `LunarDay` 列舉實體。
    #[inline]
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, LunarDayError> {
        let s = s.as_ref();

        for (i, &t) in THE_LUNAR_DAYS.iter().enumerate() {
            if s == t {
                return Ok(unsafe { Self::from_u8_unsafe(i as u8 + 1) });
            }
        }

        Err(LunarDayError)
    }
}
