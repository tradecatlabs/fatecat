use super::{SolarYear, SolarYearError, ALTERNATIVE_ZERO, THE_SOLAR_YEAR_NUMBERS_CHAR};

/// 用以解析字串的關聯函數。
impl SolarYear {
    /// 透過西曆年份字串來取得 `SolarYear` 實體。
    ///
    /// # Examples
    ///
    /// ```
    /// # use chinese_lunisolar_calendar::SolarYear;
    /// assert_eq!(
    ///     SolarYear::from_u16(2008),
    ///     SolarYear::parse_str("二〇〇八").unwrap()
    /// );
    /// assert_eq!(
    ///     SolarYear::from_u16(2008),
    ///     SolarYear::parse_str("二零零八").unwrap()
    /// );
    /// ```
    pub fn parse_str<S: AsRef<str>>(s: S) -> Result<Self, SolarYearError> {
        let s = s.as_ref();

        let mut year = 0u16;

        for (count, c) in s.chars().enumerate() {
            if count == 5 {
                return Err(SolarYearError);
            }

            if c.is_ascii_digit() {
                year = year
                    .checked_mul(10)
                    .ok_or(SolarYearError)?
                    .checked_add((c as u8 - b'0') as u16)
                    .ok_or(SolarYearError)?;
            } else {
                let mut failed = true;

                for (i, cc) in THE_SOLAR_YEAR_NUMBERS_CHAR.iter().copied().enumerate() {
                    if c == cc {
                        year = year
                            .checked_mul(10)
                            .ok_or(SolarYearError)?
                            .checked_add(i as u16)
                            .ok_or(SolarYearError)?;

                        failed = false;

                        break;
                    }
                }

                if failed {
                    match c {
                        ALTERNATIVE_ZERO => {
                            year = year.checked_mul(10).ok_or(SolarYearError)?;
                        },
                        _ => return Err(SolarYearError),
                    }
                }
            }
        }

        Ok(SolarYear(year))
    }
}
