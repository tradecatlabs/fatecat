#![cfg(feature = "ba-zi-weight")]

use chinese_lunisolar_calendar::LunisolarDate;
use chrono::prelude::*;

#[test]
fn get_ba_zi_weight_by_time() {
    assert_eq!(
        48,
        LunisolarDate::from_ymd(1993, 6, false, 23)
            .unwrap()
            .get_ba_zi_weight_by_time(NaiveTime::from_hms_opt(23, 30, 0).unwrap())
    );
}
