use super::{LunarDay, LunarMonth, LunisolarDate, LunisolarDateError, LunisolarYear, SolarYear};

/// 用以解析字串的關聯函數。
impl LunisolarDate {
    /// 用中文農曆西曆年和農曆月日字串來產生 `LunisolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::LunisolarDate;
    ///
    /// let lunisolar_date = LunisolarDate::parse_str("二〇二四　甲辰、龍年　正月　初一").unwrap();
    /// let lunisolar_date = LunisolarDate::parse_str("二零二四年正月初一").unwrap();
    /// ```
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, LunisolarDateError> {
        let s = s.as_ref();

        let year_index = {
            match s.find('　') {
                Some(index) => index,
                None => match s.find('年') {
                    Some(index) => index,
                    None => return Err(LunisolarDateError::YearIncorrect),
                },
            }
        };

        let year_str = s[..year_index].trim();

        let lunisolar_year = LunisolarYear::from_solar_year(
            SolarYear::parse_str(year_str).map_err(|_| LunisolarDateError::YearIncorrect)?,
        )?;

        let s = &s[year_index + 3..];

        let month_index = {
            match s.find('月') {
                Some(index) => index,
                None => match s.find('　') {
                    Some(index) => index,
                    None => return Err(LunisolarDateError::MonthIncorrect),
                },
            }
        };

        let month_str = s[..month_index + 3].trim();

        let month_str = {
            match month_str.find('年') {
                Some(index) => month_str[index + 3..].trim(),
                None => match month_str.find('　') {
                    Some(index) => month_str[index + 3..].trim(),
                    None => month_str,
                },
            }
        };

        let lunar_month = LunarMonth::parse_str(month_str)?;

        let mut day_str = s[month_index + 3..].trim();

        if day_str.ends_with('日') {
            day_str = &day_str[..day_str.len() - 3];
        }

        let lunar_day = LunarDay::parse_str(day_str)?;

        Self::from_lunisolar_year_lunar_month_day(lunisolar_year, lunar_month, lunar_day)
    }
}
