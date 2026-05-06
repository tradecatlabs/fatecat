use chinese_lunisolar_calendar::{EarthlyBranch, HeavenlyStems, LunarYear};

#[test]
fn parse_str() {
    let lunar_year = LunarYear::parse_str("甲午").unwrap();

    assert_eq!(HeavenlyStems::First, lunar_year.to_heavenly_stems());
    assert_eq!(EarthlyBranch::Seventh, lunar_year.to_earthly_branch());
}

#[test]
fn to_str() {
    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::First).unwrap();
    assert_eq!("甲子", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::Eleventh).unwrap();
    assert_eq!("甲戌", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::Third, EarthlyBranch::First).unwrap();
    assert_eq!("丙子", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::Ninth).unwrap();
    assert_eq!("甲申", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::Fifth, EarthlyBranch::First).unwrap();
    assert_eq!("戊子", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::Seventh).unwrap();
    assert_eq!("甲午", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::Sixth, EarthlyBranch::Twelfth).unwrap();
    assert_eq!("己亥", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::Seventh, EarthlyBranch::First).unwrap();
    assert_eq!("庚子", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::Fifth).unwrap();
    assert_eq!("甲辰", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::Ninth, EarthlyBranch::First).unwrap();
    assert_eq!("壬子", lunar_year.to_str());

    let lunar_year = LunarYear::from_era(HeavenlyStems::First, EarthlyBranch::Third).unwrap();
    assert_eq!("甲寅", lunar_year.to_str());
}
