use std::ops::Add;

use chinese_lunisolar_calendar::{
    chrono::Duration, LunisolarDate, MAX_LUNISOLAR_DATE_IN_SOLAR_DATE,
    MIN_LUNISOLAR_DATE_IN_SOLAR_DATE,
};

#[test]
fn loopback() {
    let mut current = MIN_LUNISOLAR_DATE_IN_SOLAR_DATE;

    while current <= MAX_LUNISOLAR_DATE_IN_SOLAR_DATE {
        let lunar_date = LunisolarDate::from_solar_date(current).unwrap();

        assert_eq!(lunar_date, current.to_lunisolar_date().unwrap());
        assert_eq!(current, lunar_date.to_solar_date());

        current = current.to_naive_date().add(Duration::days(1)).try_into().unwrap();
    }
}
