use chinese_lunisolar_calendar::HeavenlyStems;

#[test]
fn parse_str() {
    assert_eq!(HeavenlyStems::First, HeavenlyStems::parse_str("甲").unwrap());
    assert_eq!(HeavenlyStems::Second, HeavenlyStems::parse_str("乙").unwrap());
    assert_eq!(HeavenlyStems::Fifth, HeavenlyStems::parse_str("戊").unwrap());
    assert_eq!(HeavenlyStems::Tenth, HeavenlyStems::parse_str("癸").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("甲", HeavenlyStems::First.to_str());
    assert_eq!("乙", HeavenlyStems::Second.to_str());
    assert_eq!("戊", HeavenlyStems::Fifth.to_str());
    assert_eq!("癸", HeavenlyStems::Tenth.to_str());
}

#[test]
fn from_char() {
    assert_eq!(HeavenlyStems::First, HeavenlyStems::from_char('甲').unwrap());
    assert_eq!(HeavenlyStems::Second, HeavenlyStems::from_char('乙').unwrap());
    assert_eq!(HeavenlyStems::Fifth, HeavenlyStems::from_char('戊').unwrap());
    assert_eq!(HeavenlyStems::Tenth, HeavenlyStems::from_char('癸').unwrap());
}

#[test]
fn to_char() {
    assert_eq!('甲', HeavenlyStems::First.to_char());
    assert_eq!('乙', HeavenlyStems::Second.to_char());
    assert_eq!('戊', HeavenlyStems::Fifth.to_char());
    assert_eq!('癸', HeavenlyStems::Tenth.to_char());
}
