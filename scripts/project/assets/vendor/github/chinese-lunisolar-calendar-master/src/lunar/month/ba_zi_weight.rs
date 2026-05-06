use super::LunarMonth;

/// 從正月到臘月共十二個月的八字重量。
const BA_ZI_WEIGHT_MONTHS: [u8; 12] = [6, 7, 18, 9, 5, 16, 9, 15, 18, 8, 9, 5];

impl LunarMonth {
    /// 取得八字重量。
    ///
    /// # Examples
    ///
    /// ```
    /// # #[cfg(feature = "ba-zi-weight")]
    /// # {
    /// # use chinese_lunisolar_calendar::LunarMonth;
    /// assert_eq!(5, LunarMonth::Fifth.get_ba_zi_weight());
    /// # }
    /// ```
    #[inline]
    pub const fn get_ba_zi_weight(self) -> u8 {
        BA_ZI_WEIGHT_MONTHS[(self.to_u8() - 1) as usize]
    }
}
