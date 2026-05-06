//! Based on 5 elements in nature with its 陰 (Yin) and
//! 陽 (Yang) for each, ancient Chinese described the
//! plant growth using 10 conventional symbols known as
//! "10 Gan" (十干). Also, they tracked the motion of
//! Jupiter (which has 12 year cycle) and so they did
//! divided the night sky into 12 regions, and this is
//! known as "12 Zhi" (十二支). When they record time
//! and space, they used the combinations of 10 Gan (干)
//! and 12 Zhi (支) which makes 60 patterns, and this
//! is called 干支 (Gan-Zhi).
//!
//! 10 Gan (干):
//!
//! [0] 甲 (Jia)  
//! [1] 乙 (Yi)  
//! [2] 丙 (Bing)  
//! [3] 丁 (Ding)  
//! [4] 戊 (Wu)  
//! [5] 己 (Ji)  
//! [6] 庚 (Geng)  
//! [7] 辛 (Xin)  
//! [8] 壬 (Ren)  
//! [9] 癸 (Gui)  
//!
//! 12 Zhi (支):
//!
//! [0] 子 (Zi)  
//! [1] 丑 (Chou)  
//! [2] 寅 (Yin)  
//! [3] 卯 (Mao)  
//! [4] 辰 (Chen)  
//! [5] 巳 (Si)  
//! [6] 午 (Wu)  
//! [7] 未 (Wei)  
//! [8] 申 (Shen)  
//! [9] 酉 (You)  
//! [10] 戌 (Xu)  
//! [11] 亥 (Hai)  

use chrono::naive::{NaiveDate, NaiveTime};
use chrono::offset::{FixedOffset, Utc};
use chrono::{DateTime, Datelike, Timelike};
use serde::{Deserialize, Serialize};

use sowngwala::time::{
    julian_day_from_generic_date,
    julian_day_from_generic_datetime,
    modified_julian_day_from_generic_datetime,
    naive_date_from_generic_datetime,
    naive_time_from_generic_datetime, utc_from_fixed,
};

use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};

use crate::solar_terms::get_lichun;

use crate::utils::{
    get_json, longitude_of_the_sun_from_generic_date,
};

/// A struct representing 干 (Gan) or "Stem" and stores
/// its attributes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Stem {
    pub num: u8,
    pub name: Language,
}

/// A struct representing 支 (Zhi) or "Branch" and
/// stores its attributes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Branch {
    pub num: u8,
    pub name: Language,
}

/// A temporary struct for loading JSON data when
/// defining a static const `STEMS`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StemRawData {
    pub num: u8,
    pub name: LanguageData,
}

/// A temporary struct for loading JSON data when
/// defining a static const `BRANCHES`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BranchRawData {
    pub num: u8,
    pub name: LanguageData,
}

impl NameDataTrait for StemRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for BranchRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

/// A struct for holding `Stem` and `Branch`, or denoted
/// as 干支 (Gan-Zhi).
#[derive(Debug, Serialize)]
pub struct GanZhi<'a> {
    pub stem: &'a Stem,
    pub branch: &'a Branch,
}

/// A struct representing 八字 (Bazi) and stores `GanZhi`
/// as its attributes. It is referred as "The Four
/// Pillars of Destiny" in English mainly because the
/// structure of 八字 (Bazi) necessary for divinations
/// in 四柱命理学 (_"The Four Pillars of Destiny"_).
#[derive(Debug, Serialize)]
pub struct Bazi<'a> {
    pub year: GanZhi<'a>,
    pub month: GanZhi<'a>,
    pub day: GanZhi<'a>,
    pub hour: GanZhi<'a>,
}

impl LanguageTrait for Stem {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl LanguageTrait for Branch {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl GanZhi<'_> {
    /// Concatenate Stem & Branch (for Chinese
    /// characters)
    #[allow(dead_code)]
    fn alphabet(&self) -> String {
        format!(
            "{}{}",
            self.stem.alphabet(),
            self.branch.alphabet()
        )
    }

    /// Concatenate Stem & Branch (for Chinese
    /// phonetics)
    #[allow(dead_code)]
    fn phonetic(&self) -> String {
        format!(
            "{} {}",
            self.stem.phonetic(),
            self.branch.phonetic()
        )
    }

    /// Concatenate Stem & Branch (for Japanese
    /// characters)
    #[allow(dead_code)]
    fn alphabet_ja(&self) -> String {
        format!(
            "{}・{}",
            self.stem.alphabet_ja(),
            self.branch.alphabet_ja()
        )
    }
}

impl<'a> Bazi<'a> {
    fn new(
        year: GanZhi<'a>,
        month: GanZhi<'a>,
        day: GanZhi<'a>,
        hour: GanZhi<'a>,
    ) -> Self {
        Bazi {
            year,
            month,
            day,
            hour,
        }
    }

    /// Returns `Bazi` from localtime (`DateTime`) and
    /// zone (`i8`).
    ///
    /// Example:
    /// ```rust
    /// use chrono::DateTime;
    /// use sowngwala::time::build_fixed;
    /// use chrono::offset::FixedOffset;
    /// use mikaboshi::ganzhi::Bazi;
    /// use wasm_bindgen::prelude::*;
    ///
    /// #[wasm_bindgen]
    /// pub fn get_bazi(params: &JsValue) -> JsValue {
    ///   let nanosecond: u32 = 0;
    ///   let zone: i32 = 9;
    ///
    ///   let fixed: DateTime<FixedOffset> =
    ///       build_fixed(
    ///           1985, 11, 5, 1, 35, 0, nanosecond, zone,
    ///       );
    ///   JsValue::from_serde(
    ///     &Bazi::from_fixed(fixed)
    ///   ).unwrap()
    /// }
    /// ```
    pub fn from_fixed(
        fixed: DateTime<FixedOffset>,
    ) -> Bazi<'a> {
        let utc = utc_from_fixed(fixed);
        let year = get_year_ganzhi(utc);
        let month = get_month_ganzhi(
            Box::new(utc),
            year.stem.num,
        );
        let day = get_day_ganzhi(Box::new(utc));
        let hour = get_hour_ganzhi(
            Box::new(
                naive_time_from_generic_datetime(
                    fixed,
                ),
            ),
            day.stem.num,
        );

        Bazi::new(year, month, day, hour)
    }

    pub fn from_utc(
        utc: DateTime<Utc>,
        t: NaiveTime,
    ) -> Bazi<'a> {
        let year = get_year_ganzhi(utc);
        let month = get_month_ganzhi(
            Box::new(utc),
            year.stem.num,
        );
        let day = get_day_ganzhi(Box::new(utc));
        let hour = get_hour_ganzhi(
            Box::new(t),
            day.stem.num,
        );

        Bazi::new(year, month, day, hour)
    }
}

lazy_static! {
    /// A static vector with 60 items. `Vec<usize, usize>`
    /// where the first `usize` being the `STEMS` index,
    /// and the second for the `BRANCHES`. It is simply
    /// the combination of 10 stems and 12 branches
    /// which eventually adds up to 60 patterns.
    pub static ref GANZHI_SEXAGESIMAL: Vec<(usize, usize)> = {
        let mut v = vec![];
        for i in 0..60 {
            let stem = (i % 10) as usize;
            let branch = (i % 12) as usize;
            v.push((stem, branch));
        }
        v
    };

    /// A static vector with 10 items, each represents
    /// 干 (Gan). Each stores associated attributes for
    /// the 干 (Gan).
    ///
    /// [0] 甲 (Jia)
    /// [1] 乙 (Yi)
    /// [2] 丙 (Bing)
    /// [3] 丁 (Ding)
    /// [4] 戊 (Wu)
    /// [5] 己 (Ji)
    /// [6] 庚 (Geng)
    /// [7] 辛 (Xin)
    /// [8] 壬 (Ren)
    /// [9] 癸 (Gui)
    ///
    /// For attributes details stored in the vector is
    /// found in JSON file:
    /// `src/json/ganzhi_stems.json`
    pub static ref STEMS: Vec<Stem> = {
        let json = &include_str!("../json/ganzhi_stems.json");
        let data: Vec<StemRawData> = get_json::<StemRawData>(json);
        data.iter().map(|item| {
            let item = item.clone();
            Stem {
                num: item.num,
                name: item.language_from_data(),
            }
        }).collect()
    };

    /// A static vector with 10 items, each represents 支
    /// (Zhi). Each stores associated attributes for the
    /// 支 (Zhi).
    ///
    /// [0] 子 (Zi)
    /// [1] 丑 (Chou)
    /// [2] 寅 (Yin)
    /// [3] 卯 (Mao)
    /// [4] 辰 (Chen)
    /// [5] 巳 (Si)
    /// [6] 午 (Wu)
    /// [7] 未 (Wei)
    /// [8] 申 (Shen)
    /// [9] 酉 (You)
    /// [10] 戌 (Xu)
    /// [11] 亥 (Hai)
    ///
    /// For attributes details stored in the vector is found in JSON file:
    /// `src/json/ganzhi_branches.json`
    pub static ref BRANCHES: Vec<Branch> = {
        let json = &include_str!("../json/ganzhi_branches.json");
        let data: Vec<BranchRawData> = get_json::<BranchRawData>(json);
        data.iter().map(|item| {
            let item = item.clone();
            Branch {
                num: item.num,
                name: item.language_from_data(),
            }
        }).collect()
    };

    /// This is a table used when finding "Hour Stem".
    /// Columns represents "Day Stem" groups, and
    /// there are 5 groups. For insntace, if you have
    /// 甲 for "Day Stem", you are looking into the
    /// first column (group). Rows represents "Hour
    /// Branches" for which there are 12. For instance,
    /// if you have 子 for "Hour Branch", you are
    /// looking into the first row. So, when you have
    /// 甲 for "Day Stem", and 子 for "Hour Branch",
    /// "Hour Stem" is located in the first column in
    /// the first row, which is 甲.
    ///
    /// &nbsp; &nbsp; &nbsp; 甲乙丙丁戊
    /// &nbsp; &nbsp; &nbsp; 己庚辛壬癸
    /// &dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;
    /// 子: 甲丙戊庚壬
    /// 丑: 乙丁己辛癸
    /// 寅: 丙戊庚壬甲
    /// 卯: 丁己辛癸乙
    /// 辰: 戊庚壬甲丙
    /// 巳: 己辛癸乙丁
    /// 午: 庚壬甲丙戊
    /// 未: 辛癸乙丁己
    /// 申: 壬甲丙戊庚
    /// 酉: 癸乙丁己辛
    /// 戌: 甲丙戊庚壬
    /// 亥: 乙丁己辛癸
    pub static ref HOUR_STEM_TABLE: [[usize; 5]; 12] = [
        // 子
        [0, 2, 4, 6, 8], // 甲丙戊庚壬
        // 丑
        [1, 3, 5, 7, 9], // 乙丁己辛癸
        // 寅
        [2, 4, 6, 8, 0], // 丙戊庚壬甲
        // 卯
        [3, 5, 7, 9, 1], // 丁己辛癸乙
        // 辰
        [4, 6, 8, 0, 2], // 戊庚壬甲丙
        // 巳
        [5, 7, 9, 1, 3], // 己辛癸乙丁
        // 午
        [6, 8, 0, 2, 4], // 庚壬甲丙戊
        // 未
        [7, 9, 1, 3, 5], // 辛癸乙丁己
        // 申
        [8, 0, 2, 4, 6], // 壬甲丙戊庚
        // 酉
        [9, 1, 3, 5, 7], // 癸乙丁己辛
        // 戌
        [0, 2, 4, 6, 8], // 甲丙戊庚壬
        // 亥
        [1, 3, 5, 7, 9], // 乙丁己辛癸
    ];
}

/// Year Ganzhi
fn get_year_ganzhi(
    utc: DateTime<Utc>,
) -> GanZhi<'static> {
    // Year Stem and Branch are easily found.
    // However, we must watch out if it is before
    // or after Lichun. The year begins from Lichun,
    // and it belongs to last year if the date
    // is before Lichun.
    let lichun: NaiveDate = get_lichun(utc.year());

    let year: i32 =
        if julian_day_from_generic_datetime(utc)
            < julian_day_from_generic_date(lichun)
        {
            utc.year() - 1
        } else {
            utc.year()
        };

    // Stem is found from the last digit of the year.
    // 0   1   2   3   4   5   6   7   8  9
    // 庚  辛  壬  癸  甲  乙  丙  丁  戊  己
    let digits: Vec<_> = year
        .to_string()
        .chars()
        .map(|d| d.to_digit(10).unwrap())
        .collect();

    let last = *digits.last().unwrap();

    // Brach is found simply if we know the year,
    // but once again, it depends on Lichun.
    // 0   1   2   3   4   5   6   7   8  9   10  11
    // 申  酉  戌  亥  子  丑  寅  卯  辰  巳  午  未
    GanZhi {
        stem: &STEMS[((last + 6) % 10) as usize],
        branch: &BRANCHES[((year + 8) % 12) as usize],
    }
}

/// Month Ganzhi
#[allow(clippy::boxed_local)]
fn get_month_ganzhi(
    utc: Box<DateTime<Utc>>,
    year_stem_num: u8,
) -> GanZhi<'static> {
    let utc = *utc;

    let lng: f64 =
        longitude_of_the_sun_from_generic_date(
            naive_date_from_generic_datetime(utc),
        );

    // Branch is easily found by looking at the
    // longitude of the sun.
    let branch_index: usize =
        if (315.0..345.0).contains(&lng) {
            0 // 立春 (lichun) + 雨水 (yushui) ---> 寅 (yin)
        } else if !(15.0..345.0).contains(&lng) {
            1 // 啓蟄 (jingzhe) + 春分 (chunfen) ---> 卯 (mao)
        } else if (15.0..45.0).contains(&lng) {
            2 // 清明 (qingming) + 穀雨 (guyu) ---> 辰 (chen)
        } else if (45.0..75.0).contains(&lng) {
            3 // 立夏 (lixia) + 小滿 (xiaoman) ---> 巳 (si)
        } else if (75.0..105.0).contains(&lng) {
            4 // 芒種 (mangzhong) + 夏至 (xiazhi) ---> 午 (wu)
        } else if (105.0..135.0).contains(&lng) {
            5 // 小暑 (xiaoshu) + 大暑 (dashu) ---> 未 (wei)
        } else if (135.0..165.0).contains(&lng) {
            6 // 立秋 (liqiu) + 處暑 (chushu) ---> 申 (shen)
        } else if (165.0..195.0).contains(&lng) {
            7 // 白露 (bailu) + 秋分 (qiufen) ---> 酉 (you)
        } else if (195.0..225.0).contains(&lng) {
            8 // 寒露 (hanlu) + 霜降 (shuangjiang) ---> 戌 (xu)
        } else if (225.0..255.0).contains(&lng) {
            9 // 立冬 (lidong) + 小雪 (xiaoxue) ---> 亥 (hai)
        } else if (255.0..285.0).contains(&lng) {
            10 // 大雪 (daxue) + 冬至 (dongzhi) ---> 子 (zi)
        } else {
            // lng >= 285.0 || lng < 315.0
            11 // 小寒 (xiaohan) + 大寒 (dahan) ---> 丑 (chou)
        };

    // Stem is found using the Year Stem. For a given
    // year, you can find the first Month Stem. Once
    // you find the first Month Stem, you simply count
    // up to the current month. This is done by adding
    // 'branch_id' because 'branch_id' is nothing but
    // how many month from the beginning (Lichun).
    let stem_index: usize = if year_stem_num == 1
        || year_stem_num == 6
    {
        2 // 甲(jia:1) or 己(ji:6) ---> 丙(bing:3)
    } else if year_stem_num == 2 || year_stem_num == 7
    {
        4 // 乙(yi:2) or 庚(geng:7) ---> 戊(wu:5)
    } else if year_stem_num == 3 || year_stem_num == 8
    {
        6 // 丙(bing:3) or 辛(xin:8) ---> 庚(geng:7)
    } else if year_stem_num == 4 || year_stem_num == 9
    {
        8 // 丁(ding:4) or 壬(ren:9) ---> 壬(ren:9)
    } else {
        0 // 戊(wu:5) or 癸(gui:10) ---> 甲(jia:1)
    };

    GanZhi {
        stem: &STEMS
            [(stem_index + branch_index) % 10],
        branch: &BRANCHES[(branch_index + 2) % 12],
    }
}

/// Day Ganzhi
#[allow(clippy::boxed_local)]
fn get_day_ganzhi(
    utc: Box<DateTime<Utc>>,
) -> GanZhi<'static> {
    let utc = *utc;
    let mjd: f64 =
        modified_julian_day_from_generic_datetime(
            utc,
        );
    let index =
        ((mjd - 10.0) % 60.0).floor() as usize;

    let (stem_id, branch_id) =
        GANZHI_SEXAGESIMAL[index];

    GanZhi {
        stem: &STEMS[stem_id],
        branch: &BRANCHES[branch_id],
    }
}

/// Hour Ganzhi
#[allow(clippy::boxed_local)]
fn get_hour_ganzhi(
    t: Box<NaiveTime>,
    day_stem_num: u8,
) -> GanZhi<'static> {
    // The branch is easily found by looking at the
    // hour range of the day.
    let branch_id: usize =
        if t.hour() == 23 || t.hour() == 0 {
            0
        } else if t.hour() < 3 {
            1
        } else if t.hour() <= 4 {
            2
        } else if t.hour() <= 6 {
            3
        } else if t.hour() <= 8 {
            4
        } else if t.hour() <= 10 {
            5
        } else if t.hour() <= 12 {
            6
        } else if t.hour() <= 14 {
            7
        } else if t.hour() <= 16 {
            8
        } else if t.hour() <= 18 {
            9
        } else if t.hour() <= 20 {
            10
        } else {
            11 // if t.hour() <= 22
        };

    // The stem is found by looking at a special
    // table. Read comments for 'HOUR_STEM_TABLE' for
    // details.
    let group_id: usize = if day_stem_num == 1
        || day_stem_num == 6
    {
        0
    } else if day_stem_num == 2 || day_stem_num == 7 {
        1
    } else if day_stem_num == 3 || day_stem_num == 8 {
        2
    } else if day_stem_num == 4 || day_stem_num == 9 {
        3
    } else {
        4 // day_stem_num == 5 || day_stem_num == 10
    };

    let stem_id: usize =
        HOUR_STEM_TABLE[branch_id][group_id];

    GanZhi {
        stem: &STEMS[stem_id],
        branch: &BRANCHES[branch_id],
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sowngwala::time::{build_fixed, build_utc};

    // TODO: GANZHI_SEXAGESIMAL

    #[test]
    fn test_constant_stems() {
        assert_eq!(STEMS[0].num, 1);
    }

    #[test]
    fn test_constant_branches() {
        assert_eq!(BRANCHES[0].num, 1);
    }

    // TODO: HOUR_STEM_TABLE

    #[test]
    fn test_bazi_from_fixed() {
        let nanosecond: u32 = 137_790_000;
        let zone: i32 = 9;

        let fixed: DateTime<FixedOffset> =
            build_fixed(
                2021, 7, 6, 14, 57, 17, nanosecond,
                zone,
            );

        let bazi: Bazi = Bazi::from_fixed(fixed);

        let year: GanZhi = bazi.year;
        let month: GanZhi = bazi.month;
        let day: GanZhi = bazi.day;
        let hour: GanZhi = bazi.hour;

        println!("fixed: {:?}", fixed);
        println!(
            "年: {} ({})",
            year.alphabet(),
            year.alphabet_ja()
        );
        println!(
            "月: {} ({})",
            month.alphabet(),
            month.alphabet_ja()
        );
        println!(
            "日: {} ({})",
            day.alphabet(),
            day.alphabet_ja()
        );
        println!(
            "時: {} ({})",
            hour.alphabet(),
            hour.alphabet_ja()
        );

        assert_eq!(year.alphabet(), "辛丑");
        assert_eq!(month.alphabet(), "甲午");
        assert_eq!(day.alphabet(), "乙卯");
        assert_eq!(hour.alphabet(), "癸未");
    }

    #[test]
    fn test_bazi_from_utc() {
        let nanosecond: u32 = 275_570_000;
        let utc: DateTime<Utc> = build_utc(
            2021, 7, 6, 5, 54, 34, nanosecond,
        );

        // Local Time
        let nanosecond: u32 = 137_790_000;
        let t = NaiveTime::from_hms_nano(
            14, 57, 17, nanosecond,
        );

        let bazi: Bazi = Bazi::from_utc(utc, t);

        let year: GanZhi = bazi.year;
        let month: GanZhi = bazi.month;
        let day: GanZhi = bazi.day;
        let hour: GanZhi = bazi.hour;

        println!("utc: {:?}", utc);
        println!("t: {:?}", t);

        println!(
            "年: {} ({})",
            year.alphabet(),
            year.alphabet_ja()
        );
        println!(
            "月: {} ({})",
            month.alphabet(),
            month.alphabet_ja()
        );
        println!(
            "日: {} ({})",
            day.alphabet(),
            day.alphabet_ja()
        );
        println!(
            "時: {} ({})",
            hour.alphabet(),
            hour.alphabet_ja()
        );

        assert_eq!(year.alphabet(), "辛丑");
        assert_eq!(month.alphabet(), "甲午");
        assert_eq!(day.alphabet(), "乙卯");
        assert_eq!(hour.alphabet(), "癸未");
    }
}
