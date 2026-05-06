use chinese_lunisolar_calendar::{
    LunarDay, LunarMonth, LunarYear, LunisolarDate, LunisolarYear, SolarDate, SolarYear,
};

#[test]
fn from_solar_date() {
    let solar_date = SolarDate::from_ymd(1993, 1, 12).unwrap();

    let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1992.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("壬申").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(12, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(20).unwrap(), lunisolar_date.to_lunar_day());

    let solar_date = SolarDate::from_ymd(1993, 1, 23).unwrap();

    let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(1, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(1).unwrap(), lunisolar_date.to_lunar_day());

    let solar_date = SolarDate::from_ymd(1993, 4, 22).unwrap();

    let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(3, true).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(1).unwrap(), lunisolar_date.to_lunar_day());

    let solar_date = SolarDate::from_ymd(1993, 8, 10).unwrap();

    let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(6, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(23).unwrap(), lunisolar_date.to_lunar_day());

    let solar_date = SolarDate::from_ymd(1993, 12, 12).unwrap();

    let lunisolar_date = LunisolarDate::from_solar_date(solar_date).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(10, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(29).unwrap(), lunisolar_date.to_lunar_day());
}

#[test]
fn from_ymd() {
    let lunisolar_date = LunisolarDate::from_ymd(1992, 12, false, 20).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1992.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("壬申").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(12, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(20).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::from_ymd(1993, 1, false, 1).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(1, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(1).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::from_ymd(1993, 3, true, 1).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(3, true).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(1).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::from_ymd(1993, 6, false, 23).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(6, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(23).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::from_ymd(1993, 10, false, 29).unwrap();

    assert_eq!(SolarYear::from_u16(1993), lunisolar_date.to_solar_year());
    assert_eq!(
        LunisolarYear::from_solar_year(1993.into()).unwrap(),
        lunisolar_date.to_lunisolar_year()
    );
    assert_eq!(LunarYear::parse_str("癸酉").unwrap(), lunisolar_date.to_lunar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(10, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(29).unwrap(), lunisolar_date.to_lunar_day());
}

#[test]
fn parse_str() {
    let lunisolar_date = LunisolarDate::parse_str("二零一八　戊戌、狗年　六月　十九").unwrap();

    assert_eq!(SolarYear::from_u16(2018), lunisolar_date.to_solar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(6, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(19).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::parse_str("二〇一八　戊戌、狗年　六月　十九").unwrap();

    assert_eq!(SolarYear::from_u16(2018), lunisolar_date.to_solar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(6, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(19).unwrap(), lunisolar_date.to_lunar_day());

    let lunisolar_date = LunisolarDate::parse_str("2018　六月　十九日").unwrap();

    assert_eq!(SolarYear::from_u16(2018), lunisolar_date.to_solar_year());
    assert_eq!(LunarMonth::from_u8_with_leap(6, false).unwrap(), lunisolar_date.to_lunar_month());
    assert_eq!(LunarDay::from_u8(19).unwrap(), lunisolar_date.to_lunar_day());
}

#[test]
fn the_n_day_in_this_year() {
    assert_eq!(344, LunisolarDate::from_ymd(1992, 12, false, 20).unwrap().the_n_day_in_this_year());
    assert_eq!(1, LunisolarDate::from_ymd(1993, 1, false, 1).unwrap().the_n_day_in_this_year());
    assert_eq!(60, LunisolarDate::from_ymd(1993, 3, false, 1).unwrap().the_n_day_in_this_year());
    assert_eq!(200, LunisolarDate::from_ymd(1993, 6, false, 23).unwrap().the_n_day_in_this_year());
    assert_eq!(324, LunisolarDate::from_ymd(1993, 10, false, 29).unwrap().the_n_day_in_this_year());
}
