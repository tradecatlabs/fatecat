use super::{SolarDate, SolarDateError, SolarDay, SolarMonth, SolarYear};

/// 用以解析字串的關聯函數。
impl SolarDate {
    /// 用中文西曆年月日字串來產生 `SolarDate` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// use chinese_lunisolar_calendar::SolarDate;
    ///
    /// let solar_date = SolarDate::parse_str("二〇二四年一月一日").unwrap();
    ///
    /// assert_eq!("二〇二四年一月一日", solar_date.to_string());
    /// ```
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, SolarDateError> {
        let s = s.as_ref();

        let year_index = {
            match s.find('年') {
                Some(index) => index,
                None => match s.find('　') {
                    Some(index) => index,
                    None => return Err(SolarDateError::YearIncorrect),
                },
            }
        };

        let year_str = s[..year_index].trim();

        let solar_year = SolarYear::parse_str(year_str)?;

        let s = &s[year_index + 3..];

        let month_index = {
            match s.find('月') {
                Some(index) => index,
                None => match s.find('　') {
                    Some(index) => index,
                    None => return Err(SolarDateError::MonthIncorrect),
                },
            }
        };

        let month_str = s[..month_index + 3].trim();

        let solar_month = SolarMonth::parse_str(month_str)?;

        let mut day_str = s[month_index + 3..].trim();

        if let Some(day) = day_str.strip_suffix('日') {
            day_str = day;
        }

        let solar_day = SolarDay::parse_str(day_str)?;

        Self::from_solar_year_month_day(solar_year, solar_month, solar_day)
            .map_err(|err| err.into())
    }
}
