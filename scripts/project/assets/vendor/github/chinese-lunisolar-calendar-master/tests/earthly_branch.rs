use chinese_lunisolar_calendar::{chrono::prelude::*, EarthlyBranch, Zodiac};

#[test]
fn parse_str() {
    assert_eq!(EarthlyBranch::First, EarthlyBranch::parse_str("子").unwrap());
    assert_eq!(EarthlyBranch::Second, EarthlyBranch::parse_str("丑").unwrap());
    assert_eq!(EarthlyBranch::Fifth, EarthlyBranch::parse_str("辰").unwrap());
    assert_eq!(EarthlyBranch::Twelfth, EarthlyBranch::parse_str("亥").unwrap());
}

#[test]
fn from_time() {
    assert_eq!(
        EarthlyBranch::First,
        EarthlyBranch::from_time(NaiveTime::from_hms_opt(23, 30, 0).unwrap())
    );
    assert_eq!(
        EarthlyBranch::Second,
        EarthlyBranch::from_time(NaiveTime::from_hms_opt(1, 30, 0).unwrap())
    );
    assert_eq!(
        EarthlyBranch::Fifth,
        EarthlyBranch::from_time(NaiveTime::from_hms_opt(7, 0, 1).unwrap())
    );
    assert_eq!(
        EarthlyBranch::Twelfth,
        EarthlyBranch::from_time(NaiveTime::from_hms_opt(22, 0, 0).unwrap())
    );
}

#[test]
fn to_str() {
    assert_eq!("子", EarthlyBranch::First.to_str());
    assert_eq!("丑", EarthlyBranch::Second.to_str());
    assert_eq!("辰", EarthlyBranch::Fifth.to_str());
    assert_eq!("亥", EarthlyBranch::Twelfth.to_str());
}

#[test]
fn from_char() {
    assert_eq!(EarthlyBranch::First, EarthlyBranch::from_char('子').unwrap());
    assert_eq!(EarthlyBranch::Second, EarthlyBranch::from_char('丑').unwrap());
    assert_eq!(EarthlyBranch::Fifth, EarthlyBranch::from_char('辰').unwrap());
    assert_eq!(EarthlyBranch::Twelfth, EarthlyBranch::from_char('亥').unwrap());
}

#[test]
fn to_char() {
    assert_eq!('子', EarthlyBranch::First.to_char());
    assert_eq!('丑', EarthlyBranch::Second.to_char());
    assert_eq!('辰', EarthlyBranch::Fifth.to_char());
    assert_eq!('亥', EarthlyBranch::Twelfth.to_char());
}

#[test]
fn from_zodiac() {
    assert_eq!(EarthlyBranch::First, EarthlyBranch::from_zodiac(Zodiac::Rat),);
    assert_eq!(EarthlyBranch::Second, EarthlyBranch::from_zodiac(Zodiac::Ox));
    assert_eq!(EarthlyBranch::Fifth, EarthlyBranch::from_zodiac(Zodiac::Dragon));
    assert_eq!(EarthlyBranch::Twelfth, EarthlyBranch::from_zodiac(Zodiac::Pig));
}

#[test]
fn to_zodiac() {
    assert_eq!(Zodiac::Rat, EarthlyBranch::First.to_zodiac());
    assert_eq!(Zodiac::Ox, EarthlyBranch::Second.to_zodiac());
    assert_eq!(Zodiac::Dragon, EarthlyBranch::Fifth.to_zodiac());
    assert_eq!(Zodiac::Pig, EarthlyBranch::Twelfth.to_zodiac());
}
