use chinese_lunisolar_calendar::SolarDay;

#[test]
fn parse_str() {
    assert_eq!(SolarDay::First, SolarDay::parse_str("一").unwrap());
    assert_eq!(SolarDay::Second, SolarDay::parse_str("二").unwrap());
    assert_eq!(SolarDay::Fifth, SolarDay::parse_str("五").unwrap());
    assert_eq!(SolarDay::ThirtyFirst, SolarDay::parse_str("三十一").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("一", SolarDay::First.to_str());
    assert_eq!("二", SolarDay::Second.to_str());
    assert_eq!("五", SolarDay::Fifth.to_str());
    assert_eq!("三十一", SolarDay::ThirtyFirst.to_str());
}

#[test]
fn from_u8() {
    assert_eq!(SolarDay::First, SolarDay::from_u8(1).unwrap());
    assert_eq!(SolarDay::Second, SolarDay::from_u8(2).unwrap());
    assert_eq!(SolarDay::Fifth, SolarDay::from_u8(5).unwrap());
    assert_eq!(SolarDay::ThirtyFirst, SolarDay::from_u8(31).unwrap());
}

#[test]
fn to_u8() {
    assert_eq!(1, SolarDay::First.to_u8());
    assert_eq!(2, SolarDay::Second.to_u8());
    assert_eq!(5, SolarDay::Fifth.to_u8());
    assert_eq!(31, SolarDay::ThirtyFirst.to_u8());
}
