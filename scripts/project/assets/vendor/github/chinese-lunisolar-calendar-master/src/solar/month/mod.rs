mod built_in_traits;
mod chinese;
mod parse;

use core::fmt::{self, Display, Formatter};

use chinese::THE_SOLAR_MONTHS;
use enum_ordinalize::Ordinalize;

use super::{SolarMonthError, SolarYear};

/// 列舉西曆十二個月份名稱：一月、二月、三月、四月、五月、六月、七月、八月、九月、十月、十一月、十二月。
#[derive(Debug, Clone, Copy, PartialOrd, Ord, PartialEq, Eq, Hash, Ordinalize)]
#[ordinalize(impl_trait = false)]
#[ordinalize(from_ordinal_unsafe(
    pub fn from_u8_unsafe,
    doc = "透過西曆月份數值來取得 `SolarMonth` 列舉實體。",
    doc = "# Safety",
    doc = "必須先確認傳入的整數是合法的。",
))]
#[ordinalize(ordinal(pub fn to_u8, doc = "取得 `SolarMonth` 列舉實體所代表的西曆月份數值。"))]
#[repr(u8)]
pub enum SolarMonth {
    /// 一月
    January = 1,
    /// 二月
    February,
    /// 三月
    March,
    /// 四月
    April,
    /// 五月
    May,
    /// 六月
    June,
    /// 七月
    July,
    /// 八月
    August,
    /// 九月
    September,
    /// 十月
    October,
    /// 十一月
    November,
    /// 十二月
    December,
}

impl Display for SolarMonth {
    /// Formats the value using the given formatter.
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarMonth;
    /// assert_eq!("五月", format!("{}", SolarMonth::May));
    /// ```
    #[inline]
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        f.write_str(self.to_str())
    }
}

/// 用以建立 `SolarMonth` 列舉實體的關聯函數。
impl SolarMonth {
    /// 透過西曆月份數值來取得 `SolarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarMonth;
    /// let solar_month = SolarMonth::from_u8(5).unwrap();
    /// ```
    #[inline]
    pub const fn from_u8(month: u8) -> Result<Self, SolarMonthError> {
        if month >= 1 && month <= 12 {
            Ok(unsafe { Self::from_u8_unsafe(month) })
        } else {
            Err(SolarMonthError)
        }
    }

    /// 透過西曆月份數值來取得 `SolarMonth` 列舉實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarMonth;
    /// let solar_month = SolarMonth::from_u32(5).unwrap();
    /// ```
    #[inline]
    pub const fn from_u32(month: u32) -> Result<Self, SolarMonthError> {
        if month >= 1 && month <= 12 {
            Ok(unsafe { Self::from_u8_unsafe(month as u8) })
        } else {
            Err(SolarMonthError)
        }
    }
}

/// 將 `SolarMonth` 列舉實體轉成其它型別的方法。
impl SolarMonth {
    /// 取得 `SolarMonth` 列舉實體所代表的西曆月份字串。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarMonth;
    /// assert_eq!("五月", SolarMonth::May.to_str());
    /// ```
    #[inline]
    pub const fn to_str(self) -> &'static str {
        let i = (self.to_u8() - 1) as usize;

        THE_SOLAR_MONTHS[i]
    }

    /// 取得 `SolarMonth` 列舉實體所代表的西曆月份數值。
    #[inline]
    pub const fn to_u32(self) -> u32 {
        self.to_u8() as u32
    }
}

/// 西曆月份相關計算方法。
impl SolarMonth {
    /// 傳入指定的西曆年，並計算此西曆月在這個指定的西曆年內共有幾天。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::{SolarMonth, SolarYear};
    /// assert_eq!(
    ///     31,
    ///     SolarMonth::January.get_total_days(SolarYear::from_u16(2008))
    /// );
    /// assert_eq!(
    ///     29,
    ///     SolarMonth::February.get_total_days(SolarYear::from_u16(2008))
    /// );
    /// assert_eq!(30, SolarMonth::April.get_total_days(SolarYear::from_u16(2008)));
    /// assert_eq!(
    ///     28,
    ///     SolarMonth::February.get_total_days(SolarYear::from_u16(2009))
    /// );
    /// ```
    #[inline]
    pub const fn get_total_days(self, solar_year: SolarYear) -> u8 {
        solar_year.get_total_days_in_a_month(self)
    }
}
