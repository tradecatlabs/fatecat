mod built_in_traits;
mod chinese;
mod parse;

use core::{
    fmt::{self, Display, Formatter},
    mem::transmute,
};

use chinese::{THE_ZODIAC_SIGNS, THE_ZODIAC_SIGNS_CHAR};
use enum_ordinalize::Ordinalize;

use crate::{ChineseVariant, EarthlyBranch};

/// 列舉中國十二生肖：鼠、牛、虎、兔、龍、蛇、馬、羊、猴、雞、狗、豬。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_ordinal_unsafe,
    doc = "透過整數來取得 `Zodiac` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn ordinal, doc = "取得 `Zodiac` 列舉實體所代表的整數。"))]
#[repr(u8)]
pub enum Zodiac {
    /// 鼠
    Rat = 1,
    /// 牛
    Ox,
    /// 虎
    Tiger,
    /// 兔
    Rabbit,
    /// 龍
    Dragon,
    /// 蛇
    Snake,
    /// 馬
    Horse,
    /// 羊
    Goat,
    /// 猴
    Monkey,
    /// 雞
    Rooster,
    /// 狗
    Dog,
    /// 豬
    Pig,
}

impl Display for Zodiac {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::Zodiac;
    /// assert_eq!("龍", format!("{}", Zodiac::Dragon));
    /// assert_eq!("龙", format!("{:#}", Zodiac::Dragon));
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

/// 用以建立 `Zodiac` 列舉實體的關聯函數。
impl Zodiac {
    /// 透過鼠、牛、虎、兔、龍、蛇、馬、羊、猴、雞、狗、豬等字元來取得 `Zodiac` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::Zodiac;
    /// assert_eq!(Zodiac::Dragon, Zodiac::from_char('龍').unwrap());
    /// assert_eq!(Zodiac::Dragon, Zodiac::from_char('龙').unwrap());
    /// ```
    #[inline]
    pub const fn from_char(c: char) -> Option<Self> {
        let len = THE_ZODIAC_SIGNS_CHAR.len();

        let mut i = 0;

        loop {
            let t = THE_ZODIAC_SIGNS_CHAR[i];

            if c == t.0 || c == t.1 {
                return Some(unsafe { Self::from_ordinal_unsafe(i as u8 + 1) });
            }

            if i == len {
                break;
            }

            i += 1;
        }

        None
    }

    /// 透過地支來取得生肖。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, Zodiac};
    ///
    /// assert_eq!(
    ///     Zodiac::Dragon,
    ///     Zodiac::from_earthly_branch(EarthlyBranch::Fifth)
    /// );
    /// ```
    #[inline]
    pub const fn from_earthly_branch(earthly_branch: EarthlyBranch) -> Self {
        unsafe { transmute(earthly_branch) }
    }
}

/// 將 `Zodiac` 列舉實體轉成其它型別的方法。
impl Zodiac {
    /// 取得 `Zodiac` 列舉實體所代表的生肖字串。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{ChineseVariant, Zodiac};
    ///
    /// assert_eq!("龍", Zodiac::Dragon.to_str(ChineseVariant::Traditional));
    /// assert_eq!("龙", Zodiac::Dragon.to_str(ChineseVariant::Simple));
    /// ```
    #[inline]
    pub const fn to_str(self, chinese_variant: ChineseVariant) -> &'static str {
        let i = (self.ordinal() - 1) as usize;

        match chinese_variant {
            ChineseVariant::Simple => THE_ZODIAC_SIGNS[i].1,
            ChineseVariant::Traditional => THE_ZODIAC_SIGNS[i].0,
        }
    }

    /// 取得 `Zodiac` 列舉實體所代表的生肖字元。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{Zodiac, ChineseVariant};
    ///
    /// assert_eq!('龍', Zodiac::Dragon.to_char(ChineseVariant::Traditional));
    /// assert_eq!('龙', Zodiac::Dragon.to_char(ChineseVariant::Simple));
    #[inline]
    pub const fn to_char(self, chinese_variant: ChineseVariant) -> char {
        let i = (self.ordinal() - 1) as usize;

        match chinese_variant {
            ChineseVariant::Simple => THE_ZODIAC_SIGNS_CHAR[i].1,
            ChineseVariant::Traditional => THE_ZODIAC_SIGNS_CHAR[i].0,
        }
    }

    /// 將生肖轉成地支。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, Zodiac};
    ///
    /// assert_eq!(EarthlyBranch::Fifth, Zodiac::Dragon.to_earthly_branch());
    /// ```
    #[inline]
    pub const fn to_earthly_branch(self) -> EarthlyBranch {
        unsafe { transmute(self) }
    }
}
