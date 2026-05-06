use super::EarthlyBranch;

/// 從子時到亥時共十二地支的八字重量。
const BA_ZI_WEIGHT_TIME: [u8; 12] = [16, 6, 7, 10, 9, 16, 10, 8, 8, 9, 6, 6];

impl EarthlyBranch {
    /// 取得八字重量。
    ///
    /// # Examples
    ///
    /// ```
    /// # #[cfg(feature = "ba-zi-weight")]
    /// # {
    /// # use chinese_lunisolar_calendar::EarthlyBranch;
    /// assert_eq!(9, EarthlyBranch::Fifth.get_ba_zi_weight());
    /// # }
    /// ```
    #[inline]
    pub const fn get_ba_zi_weight(self) -> u8 {
        let i = (self.ordinal() - 1) as usize;

        BA_ZI_WEIGHT_TIME[i]
    }
}
