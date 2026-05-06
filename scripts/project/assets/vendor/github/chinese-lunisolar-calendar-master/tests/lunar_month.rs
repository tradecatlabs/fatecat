use chinese_lunisolar_calendar::{ChineseVariant, LunarMonth, LunisolarYear};

#[test]
fn parse_str() {
    assert_eq!(LunarMonth::First, LunarMonth::parse_str("正月").unwrap());
    assert_eq!(LunarMonth::Second, LunarMonth::parse_str("二月").unwrap());
    assert_eq!(LunarMonth::Fifth, LunarMonth::parse_str("五月").unwrap());
    assert_eq!(LunarMonth::Sixth, LunarMonth::parse_str("六月").unwrap());
    assert_eq!(LunarMonth::Twelfth, LunarMonth::parse_str("臘月").unwrap());
    assert_eq!(LunarMonth::Twelfth, LunarMonth::parse_str("腊月").unwrap());
    assert_eq!(LunarMonth::LeapFirst, LunarMonth::parse_str("閏一月").unwrap());
    assert_eq!(LunarMonth::LeapSecond, LunarMonth::parse_str("閏二月").unwrap());
    assert_eq!(LunarMonth::LeapFifth, LunarMonth::parse_str("閏五月").unwrap());
    assert_eq!(LunarMonth::LeapSixth, LunarMonth::parse_str("閏六月").unwrap());
    assert_eq!(LunarMonth::LeapTwelfth, LunarMonth::parse_str("閏臘月").unwrap());
    assert_eq!(LunarMonth::LeapTwelfth, LunarMonth::parse_str("闰腊月").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("正月", LunarMonth::First.to_str(ChineseVariant::Traditional));
    assert_eq!("二月", LunarMonth::Second.to_str(ChineseVariant::Traditional));
    assert_eq!("五月", LunarMonth::Fifth.to_str(ChineseVariant::Traditional));
    assert_eq!("六月", LunarMonth::Sixth.to_str(ChineseVariant::Traditional));
    assert_eq!("臘月", LunarMonth::Twelfth.to_str(ChineseVariant::Traditional));
    assert_eq!("腊月", LunarMonth::Twelfth.to_str(ChineseVariant::Simple));
    assert_eq!("閏正月", LunarMonth::LeapFirst.to_str(ChineseVariant::Traditional));
    assert_eq!("閏二月", LunarMonth::LeapSecond.to_str(ChineseVariant::Traditional));
    assert_eq!("閏五月", LunarMonth::LeapFifth.to_str(ChineseVariant::Traditional));
    assert_eq!("閏六月", LunarMonth::LeapSixth.to_str(ChineseVariant::Traditional));
    assert_eq!("閏臘月", LunarMonth::LeapTwelfth.to_str(ChineseVariant::Traditional));
    assert_eq!("闰腊月", LunarMonth::LeapTwelfth.to_str(ChineseVariant::Simple));
}

#[test]
fn from_u8_with_leap() {
    assert_eq!(LunarMonth::First, LunarMonth::from_u8_with_leap(1, false).unwrap());
    assert_eq!(LunarMonth::Second, LunarMonth::from_u8_with_leap(2, false).unwrap());
    assert_eq!(LunarMonth::Fifth, LunarMonth::from_u8_with_leap(5, false).unwrap());
    assert_eq!(LunarMonth::Sixth, LunarMonth::from_u8_with_leap(6, false).unwrap());
    assert_eq!(LunarMonth::Twelfth, LunarMonth::from_u8_with_leap(12, false).unwrap());
    assert_eq!(LunarMonth::LeapFirst, LunarMonth::from_u8_with_leap(1, true).unwrap());
    assert_eq!(LunarMonth::LeapSecond, LunarMonth::from_u8_with_leap(2, true).unwrap());
    assert_eq!(LunarMonth::LeapFifth, LunarMonth::from_u8_with_leap(5, true).unwrap());
    assert_eq!(LunarMonth::LeapSixth, LunarMonth::from_u8_with_leap(6, true).unwrap());
    assert_eq!(LunarMonth::LeapTwelfth, LunarMonth::from_u8_with_leap(12, true).unwrap());
}

#[test]
fn to_u8() {
    assert_eq!(1, LunarMonth::First.to_u8());
    assert_eq!(2, LunarMonth::Second.to_u8());
    assert_eq!(5, LunarMonth::Fifth.to_u8());
    assert_eq!(6, LunarMonth::Sixth.to_u8());
    assert_eq!(12, LunarMonth::Twelfth.to_u8());
    assert_eq!(1, LunarMonth::LeapFirst.to_u8());
    assert_eq!(2, LunarMonth::LeapSecond.to_u8());
    assert_eq!(5, LunarMonth::LeapFifth.to_u8());
    assert_eq!(6, LunarMonth::LeapSixth.to_u8());
    assert_eq!(12, LunarMonth::LeapTwelfth.to_u8());
}

#[test]
fn get_total_days() {
    assert_eq!(
        Some(30),
        LunarMonth::Fourth.get_total_days(LunisolarYear::from_solar_year(2020.into()).unwrap())
    );
    assert_eq!(
        Some(29),
        LunarMonth::LeapFourth.get_total_days(LunisolarYear::from_solar_year(2020.into()).unwrap())
    );
    assert_eq!(
        Some(30),
        LunarMonth::Fifth.get_total_days(LunisolarYear::from_solar_year(2020.into()).unwrap())
    );
}
