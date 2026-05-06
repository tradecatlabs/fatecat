#[cfg(feature = "ba-zi-weight")]
mod ba_zi_weight;
mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::THE_LUNAR_MONTHS;
use chinese_variant::ChineseVariant;
use enum_ordinalize::Ordinalize;

use super::LunarMonthError;

/// 列舉農曆十二個月份名稱：正月、二月、三月、四月、五月、六月、七月、八月、九月、十月、冬月、臘月。包含閏月。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_u8_raw_unsafe,
    doc = "透過農曆月份數值來取得 `LunarMonth` 列舉實體。閏月必須加上 `100`。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn to_u8_raw, doc = "取得 `LunarMonth` 列舉實體所代表的農曆月份數值。閏月會加上 `100`。"))]
#[repr(u8)]
pub enum LunarMonth {
    /// 正月
    First     = 1,
    /// 二月
    Second,
    /// 三月
    Third,
    /// 四月
    Fourth,
    /// 五月
    Fifth,
    /// 六月
    Sixth,
    /// 七月
    Seventh,
    /// 八月
    Eighth,
    /// 九月
    Ninth,
    /// 十月
    Tenth,
    /// 冬月
    Eleventh,
    /// 臘月
    Twelfth,
    /// 閏正月
    LeapFirst = 101,
    /// 閏二月
    LeapSecond,
    /// 閏三月
    LeapThird,
    /// 閏四月
    LeapFourth,
    /// 閏五月
    LeapFifth,
    /// 閏六月
    LeapSixth,
    /// 閏七月
    LeapSeventh,
    /// 閏八月
    LeapEighth,
    /// 閏九月
    LeapNinth,
    /// 閏十月
    LeapTenth,
    /// 閏冬月
    LeapEleventh,
    /// 閏臘月
    LeapTwelfth,
}

impl Display for LunarMonth {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunarMonth;
    /// assert_eq!("臘月", format!("{}", LunarMonth::Twelfth));
    /// assert_eq!("腊月", format!("{:#}", LunarMonth::Twelfth));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        if f.alternate() {
            f.write_str(self.to_str(ChineseVariant::Simple))
        } else {
            f.write_str(self.to_str(ChineseVariant::Traditional))
        }
    }
}

/// 用以建立 `LunarMonth` 列舉實體的關聯函數。
impl LunarMonth {
    /// 透過農曆月份數值和是否閏月來取得 `LunarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunarMonth;
    /// assert_eq!(LunarMonth::Fifth, unsafe {
    ///     LunarMonth::from_u8_with_leap_unsafe(5, false)
    /// });
    /// assert_eq!(LunarMonth::LeapFifth, unsafe {
    ///     LunarMonth::from_u8_with_leap_unsafe(5, true)
    /// });
    /// ```
    ///
    /// # Safety
    /// 必須先確認傳入的整數是合法的。
    #[inline]
    pub const unsafe fn from_u8_with_leap_unsafe(mut month: u8, leap: bool) -> Self {
        if leap {
            month += 100;
        }

        Self::from_u8_raw_unsafe(month)
    }

    /// 透過農曆月份數值和是否閏月來取得 `LunarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::LunarMonth;
    /// assert_eq!(
    ///     LunarMonth::Fifth,
    ///     LunarMonth::from_u8_with_leap(5, false).unwrap()
    /// );
    /// assert_eq!(
    ///     LunarMonth::LeapFifth,
    ///     LunarMonth::from_u8_with_leap(5, true).unwrap()
    /// );
    /// ```
    #[inline]
    pub const fn from_u8_with_leap(month: u8, leap: bool) -> Result<Self, LunarMonthError> {
        if month >= 1 && month <= 12 {
            Ok(unsafe { Self::from_u8_with_leap_unsafe(month, leap) })
        } else {
            Err(LunarMonthError)
        }
    }
}

/// 將 `LunarMonth` 列舉實體轉成其它型別的方法。
impl LunarMonth {
    /// 取得 `Zodiac` 列舉實體所代表的生肖字串。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{ChineseVariant, LunarMonth};
    ///
    /// assert_eq!("臘月", LunarMonth::Twelfth.to_str(ChineseVariant::Traditional));
    /// assert_eq!("腊月", LunarMonth::Twelfth.to_str(ChineseVariant::Simple));
    /// ```
    #[inline]
    pub const fn to_str(self, chinese_variant: ChineseVariant) -> &'static str {
        let mut i = (self.to_u8_raw() - 1) as usize;

        if i >= 100 {
            i -= 88;
        }

        match chinese_variant {
            ChineseVariant::Simple => THE_LUNAR_MONTHS[i].1,
            ChineseVariant::Traditional => THE_LUNAR_MONTHS[i].0,
        }
    }

    /// 取得 `LunarMonth` 列舉實體所代表的農曆月份數值。
    #[inline]
    pub const fn to_u8(self) -> u8 {
        let mut i = self.to_u8_raw();

        if i >= 101 {
            i -= 100;
        }

        i
    }
}

/// 農曆月份相關計算方法。
impl LunarMonth {
    /// 是否為閏月。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::LunarMonth;
    ///
    /// assert_eq!(false, LunarMonth::Twelfth.is_leap_month());
    /// assert_eq!(true, LunarMonth::LeapTwelfth.is_leap_month());
    /// ```
    #[inline]
    pub const fn is_leap_month(self) -> bool {
        self.to_u8_raw() >= 101
    }
}
