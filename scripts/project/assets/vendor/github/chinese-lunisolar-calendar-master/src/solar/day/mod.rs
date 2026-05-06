mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::THE_SOLAR_DAYS;
use enum_ordinalize::Ordinalize;

use super::SolarDayError;

/// 列舉西曆三十一個天數名稱：一、二、...、十一、十二、...、二十一、二十二、...、三十、三十一。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_u8_unsafe,
    doc = "透過西曆日期數值來取得 `SolarDay` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn to_u8, doc = "取得 `SolarDay` 列舉實體所代表的西曆日期字串。"))]
#[repr(u8)]
pub enum SolarDay {
    /// 一
    First = 1,
    /// 二
    Second,
    /// 三
    Third,
    /// 四
    Fourth,
    /// 五
    Fifth,
    /// 六
    Sixth,
    /// 七
    Seventh,
    /// 八
    Eighth,
    /// 九
    Ninth,
    /// 十
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
    /// 二十一
    TwentyFirst,
    /// 二十二
    TwentySecond,
    /// 二十三
    TwentyThird,
    /// 二十四
    TwentyFourth,
    /// 二十五
    TwentyFifth,
    /// 二十六
    TwentySixth,
    /// 二十七
    TwentySeventh,
    /// 二十八
    TwentyEighth,
    /// 二十九
    TwentyNinth,
    /// 三十
    Thirty,
    /// 三十一
    ThirtyFirst,
}

impl Display for SolarDay {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDay;
    /// assert_eq!("十五", format!("{}", SolarDay::Fifteen));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `SolarDay` 列舉實體的關聯函數。
impl SolarDay {
    /// 透過西曆日期數值來取得 `SolarDay` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDay;
    /// let solar_day = SolarDay::from_u8(5).unwrap();
    /// ```
    #[inline]
    pub const fn from_u8(day: u8) -> Result<Self, SolarDayError> {
        if day >= 1 && day <= 31 {
            Ok(unsafe { Self::from_u8_unsafe(day) })
        } else {
            Err(SolarDayError)
        }
    }

    /// 透過西曆日期數值來取得 `SolarDay` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDay;
    /// let solar_day = SolarDay::from_u32(5).unwrap();
    /// ```
    #[inline]
    pub const fn from_u32(day: u32) -> Result<Self, SolarDayError> {
        if day >= 1 && day <= 31 {
            Ok(unsafe { Self::from_u8_unsafe(day as u8) })
        } else {
            Err(SolarDayError)
        }
    }
}

/// 將 `SolarDay` 列舉實體轉成其它型別的方法。
impl SolarDay {
    /// 取得 `SolarDay` 列舉實體所代表的西曆日期字串。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarDay;
    /// assert_eq!("十五", SolarDay::Fifteen.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        let i = (self.to_u8() - 1) as usize;

        THE_SOLAR_DAYS[i]
    }

    /// 取得 `SolarDay` 列舉實體所代表的西曆日期字串。
    #[inline]
    pub const fn to_u32(self) -> u32 {
        self.to_u8() as u32
    }
}
