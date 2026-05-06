use chinese_lunisolar_calendar::{ChineseVariant, EarthlyBranch, Zodiac};

#[test]
fn parse_str() {
    assert_eq!(Zodiac::Rat, Zodiac::parse_str("鼠").unwrap());
    assert_eq!(Zodiac::Ox, Zodiac::parse_str("牛").unwrap());
    assert_eq!(Zodiac::Dragon, Zodiac::parse_str("龍").unwrap());
    assert_eq!(Zodiac::Dragon, Zodiac::parse_str("龙").unwrap());
    assert_eq!(Zodiac::Pig, Zodiac::parse_str("豬").unwrap());
    assert_eq!(Zodiac::Pig, Zodiac::parse_str("猪").unwrap());
}

#[test]
fn to_str() {
    assert_eq!("鼠", Zodiac::Rat.to_str(ChineseVariant::Traditional));
    assert_eq!("牛", Zodiac::Ox.to_str(ChineseVariant::Traditional));
    assert_eq!("龍", Zodiac::Dragon.to_str(ChineseVariant::Traditional));
    assert_eq!("龙", Zodiac::Dragon.to_str(ChineseVariant::Simple));
    assert_eq!("豬", Zodiac::Pig.to_str(ChineseVariant::Traditional));
    assert_eq!("猪", Zodiac::Pig.to_str(ChineseVariant::Simple));
}

#[test]
fn from_char() {
    assert_eq!(Zodiac::Rat, Zodiac::from_char('鼠').unwrap());
    assert_eq!(Zodiac::Ox, Zodiac::from_char('牛').unwrap());
    assert_eq!(Zodiac::Dragon, Zodiac::from_char('龍').unwrap());
    assert_eq!(Zodiac::Dragon, Zodiac::from_char('龙').unwrap());
    assert_eq!(Zodiac::Pig, Zodiac::from_char('豬').unwrap());
    assert_eq!(Zodiac::Pig, Zodiac::from_char('猪').unwrap());
}

#[test]
fn to_char() {
    assert_eq!('鼠', Zodiac::Rat.to_char(ChineseVariant::Traditional),);
    assert_eq!('牛', Zodiac::Ox.to_char(ChineseVariant::Traditional));
    assert_eq!('龍', Zodiac::Dragon.to_char(ChineseVariant::Traditional));
    assert_eq!('龙', Zodiac::Dragon.to_char(ChineseVariant::Simple));
    assert_eq!('豬', Zodiac::Pig.to_char(ChineseVariant::Traditional));
    assert_eq!('猪', Zodiac::Pig.to_char(ChineseVariant::Simple));
}

#[test]
fn from_earthly_branch() {
    assert_eq!(Zodiac::Rat, Zodiac::from_earthly_branch(EarthlyBranch::First));
    assert_eq!(Zodiac::Ox, Zodiac::from_earthly_branch(EarthlyBranch::Second),);
    assert_eq!(Zodiac::Dragon, Zodiac::from_earthly_branch(EarthlyBranch::Fifth));
    assert_eq!(Zodiac::Pig, Zodiac::from_earthly_branch(EarthlyBranch::Twelfth));
}

#[test]
fn to_earthly_branch() {
    assert_eq!(EarthlyBranch::First, Zodiac::Rat.to_earthly_branch());
    assert_eq!(EarthlyBranch::Second, Zodiac::Ox.to_earthly_branch());
    assert_eq!(EarthlyBranch::Fifth, Zodiac::Dragon.to_earthly_branch());
    assert_eq!(EarthlyBranch::Twelfth, Zodiac::Pig.to_earthly_branch());
}
