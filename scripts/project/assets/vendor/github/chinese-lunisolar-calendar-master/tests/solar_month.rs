use chinese_lunisolar_calendar::SolarMonth;

#[test]
fn parse_str() {
    assert_eq!(SolarMonth::January, SolarMonth::parse_str("一月").unwrap());
    assert_eq!(SolarMonth::February, SolarMonth::parse_str("二月").unwrap());
    assert_eq!(SolarMonth::May, SolarMonth::parse_str("五月").unwrap());
    assert_eq!(SolarMonth::December, SolarMonth::parse_str("十二月").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("一月", SolarMonth::January.to_str());
    assert_eq!("二月", SolarMonth::February.to_str());
    assert_eq!("五月", SolarMonth::May.to_str());
    assert_eq!("十二月", SolarMonth::December.to_str());
}

#[test]
fn from_u8() {
    assert_eq!(SolarMonth::January, SolarMonth::from_u8(1).unwrap());
    assert_eq!(SolarMonth::February, SolarMonth::from_u8(2).unwrap());
    assert_eq!(SolarMonth::May, SolarMonth::from_u8(5).unwrap());
    assert_eq!(SolarMonth::December, SolarMonth::from_u8(12).unwrap());
}

#[test]
fn to_u8() {
    assert_eq!(1, SolarMonth::January.to_u8());
    assert_eq!(2, SolarMonth::February.to_u8());
    assert_eq!(5, SolarMonth::May.to_u8());
    assert_eq!(12, SolarMonth::December.to_u8());
}

#[test]
fn get_total_days() {
    assert_eq!(31, SolarMonth::January.get_total_days(2000.into()));
    assert_eq!(29, SolarMonth::February.get_total_days(2000.into()));
    assert_eq!(31, SolarMonth::March.get_total_days(2000.into()));
    assert_eq!(30, SolarMonth::April.get_total_days(2000.into()));
    assert_eq!(30, SolarMonth::November.get_total_days(2000.into()));
    assert_eq!(31, SolarMonth::December.get_total_days(2000.into()));
    assert_eq!(31, SolarMonth::January.get_total_days(2100.into()));
    assert_eq!(28, SolarMonth::February.get_total_days(2100.into()));
    assert_eq!(31, SolarMonth::March.get_total_days(2100.into()));
    assert_eq!(30, SolarMonth::April.get_total_days(2100.into()));
    assert_eq!(30, SolarMonth::November.get_total_days(2100.into()));
    assert_eq!(31, SolarMonth::December.get_total_days(2100.into()));
}
