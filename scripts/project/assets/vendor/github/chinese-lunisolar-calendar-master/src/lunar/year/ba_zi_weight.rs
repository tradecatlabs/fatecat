use super::LunarYear;

/// 從甲子年到癸亥年共六十年的八字重量。
#[rustfmt::skip]
const BA_ZI_WEIGHT_YEARS: [u8; 60] = [
    12,  9,  6,  7, 12,  5,  9,  8,  7,  8,
    15,  9, 16,  8,  8, 19, 12,  6,  8,  7,
     5, 15,  6, 16, 15,  7,  9, 12, 10,  7,
    15,  6,  5, 14, 14,  9,  7,  7,  9, 12,
     8,  7, 13,  5, 14,  5,  9, 17,  5,  7,
    12,  8,  8,  6, 19,  6,  8, 16, 10,  7,
];

impl LunarYear {
    /// 取得八字重量。
    ///
    /// # Examples
    ///
    /// ```
    /// # #[cfg(feature = "ba-zi-weight")]
    /// # {
    /// # use chinese_lunisolar_calendar::LunarYear;
    /// assert_eq!(14, LunarYear::parse_str("戊戌").unwrap().get_ba_zi_weight());
    /// # }
    /// ```
    #[inline]
    pub const fn get_ba_zi_weight(self) -> u8 {
        BA_ZI_WEIGHT_YEARS[self.0 as usize]
    }
}
