#[cfg(feature = "ba-zi-weight")]
mod ba_zi_weight;
mod built_in_traits;
mod chinese;
mod parse;

use core::{
    fmt::{self, Display, Formatter},
    mem::transmute,
};

use chinese::{THE_EARTHLY_BRANCHES, THE_EARTHLY_BRANCHES_CHAR};
use chrono::prelude::*;
use enum_ordinalize::Ordinalize;

use crate::Zodiac;

/// 列舉中國十二地支：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_ordinal_unsafe,
    doc = "透過整數來取得 `EarthlyBranch` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn ordinal, doc = "取得 `EarthlyBranch` 列舉實體所代表的整數。"))]
#[repr(u8)]
pub enum EarthlyBranch {
    /// 子
    First = 1,
    /// 丑
    Second,
    /// 寅
    Third,
    /// 卯
    Fourth,
    /// 辰
    Fifth,
    /// 巳
    Sixth,
    /// 午
    Seventh,
    /// 未
    Eighth,
    /// 申
    Ninth,
    /// 酉
    Tenth,
    /// 戌
    Eleventh,
    /// 亥
    Twelfth,
}

impl Display for EarthlyBranch {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!("辰", format!("{}", EarthlyBranch::Fifth));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `EarthlyBranch` 列舉實體的關聯函數。
impl EarthlyBranch {
    /// 透過子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥等字元來取得 `EarthlyBranch` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!(EarthlyBranch::Fifth, EarthlyBranch::from_char('辰').unwrap());
    /// ```
    #[inline]
    pub const fn from_char(c: char) -> Option<Self> {
        let len = THE_EARTHLY_BRANCHES_CHAR.len();

        let mut i = 0;

        loop {
            if c == THE_EARTHLY_BRANCHES_CHAR[i] {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }

            if i == len {
                break;
            }

            i += 1;
        }

        None
    }

    /// 透過生肖來取得地支。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, Zodiac};
    ///
    /// assert_eq!(
    ///     EarthlyBranch::Fifth,
    ///     EarthlyBranch::from_zodiac(Zodiac::Dragon)
    /// );
    /// ```
    #[inline]
    pub const fn from_zodiac(zodiac: Zodiac) -> Self {
        unsafe { transmute(zodiac) }
    }

    /// 將時間轉成對應的地支。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, Zodiac};
    /// use chrono::prelude::*;
    ///
    /// let date_time = Local.with_ymd_and_hms(2024, 1, 1, 12, 30, 45).unwrap();
    ///
    /// assert_eq!(EarthlyBranch::Seventh, EarthlyBranch::from_time(date_time));
    /// ```
    #[inline]
    pub fn from_time<T: Timelike>(time: T) -> EarthlyBranch {
        let hour = time.hour();

        let ordinal = ((hour + 1) % 24) / 2;

        unsafe { Self::from_ordinal_unsafe(ordinal as u8 + 1) }
    }
}

/// 將 `EarthlyBranch` 列舉實體轉成其它型別的方法。
impl EarthlyBranch {
    /// 取得 `EarthlyBranch` 列舉實體所代表的地支字串。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!("辰", EarthlyBranch::Fifth.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        let i = (self.ordinal() - 1) as usize;

        THE_EARTHLY_BRANCHES[i]
    }

    /// 取得 `EarthlyBranch` 列舉實體所代表的地支字元。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!('辰', EarthlyBranch::Fifth.to_char());
    /// ```
    #[inline]
    pub const fn to_char(self) -> char {
        let i = (self.ordinal() - 1) as usize;

        THE_EARTHLY_BRANCHES_CHAR[i]
    }

    /// 將地支轉成生肖。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, Zodiac};
    ///
    /// assert_eq!(Zodiac::Dragon, EarthlyBranch::Fifth.to_zodiac());
    /// ```
    #[inline]
    pub const fn to_zodiac(self) -> Zodiac {
        unsafe { transmute(self) }
    }
}
