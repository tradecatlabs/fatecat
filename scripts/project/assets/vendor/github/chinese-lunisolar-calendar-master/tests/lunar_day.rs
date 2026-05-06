use chinese_lunisolar_calendar::LunarDay;

#[test]
fn parse_str() {
    assert_eq!(LunarDay::First, LunarDay::parse_str("初一").unwrap());
    assert_eq!(LunarDay::Second, LunarDay::parse_str("初二").unwrap());
    assert_eq!(LunarDay::Fifth, LunarDay::parse_str("初五").unwrap());
    assert_eq!(LunarDay::Thirty, LunarDay::parse_str("三十").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("初一", LunarDay::First.to_str());
    assert_eq!("初二", LunarDay::Second.to_str());
    assert_eq!("初五", LunarDay::Fifth.to_str());
    assert_eq!("三十", LunarDay::Thirty.to_str());
}

#[test]
fn from_u8() {
    assert_eq!(LunarDay::First, LunarDay::from_u8(1).unwrap());
    assert_eq!(LunarDay::Second, LunarDay::from_u8(2).unwrap());
    assert_eq!(LunarDay::Fifth, LunarDay::from_u8(5).unwrap());
    assert_eq!(LunarDay::Thirty, LunarDay::from_u8(30).unwrap());
}

#[test]
fn to_u8() {
    assert_eq!(1, LunarDay::First.to_u8());
    assert_eq!(2, LunarDay::Second.to_u8());
    assert_eq!(5, LunarDay::Fifth.to_u8());
    assert_eq!(30, LunarDay::Thirty.to_u8());
}
