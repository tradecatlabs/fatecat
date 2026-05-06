mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::{THE_HEAVENLY_STEMS, THE_HEAVENLY_STEMS_CHAR};
use enum_ordinalize::Ordinalize;

/// 列舉中國十天干：甲、乙、丙、丁、戊、己、更、辛、壬、葵。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_ordinal_unsafe,
    doc = "透過整數來取得 `HeavenlyStems` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn ordinal, doc = "取得 `HeavenlyStems` 列舉實體所代表的整數。"))]
#[repr(u8)]
pub enum HeavenlyStems {
    /// 甲
    First = 1,
    /// 乙
    Second,
    /// 丙
    Third,
    /// 丁
    Fourth,
    /// 戊
    Fifth,
    /// 己
    Sixth,
    /// 更
    Seventh,
    /// 辛
    Eighth,
    /// 壬
    Ninth,
    /// 葵
    Tenth,
}

impl Display for HeavenlyStems {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::HeavenlyStems;
    /// assert_eq!("戊", format!("{}", HeavenlyStems::Fifth));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `HeavenlyStems` 列舉實體的關聯函數。
impl HeavenlyStems {
    /// 透過甲、乙、丙、丁、戊、己、更、辛、壬、葵等字元來取得 `HeavenlyStems` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::HeavenlyStems;
    /// assert_eq!(HeavenlyStems::Fifth, HeavenlyStems::from_char('戊').unwrap());
    /// ```
    #[inline]
    pub const fn from_char(c: char) -> Option<Self> {
        let len = THE_HEAVENLY_STEMS_CHAR.len();

        let mut i = 0;

        loop {
            if c == THE_HEAVENLY_STEMS_CHAR[i] {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }

            if i == len {
                break;
            }

            i += 1;
        }

        None
    }
}

/// 將 `HeavenlyStems` 列舉實體轉成其它型別的方法。
impl HeavenlyStems {
    /// 取得 `HeavenlyStems` 列舉實體所代表的地支字串。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::HeavenlyStems;
    /// assert_eq!("戊", HeavenlyStems::Fifth.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        let i = (self.ordinal() - 1) as usize;

        THE_HEAVENLY_STEMS[i]
    }

    /// 取得 `HeavenlyStems` 列舉實體所代表的地支字元。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::HeavenlyStems;
    /// assert_eq!('戊', HeavenlyStems::Fifth.to_char());
    /// ```
    #[inline]
    pub const fn to_char(self) -> char {
        let i = (self.ordinal() - 1) as usize;

        THE_HEAVENLY_STEMS_CHAR[i]
    }
}
