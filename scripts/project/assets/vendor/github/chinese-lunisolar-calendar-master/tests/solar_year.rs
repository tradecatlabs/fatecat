use chinese_lunisolar_calendar::SolarYear;

#[test]
fn parse_str_to_u16() {
    let solar_year = SolarYear::parse_str("二零一八").unwrap();
    assert_eq!(2018, solar_year.to_u16());

    let solar_year = SolarYear::parse_str("二〇一八").unwrap();
    assert_eq!(2018, solar_year.to_u16());
}

#[test]
fn is_leap() {
    assert!(SolarYear::from_u16(2000).is_leap());
    assert!(!SolarYear::from_u16(2001).is_leap());
    assert!(!SolarYear::from_u16(2002).is_leap());
    assert!(SolarYear::from_u16(2004).is_leap());
    assert!(!SolarYear::from_u16(2100).is_leap());
    assert!(SolarYear::from_u16(2104).is_leap());
}

#[test]
fn get_total_days() {
    assert_eq!(366, SolarYear::from_u16(2000).get_total_days());
    assert_eq!(365, SolarYear::from_u16(2001).get_total_days());
    assert_eq!(365, SolarYear::from_u16(2002).get_total_days());
    assert_eq!(366, SolarYear::from_u16(2004).get_total_days());
    assert_eq!(365, SolarYear::from_u16(2100).get_total_days());
    assert_eq!(366, SolarYear::from_u16(2104).get_total_days());
}
