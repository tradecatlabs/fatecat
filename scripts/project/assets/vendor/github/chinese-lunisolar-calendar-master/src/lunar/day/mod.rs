#[cfg(feature = "ba-zi-weight")]
mod ba_zi_weight;
mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::THE_LUNAR_DAYS;
use enum_ordinalize::Ordinalize;

use super::LunarDayError;

/// 列舉農曆三十個天數名稱：初一、初二、...、十一、十二、...、廿一、廿二、...、三十。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_u8_unsafe,
    doc = "透過農曆日期數值來取得 `LunarDay` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn to_u8, doc = "取得 `LunarDay` 列舉實體所代表的農曆日期字串。"))]
#[repr(u8)]
pub enum LunarDay {
    /// 初一
    First = 1,
    /// 初二
    Second,
    /// 初三
    Third,
    /// 初四
    Fourth,
    /// 初五
    Fifth,
    /// 初六
    Sixth,
    /// 初七
    Seventh,
    /// 初八
    Eighth,
    /// 初九
    Ninth,
    /// 初十
    Tenth,
    /// 十一
    Eleventh,
    /// 十二
    Twelfth,
    /// 十三
    Thirteen,
    /// 十四
    Fourteen,
    /// 十五
    Fifteen,
    /// 十六
    Sixteen,
    /// 十七
    Seventeen,
    /// 十八
    Eighteen,
    /// 十九
    Nineteen,
    /// 二十
    Twenty,
    /// 廿一
    TwentyFirst,
    /// 廿二
    TwentySecond,
    /// 廿三
    TwentyThird,
    /// 廿四
    TwentyFourth,
    /// 廿五
    TwentyFifth,
    /// 廿六
    TwentySixth,
    /// 廿七
    TwentySeventh,
    /// 廿八
    TwentyEighth,
    /// 廿九
    TwentyNinth,
    /// 三十
    Thirty,
}

impl Display for LunarDay {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunarDay;
    /// assert_eq!("初七", format!("{}", LunarDay::Seventh));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `LunarDay` 列舉實體的關聯函數。
impl LunarDay {
    /// 透過農曆日期數值來取得 `LunarDay` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunarDay;
    /// assert_eq!(LunarDay::Seventh, LunarDay::from_u8(7).unwrap());
    /// ```
    #[inline]
    pub const fn from_u8(day: u8) -> Result<Self, LunarDayError> {
        if day >= 1 && day <= 30 {
            Ok(unsafe { Self::from_u8_unsafe(day) })
        } else {
            Err(LunarDayError)
        }
    }
}

/// 將 `LunarDay` 列舉實體轉成其它型別的方法。
impl LunarDay {
    /// 取得 `LunarDay` 列舉實體所代表的農曆日期字串。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::LunarDay;
    ///
    /// assert_eq!("初七", LunarDay::Seventh.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        let i = (self.to_u8() - 1) as usize;

        THE_LUNAR_DAYS[i]
    }
}
