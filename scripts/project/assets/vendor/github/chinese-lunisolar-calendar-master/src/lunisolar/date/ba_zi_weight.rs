use chrono::Timelike;

use super::LunisolarDate;
use crate::EarthlyBranch;

impl LunisolarDate {
    /// 搭配出生時間(地支)，來計算八字有幾錢重。(10錢 = 1兩)
    ///
    /// * 子：２３～１
    /// * 丑：１～３
    /// * 寅：３～５
    /// * 卯：５～７
    /// * 辰：７～９
    /// * 巳：９～１１
    /// * 午：１１～１３
    /// * 未：１３～１５
    /// * 申：１５～１７
    /// * 酉：１７～１９
    /// * 戌：１９～２１
    /// * 亥：２１～２３
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{EarthlyBranch, LunisolarDate, SolarDate};
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(35, lunisolar_date.get_ba_zi_weight(EarthlyBranch::First));
    /// ```
    #[inline]
    pub const fn get_ba_zi_weight(self, earthly_branch: EarthlyBranch) -> u8 {
        self.lunisolar_year.to_lunar_year().get_ba_zi_weight()
            + self.lunar_month.get_ba_zi_weight()
            + self.lunar_day.get_ba_zi_weight()
            + earthly_branch.get_ba_zi_weight()
    }

    /// 搭配出生時間，來計算八字有幾錢重。(10錢 = 1兩)
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::{LunisolarDate, SolarDate};
    /// use chrono::prelude::*;
    ///
    /// let solar_date = SolarDate::from_ymd(2024, 2, 10).unwrap();
    ///
    /// let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();
    ///
    /// assert_eq!(
    ///     29,
    ///     lunisolar_date.get_ba_zi_weight_by_time(
    ///         NaiveTime::from_hms_opt(12, 30, 0).unwrap()
    ///     )
    /// );
    /// ```
    #[inline]
    pub fn get_ba_zi_weight_by_time<T: Timelike>(self, time: T) -> u8 {
        let earthly_branch = EarthlyBranch::from_time(time);

        self.get_ba_zi_weight(earthly_branch)
    }
}
