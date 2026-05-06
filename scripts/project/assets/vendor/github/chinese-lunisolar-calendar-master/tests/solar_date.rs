use chinese_lunisolar_calendar::{
    chrono::prelude::*, LunisolarDate, SolarDate, SolarDay, SolarMonth, SolarYear,
};

#[test]
fn from_date() {
    let solar_year = SolarYear::from_u16(2018);
    let solar_month = SolarMonth::from_u8(6).unwrap();
    let solar_day = SolarDay::from_u8(19).unwrap();

    let naive_date = NaiveDate::from_ymd_opt(2018, 6, 19).unwrap();

    let solar_date = SolarDate::from_date(naive_date).unwrap();

    assert_eq!(solar_year, solar_date.to_solar_year());
    assert_eq!(solar_month, solar_date.to_solar_month());
    assert_eq!(solar_day, solar_date.to_solar_day());
}

#[test]
fn from_solar_year_month_day() {
    let solar_year = SolarYear::from_u16(2018);
    let solar_month = SolarMonth::from_u8(6).unwrap();
    let solar_day = SolarDay::from_u8(19).unwrap();

    let solar_date =
        SolarDate::from_solar_year_month_day(solar_year, solar_month, solar_day).unwrap();

    assert_eq!(solar_year, solar_date.to_solar_year());
    assert_eq!(solar_month, solar_date.to_solar_month());
    assert_eq!(solar_day, solar_date.to_solar_day());
}

#[test]
fn from_ymd() {
    let solar_year = SolarYear::from_u16(2018);
    let solar_month = SolarMonth::from_u8(6).unwrap();
    let solar_day = SolarDay::from_u8(19).unwrap();

    let solar_date = SolarDate::from_ymd(2018, 6, 19).unwrap();

    assert_eq!(solar_year, solar_date.to_solar_year());
    assert_eq!(solar_month, solar_date.to_solar_month());
    assert_eq!(solar_day, solar_date.to_solar_day());
}

#[test]
fn from_lunisolar_date() {
    let solar_year = SolarYear::from_u16(2018);
    let solar_month = SolarMonth::from_u8(6).unwrap();
    let solar_day = SolarDay::from_u8(19).unwrap();

    let lunisolar_date = LunisolarDate::from_ymd(2018, 5, false, 6).unwrap();

    let solar_date = SolarDate::from_lunisolar_date(lunisolar_date);

    assert_eq!(solar_year, solar_date.to_solar_year());
    assert_eq!(solar_month, solar_date.to_solar_month());
    assert_eq!(solar_day, solar_date.to_solar_day());
}

#[test]
fn parse_str() {
    let solar_date = SolarDate::parse_str("二零一八年六月十九日").unwrap();

    assert_eq!(SolarYear::from_u16(2018), solar_date.to_solar_year());
    assert_eq!(SolarMonth::from_u8(6).unwrap(), solar_date.to_solar_month());
    assert_eq!(SolarDay::from_u8(19).unwrap(), solar_date.to_solar_day());

    let solar_date = SolarDate::parse_str("二〇一八年六月十九日").unwrap();

    assert_eq!(SolarYear::from_u16(2018), solar_date.to_solar_year());
    assert_eq!(SolarMonth::from_u8(6).unwrap(), solar_date.to_solar_month());
    assert_eq!(SolarDay::from_u8(19).unwrap(), solar_date.to_solar_day());

    let solar_date = SolarDate::parse_str("2018　六月　十九").unwrap();

    assert_eq!(SolarYear::from_u16(2018), solar_date.to_solar_year());
    assert_eq!(SolarMonth::from_u8(6).unwrap(), solar_date.to_solar_month());
    assert_eq!(SolarDay::from_u8(19).unwrap(), solar_date.to_solar_day());
}

#[test]
fn the_n_day_in_this_year() {
    assert_eq!(4, SolarDate::from_ymd(2013, 1, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(63, SolarDate::from_ymd(2013, 3, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(94, SolarDate::from_ymd(2013, 4, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(124, SolarDate::from_ymd(2013, 5, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(64, SolarDate::from_ymd(2020, 3, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(95, SolarDate::from_ymd(2020, 4, 4).unwrap().the_n_day_in_this_year());
    assert_eq!(125, SolarDate::from_ymd(2020, 5, 4).unwrap().the_n_day_in_this_year());
}
