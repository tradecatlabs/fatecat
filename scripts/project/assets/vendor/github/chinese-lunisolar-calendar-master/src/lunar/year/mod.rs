#[cfg(feature = "ba-zi-weight")]
mod ba_zi_weight;
mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::THE_LUNAR_YEARS;

use super::LunarYearError;
use crate::{EarthlyBranch, HeavenlyStems, Zodiac};

/// 農曆年份，由天干加地支組成，六十年一輪。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash)]
pub struct LunarYear(u8);

impl Display for LunarYear {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    ///
    /// assert_eq!("戊戌", format!("{}", lunar_year));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `LunarYear` 列舉實體的關聯函數。
impl LunarYear {
    /// 透過中國天干地支來取得 `LunarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    /// ```
    #[inline]
    pub const fn from_era(
        heavenly_stems: HeavenlyStems,
        earthly_branch: EarthlyBranch,
    ) -> Result<Self, LunarYearError> {
        let h = heavenly_stems.ordinal();
        let e = earthly_branch.ordinal();

        let year_index = if h == e {
            h
        } else if h < e {
            let diff = e - h;

            if diff & 1 == 1 {
                return Err(LunarYearError);
            }

            h + (12 - diff) * 5
        } else {
            let diff = h - e;

            if diff & 1 == 1 {
                return Err(LunarYearError);
            }

            e + diff * 6
        } - 1;

        Ok(LunarYear(year_index))
    }
}

/// 將 `LunarYear` 列舉實體轉成其它型別的方法。
impl LunarYear {
    /// 取得 `LunarYear` 實體所代表的農曆年份字串。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    ///
    /// assert_eq!("戊戌", lunar_year.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        THE_LUNAR_YEARS[self.0 as usize]
    }

    /// 取得天干。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    ///
    /// assert_eq!(HeavenlyStems::Fifth, lunar_year.to_heavenly_stems());
    /// ```
    #[inline]
    pub const fn to_heavenly_stems(&self) -> HeavenlyStems {
        unsafe { HeavenlyStems::from_ordinal_unsafe(self.0 % 10 + 1) }
    }

    /// 取得地支。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    ///
    /// assert_eq!(EarthlyBranch::Eleventh, lunar_year.to_earthly_branch());
    /// ```
    #[inline]
    pub const fn to_earthly_branch(&self) -> EarthlyBranch {
        unsafe { EarthlyBranch::from_ordinal_unsafe(self.0 % 12 + 1) }
    }

    /// 取得生肖。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{
    ///     EarthlyBranch, HeavenlyStems, LunarYear, Zodiac,
    /// };
    ///
    /// let lunar_year =
    ///     LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::Eleventh)
    ///         .unwrap();
    ///
    /// assert_eq!(Zodiac::Dog, lunar_year.to_zodiac());
    /// ```
    #[inline]
    pub const fn to_zodiac(&self) -> Zodiac {
        self.to_earthly_branch().to_zodiac()
    }
}
