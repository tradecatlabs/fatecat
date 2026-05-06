use super::LunarDay;

/// 從初一到三十共三十天的八字重量。
#[rustfmt::skip]
const BA_ZI_WEIGHT_DAYS: [u8; 30] = [
     5, 10,  8, 15, 16, 15,  8, 16,  8, 16,
     9, 17,  8, 17, 10,  8,  9, 18,  5, 15,
    10,  9,  8,  9, 15, 18,  7,  8, 16,  6,
];

impl LunarDay {
    /// 取得八字重量。
    ///
    /// # Examples
    ///
    /// ```
    /// # #[cfg(feature = "ba-zi-weight")]
    /// # {
    /// # use chinese_lunisolar_calendar::LunarDay;
    /// assert_eq!(8, LunarDay::Seventh.get_ba_zi_weight());
    /// # }
    /// ```
    #[inline]
    pub const fn get_ba_zi_weight(self) -> u8 {
        BA_ZI_WEIGHT_DAYS[(self.to_u8() - 1) as usize]
    }
}
