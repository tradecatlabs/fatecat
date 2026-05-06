//! 九星 (Jiu-Xing) means "9 stars" in Chinese.
//! In 風水 (Feng-Shui), 9 boxes are drawn to represent
//! the spatial condition of the place in concern.
//! The box in the middle represents where you are,
//! and 8 boxes which surrounding the middle represent
//! 8 compass directions. For these 9 boxes, plotted
//! special symbols, each of which is called, a "Star"
//! (星). When we say 九星 (Jiu-Xing) in Chinese, "Jiu"
//! means "9", and "Xing" means a "Star". While 九星
//! (Jiu-Xing) has fixed positions (associated with
//! 洛書 (Lo-Shu)), they change positions over time,
//! and this movement is called 飞泊 (Fei-Po) or
//! "flying" because of how it appears to our eyes when
//! they move.
//!
//! As explained in 八卦 (Ba-Gua) (see: `src/bagua.rs`),
//! there are 2 worldly systems concerned, namely,
//! 先天八卦 (or "the Primordial Heaven") and
//! 後天八卦 (or "the Manifested Heaven"), and we deal
//! with the latter system when we talk about 風水
//! (Feng-Shui).
//!
//! In 玄空飞星風水 (Xuan-Kong Fei-Xing Feng-Shui),
//! there is a special name given to the latter system,
//! and is called, 地盤 (Di-Pan). "Di" means "earth",
//! and "Pan" means "board". So, it is basically a board
//! which is drawn at the bottom of any Feng-Shui charts.
//! On 地盤 (Di-Pan), 九星 (Jiu-Xing) are plotted for
//! which the order is fundamentally that of 洛書
//! (Lo-Shu) order in 八卦 (Ba-Gua). However, they move
//! (or "fly") over 地盤 (Di-Pan) as time goes.
//! In 玄空飞星風水 (Xuan-Kong Fei-Xing Feng-Shui),
//! there are 3 other boards that are drawn on top of
//! 地盤 (Di-Pan), namely:
//!
//! - 運盤 (Un-Pan) or 天盤 (Tien-Pan)  
//! - 山星 (Shan-Xing)  
//! - 向星 (Xiang-Xing)  
//!
//! For 運盤 (Un-Pan), positions of 九星 (Jiu-Xing) are
//! determined by construction year for the building in
//! concern which is calculated based on 三元九運
//! (Sang-Yuan Jiu-Yun), or "9 Yearly Cycles". We could
//! say that 運盤 (Un-Pan) essentially describes the
//! temporal aspect. 山星 (Shan-Xing) and 向星
//! (Xiang-Xing) are determined by spatial aspects of
//! the building (however, in actual calculations, some
//! temporal aspects comes in).
//!
//! When these 3 extra boards are placed on top of 地盤
//! (Di-Pan), the whole thing is called, 下卦図
//! (Xia-Gua-Tu), or simply referred as 飞星図
//! (Fei-Xing-Tu), or "The Flying Star Chart".
//!
//! Jiu-Xing (九星):
//!
//! [0] 一白水星 (1 White)  
//! [1] 二黒土星 (2 Black)  
//! [2] 三碧木星 (3 Jade)  
//! [3] 四緑木星 (4 Green)  
//! [4] 五黄土星 (5 Yellow)  
//! [5] 六白金星 (6 White)  
//! [6] 七赤金星 (7 Red)  
//! [7] 八白土星 (8 White)  
//! [8] 九紫火星 (9 Purple)  

use chrono::naive::NaiveDate;
use chrono::Datelike;
use serde::{Deserialize, Serialize};
use sowngwala::time::julian_day_from_generic_date;
use std::collections::HashMap;
use std::convert::TryInto;

use crate::compass::{
    get_opposite_direction, DIRECTIONS,
    DIRECTION_POSITIONS_IN_CHART,
};
use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};
use crate::planet::{Planet, PLANETS};
use crate::utils::{get_json, make_positive};
use crate::wuxing::{WuXing, WU_XING};

pub const SAN_YUAN_JIU_YUN_START_YEAR: u16 = 1864;

/// A struct representing 九星 (Jiu-Xing).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JiuXing {
    pub num: u8,
    pub direction: String,
    pub name: Language,
    pub color: String,
    pub element: WuXing,
    pub planet: Planet,
}

/// A temporary struct for loading JSON data when
/// defining a static const `JIU_XING`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JiuXingRawData {
    pub num: u8,
    pub direction: String,
    pub name: LanguageData,
    pub color: String,
    pub element: u8,
    pub planet: u8,
}

impl LanguageTrait for JiuXing {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for JiuXingRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

#[derive(
    Debug, Clone, Serialize, Deserialize, Copy,
)]
pub enum XiaGuaTuKind {
    UnPanXing, // 運盤
    ShanXing,  // 山星
    XiangXing, // 向星
}

/// A struct representing 下卦図 (Xia-Gua-Tu).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct XiaGuaTu<'a> {
    pub kind: XiaGuaTuKind,
    pub center: Option<usize>,
    pub direction: Option<&'a str>,
    pub sector: Option<usize>,
    pub chart: Option<[usize; 9]>,
}

lazy_static! {
    /// A static vector with 9 items, each represents
    /// 九星 (Jiu-Xing).
    ///
    /// [0] 一白水星 (1 White)
    /// [1] 二黒土星 (2 Black)
    /// [2] 三碧木星 (3 Jade)
    /// [3] 四緑木星 (4 Green)
    /// [4] 五黄土星 (5 Yellow)
    /// [5] 六白金星 (6 White)
    /// [6] 七赤金星 (7 Red)
    /// [7] 八白土星 (8 White)
    /// [8] 九紫火星 (9 Purple)
    ///
    /// For attributes details stored in the vector is
    /// found in JSON file:
    /// `src/json/jiuxing.json`
    pub static ref JIU_XING: [JiuXing; 9] = {
        let json = &include_str!("../json/jiuxing.json");
        get_json::<JiuXingRawData>(json)
            .iter() // TODO: into_iter()?
            .map(|item| {
                JiuXing {
                    num: item.num,
                    direction: item.direction.clone(),
                    name: item.language_from_data(),
                    color: item.color.clone(),
                    element: WU_XING[item.element as usize].clone(),
                    planet: PLANETS[item.planet as usize].clone(),
                }
            })
            .collect::<Vec<JiuXing>>()
            .try_into()
            .unwrap()
    };
}

/// A getter for `JIU_XING`.
///
/// Example:
/// ```rust
/// use mikaboshi::jiuxing::{get_jiuxing_from_index, JiuXing};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(index: usize) -> JsValue {
///     let dir: &JiuXing = get_jiuxing_from_index(index);
///     JsValue::from_serde(dir).unwrap()
/// }
/// ```
pub fn get_jiuxing_from_index(
    index: usize,
) -> &'static JiuXing {
    &JIU_XING[index]
}

lazy_static! {
    pub static ref DIRECTION_TO_JIU_XING: HashMap<&'static str, usize> =
        JIU_XING
            .iter()
            .enumerate()
            .map(|(index, jiuxing)| {
                let dir = jiuxing.direction.as_str();
                match dir {
                    "" => ("", index),
                    _ => (
                        jiuxing.direction.as_str(),
                        index,
                    ),
                }
            })
            .collect();
}

fn jiuxing_index_from_direction(dir: &str) -> usize {
    match dir {
        "" => 4,
        _ => DIRECTION_TO_JIU_XING[dir],
    }
}

lazy_static! {
    /// Although 洛書 (Lo-Shu) order is fixed, when
    /// 地盤 (Di-Pan) is drawn on a device screen,
    /// the mapping for 九星 (Jiu-Xing) changes as
    /// the device rotates.
    /// For example, 一白水星 (1 White) usually comes
    /// to the top of the board when a device is
    /// pointing north. However, when pointing north
    /// east, 一白水星 (1 White) moves to the top left
    /// (which is north west). For 8 compass directions,
    /// this constant provides a mapping for the 洛書
    /// (Lo-Shu) order. For "n", 一白水星 (1 White) is
    /// the 2nd in the array. For "ne", 一白水星
    /// (1 White) is the 1st in the array.
    ///
    /// It would look like this:
    ///
    /// [5] 六白 [0] 一白 [7] 八白
    /// [6] 七赤 [4] 五黄 [2] 三碧
    /// [1] 二黒 [8] 九紫 [3] 四緑
    /// n: [5, 0, 7, 6, 4, 2, 1, 8, 3]
    ///
    /// [0] 一白 [7] 八白 [2] 三碧
    /// [5] 六白 [4] 五黄 [3] 四緑
    /// [6] 七赤 [1] 二黒 [8] 九紫
    /// ne: [0, 7, 2, 5, 4, 3, 6, 1, 8]
    ///
    /// [7] 八白 [2] 三碧 [3] 四緑
    /// [0] 一白 [4] 五黄 [8] 九紫
    /// [5] 六白 [6] 七赤 [1] 二黒
    /// e: [7, 2, 3, 0, 4, 8, 5, 6, 1]
    ///
    /// [2] 三碧 [3] 四緑 [8] 九紫
    /// [7] 八白 [4] 五黄 [1] 二黒
    /// [0] 一白 [5] 六白 [6] 七赤
    /// se: [2, 3, 8, 7, 4, 1, 0, 5, 6]
    ///
    /// [3] 四緑 [8] 九紫 [1] 二黒
    /// [2] 三碧 [4] 五黄 [6] 七赤
    /// [7] 八白 [0] 一白 [5] 六白
    /// s: [3, 8, 1, 2, 4, 6, 7, 0, 5]
    ///
    /// [8] 九紫 [1] 二黒 [6] 七赤
    /// [3] 四緑 [4] 五黄 [5] 六白
    /// [2] 三碧 [7] 八白 [0] 一白
    /// sw: [8, 1, 6, 3, 4, 5, 2, 7, 0]
    ///
    /// [1] 二黒 [6] 七赤 [5] 六白
    /// [8] 九紫 [4] 五黄 [0] 一白
    /// [3] 四緑 [2] 三碧 [7] 八白
    /// w: [1, 6, 5, 8, 4, 0, 3, 2, 7]
    ///
    /// [6] 七赤 [5] 六白 [0] 一白
    /// [1] 二黒 [4] 五黄 [7] 八白
    /// [8] 九紫 [3] 四緑 [2] 三碧
    /// nw: [6, 5, 0, 1, 4, 7, 8, 3, 2]
    pub static ref JIU_XING_DI_PAN_POSITIONS: HashMap<&'static str, [usize; 9]> = DIRECTIONS
        .iter()
        .map(|dir| -> (&str, [usize; 9]) {
            (
                dir,
                DIRECTION_POSITIONS_IN_CHART[dir]
                    .iter()
                    .map(|d| jiuxing_index_from_direction(d))
                    .collect::<Vec<usize>>()
                    .try_into()
                    .unwrap()
            )
        })
        .collect();

}

/// A getter for `JIU_XING_DI_PAN_POSITIONS`.
pub fn get_jiuxing_dipan_positions_from_direction(
    direction: &str,
) -> Option<&[usize; 9]> {
    JIU_XING_DI_PAN_POSITIONS.get(direction)
}

lazy_static! {
    /*
     * NOT IN USE
     *
     * Order for Jiu-Xing, starting north, CLOCK-WISE.
     * Since it is starting north, see bellow for
     * where each index is located:
     *
     * [7] xxx [0] xxx [1] xxx
     * [6] xxx [_] ___ [2] xxx
     * [5] xxx [4] xxx [3] xxx
     *
     * or, to be more specific, here are how Jiu-Xing
     * will be placed on the board:
     *
     * [7] 六白金星 (6 White) [0] 一白水星 (1 White)  [1] 八白土星 (8 White)
     * [6] 七赤金星 (7 Red)   [_] 五黄土星 (5 Yellow) [2] 三碧木星 (3 Jade)
     * [5] 二黒土星 (2 Black) [4] 九紫火星 (9 Purple) [3] 四緑木星 (4 Green)
     *
     * For each index means:
     *
     * [0] --> N  --> 一白水星 (1 White) [0]
     * [1] --> NE --> 八白土星 (8 White) [7]
     * [2] --> E  --> 三碧木星 (3 Jade) [2]
     * [3] --> SE --> 四緑木星 (4 Green) [3]
     * [4] --> S  --> 九紫火星 (9 Purple) [8]
     * [5] --> SW --> 二黒土星 (2 Black) [1]
     * [6] --> W  --> 七赤金星 (7 Red) [6]
     * [7] --> NW --> 六白金星 (6 White) [5]
     * pub static ref JIU_XING_DI_PAN_POSITIONS_CLOCKWISE: [usize; 8] = [0, 7, 2, 3, 8, 1, 6, 5];
     */
}

/// Given incorrect value for Jiu-Xing index, applies
/// a modulo to normalize it to fit within the range
/// of 0 to 8.  
///
/// Ex.  
///   0 -> 0 ... Stays the same. "0" being 一白水星 (1 White).  
///   8 -> 8 ... Stays the same. "8" being 九紫火星 (9 Purple).  
///   9 -> 0 ... "9" is too much for the range and becoming "0" which is 一白水星 (1 White).  
///   10 -> 1 ... "10" is too much, and becoming "1" which is 二黒土星 (2 Black).  
///   -1 -> 8 ... Making it positive. "8" being 九紫火星 (9 Purple).  
///   -2 -> 7 ... Making it positive. "8" being 八白土星 (8 White).  
pub fn normalize_jiuxing(index: i32) -> usize {
    let tmp = (make_positive(9)(index) + 1) % 9;
    match tmp {
        0 => 8,
        _ => (tmp - 1) as usize,
    }
}

/// Sang-Yuan 三元九運 (Jiu-Yun), or _"9 YEARLY
/// CYCLES"_, is the core concept in 玄空飞星風水
/// (Xuan-Kong Fei-Xing Feng-Shui), and it tells how
/// 九星 (Jiu-Xing) fly throughout 180 years.
/// This function will calculate from the given:
///
/// 1. CURRENT LOCALTIME, and  
/// 2. LIU-CHUN (for the year)  
///
/// for the corresponding Jiu-Xing, for which
/// the generated board is usually referred as
/// 運盤 (Un-Pan).
///
/// Example:
/// ```rust
/// use chrono::NaiveDate;
/// use mikaboshi::jiuxing::unpan_xing_index;
/// use mikaboshi::test_mods::DateParams;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(current: &JsValue, lichun: &JsValue) -> JsValue {
///     let params_1: DateParams = current.into_serde().unwrap();
///     let params_2: DateParams = lichun.into_serde().unwrap();
///     let current = NaiveDate::from(params_1);
///     let lichun = NaiveDate::from(params_2);
///     let index: usize = unpan_xing_index(current, lichun);
///     JsValue::from_f64(index as f64)
/// }
pub fn unpan_xing_index(
    current: NaiveDate,
    lichun: NaiveDate,
) -> usize {
    let year: i32 =
        if (julian_day_from_generic_date(current)
            - julian_day_from_generic_date(lichun))
            < 0_f64
        {
            current.year() - 1
        } else {
            current.year()
        };
    let dt: i32 =
        year - SAN_YUAN_JIU_YUN_START_YEAR as i32;
    let norm: i32 = dt % 180;
    (norm / 20) as usize
}

// /// Returns Jiu-xing (for Un-Pan)
// pub fn unpan_xing_data(&current: &Date, &lichun: &Date) -> JiuXing {
//     JIU_XING[unpan_xing_index(&current, &lichun)].clone()
// }

/// This is a function for 飞泊 (Fei-Po) or "flying".
/// The idea is quite simple. Given the order (which is
/// the second argument `order` in array) of
/// 九星 (Jiu-Xing) indexes, increments or decrements
/// each in the array, and simply return the array.
/// Depending on whichever currently resides in the
/// center of the board (which is the first argument
/// `center`), the value to increment or decrement
/// changes. For `order` is fundamentally that of the
/// Lo-Shu order (which is defined in
/// `JIU_XING_DI_PAN_POSITIONS`), however, the layout
/// is always different since the position changes
/// depending on which direction the device is
/// pointing as the device rotates.
pub fn fly_flying_stars(
    center: usize,
    order: &[usize; 9],
    reverse: bool,
) -> [usize; 9] {
    let diff: usize = center - 4;
    order
        .iter()
        .map(|index: &usize| -> usize {
            let index: usize = match reverse {
                true => 8 - *index,
                false => *index,
            } + diff;
            normalize_jiuxing(index as i32)
        })
        .collect::<Vec<usize>>()
        .try_into()
        .unwrap()
}

// fn flying_stars_chart(reverse: bool, center: usize, order: &[usize; 9]) -> [JiuXing; 9] {
//     fly_flying_stars(center, order, reverse)
//         .iter()
//         .map(|index: &usize| -> JiuXing { JIU_XING[*index].clone() })
//         .collect::<Vec<JiuXing>>()
//         .try_into()
//         .unwrap()
// }

/// This is a useful well known formula for finding out
/// whether 山星 (Shan-Xing) or 向星 (Xiang-Xing) is
/// flying in normal order.
///
/// IMPORTANT:
/// It does not work when 九星 (Jiu-Xing) is "5".
/// If such the case, center index for Un-Pan must
/// be fed.
fn is_shan_xiang_flying_normal(
    index: usize,
    sector: usize,
) -> bool {
    let num: usize = index + 1;
    let rem = num % 2;
    (rem != 0 && sector == 1)
        || (rem == 0 && sector > 1)
}

/// Looking at the 地盤 (Di-Pan) order, finds the
/// current direction facing.
fn direction_from_dipan_order(
    order: &[usize; 9],
) -> &'static str {
    JIU_XING_DI_PAN_POSITIONS
        .iter()
        .find_map(|(dir, dipan_order)| {
            match order.iter().eq(dipan_order.iter())
            {
                true => Some(*dir),
                _ => None,
            }
        })
        .unwrap_or("")
}

/// Calculates for 下卦図 (Xia-Gua-Tu). 1st and 2nd
/// arguments (`unpan_xing_center` and
/// `unpan_xing_order`) are required for all.
/// For calculating a chart for 運盤星 (Un-Pan Xing),
/// that is all we need. However, to calculate charts
/// for 山星 (Shan-Xing) and 向星 (Xiang-Xing), requires
/// 3rd and 4th arguments (`xiang_xing_direction` and
/// `xiang_xing_sector`.
///
/// Example:
/// ```rust
/// use std::collections::HashMap;
/// use std::convert::TryInto;
/// use mikaboshi::jiuxing::{get_xiaguatu_from_unpan_index, XiaGuaTu};
/// use mikaboshi::test_mods::XiaGuaTuParams;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(params: &JsValue) -> JsValue {
///     let params: XiaGuaTuParams = params.into_serde().unwrap();
///     let unpan_xing_order: [usize; 9] =
///         params
///             .unpan_xing_order
///             .try_into()
///             .unwrap_or_else(|v: Vec<usize>| {
///                 panic!("Expected a Vec of length 9 but it was {}", v.len())
///             });
///     let xia_gua_tu: HashMap<&str, XiaGuaTu> = get_xiaguatu_from_unpan_index(
///         params.unpan_xing_center,
///         &unpan_xing_order,
///         params.xiang_xing_direction.as_str(),
///         params.xiang_xing_sector,
///     );
///     JsValue::from_serde(&xia_gua_tu).unwrap()
/// }
/// ```
pub fn get_xiaguatu_from_unpan_index<'a>(
    unpan_xing_center: usize,
    unpan_xing_order: &'a [usize; 9],
    xiang_xing_direction: &'a str,
    xiang_xing_sector: usize,
) -> HashMap<&'a str, XiaGuaTu<'a>> {
    let mut xgtu = HashMap::new();

    // `chart` for 運盤星 (Un-Pan Xing) is straight
    // forward. The center 九星 (Jiu-Xing) is already
    // given, and you simply have to fly the given
    // chart.
    xgtu.insert(
        "unpan_xing",
        XiaGuaTu {
            kind: XiaGuaTuKind::UnPanXing,
            center: Some(unpan_xing_center),
            direction: None,
            sector: None,
            chart: Some(fly_flying_stars(
                unpan_xing_center,
                unpan_xing_order,
                false,
            )),
        },
    );

    // `chart` for 山星 (Shan-Xing) to be later
    // calculated. `direction` for 山星 (Shan-Xing)
    // is just the opposite of 向星 (Xiang-Xing).
    xgtu.insert(
        "shan_xing",
        XiaGuaTu {
            kind: XiaGuaTuKind::ShanXing,
            center: None,
            direction: Some(get_opposite_direction(
                xiang_xing_direction,
            )),
            sector: Some(xiang_xing_sector),
            chart: None,
        },
    );

    // `chart` for 向星 (Xiang-Xing) to be later
    // calculated. `direction` is already given.
    xgtu.insert(
        "xiang_xing",
        XiaGuaTu {
            kind: XiaGuaTuKind::XiangXing,
            center: None,
            direction: Some(xiang_xing_direction),
            sector: Some(xiang_xing_sector),
            chart: None,
        },
    );

    // First, we need to find out which direction
    // the device is currently pointing to.
    let curr_dir: &str =
        direction_from_dipan_order(unpan_xing_order);

    // Once the direction is found, then we will
    // obtain the compass direction mapping.
    let compass_positions: [&str; 9] =
        DIRECTION_POSITIONS_IN_CHART[curr_dir];

    // Find `center` and `chart` for both 山星
    // (Shan-Xing) and 向星 (Xiang-Xing).
    for key in ["shan_xing", "xiang_xing"] {
        // Since we only know directions for 山星
        // (Shan-Xing) and 向星 (Xiang-Xing), we will
        // look into the Un-Pan chart, and will find
        // out what 九星 (Jiu-Xing) we have for the
        // direction.

        // Initially, we only know the direction.
        let dir: &str =
            xgtu.get(key).unwrap().direction.unwrap();

        // For the direction, find out its array index.
        let pos: usize = compass_positions
            .iter()
            .position(|&d| d == dir)
            .unwrap();

        // Once the index is found, then find out its
        // 九星 (Jiu-Xing).
        let center: usize = (xgtu
            .get("unpan_xing")
            .unwrap()
            .chart
            .unwrap())[pos];

        let prev: &XiaGuaTu = xgtu.get(key).unwrap();

        // It is important to figure out whether it
        // is flying in normal or reverse order.
        // To do so, we will use a useful well known
        // formula.
        let normal: bool =
            is_shan_xiang_flying_normal(
                // Having 五黄土星 (5 Yellow) is a
                // special case, and the formula does
                // not work. Therefore, replacing it
                // with 運盤星 (Un-Pan Xing) index.
                if center == 4 {
                    xgtu.get("unpan_xing")
                        .unwrap()
                        .center
                        .unwrap()
                } else {
                    center
                },
                xgtu.get(key)
                    .unwrap()
                    .sector
                    .unwrap(),
            );

        // Now, calculate for the flying chart.
        let chart: [usize; 9] = fly_flying_stars(
            center,
            unpan_xing_order,
            normal,
        );

        *xgtu.get_mut(key).unwrap() = XiaGuaTu {
            center: Some(center),
            chart: Some(chart),
            ..*prev
        };
    }

    xgtu
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_constant_jiuxing() {
        assert_eq!(JIU_XING[0].num, 1);
    }

    #[test]
    fn test_get_jiuxing_from_index() {
        assert_eq!(get_jiuxing_from_index(0).num, 1);
    }

    #[test]
    fn test_constant_direction_to_jiuxing() {
        assert_eq!(
            *DIRECTION_TO_JIU_XING.get("n").unwrap(),
            0
        );
    }

    // TODO: jiuxing_index_from_direction
    // TODO: JIU_XING_DI_PAN_POSITIONS

    #[test]
    fn test_get_jiuxing_dipan_positions_from_direction(
    ) {
        let exp = [5, 0, 7, 6, 4, 2, 1, 8, 3];
        assert_eq!(
            get_jiuxing_dipan_positions_from_direction("n").unwrap(),
            &exp
        );
    }

    // TODO: JIU_XING_DI_PAN_POSITIONS_CLOCKWISE <-- NOT NEEDED

    #[test]
    fn normalize_jiuxing_single() {
        assert_eq!(normalize_jiuxing(9), 0);
    }

    #[test]
    fn normalize_jiuxing_all() {
        let arr: [usize; 11] =
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let exp: [usize; 11] =
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 0, 1];

        let res: [usize; 11] = arr
            .iter()
            .map(|index: &usize| {
                normalize_jiuxing(*index as i32)
            })
            .collect::<Vec<usize>>()
            .try_into()
            .unwrap();

        assert_eq!(res, exp);
    }

    // TODO: unpan_xing_index
    // TODO: unpan_xing_data <--- NOT IN USE
    // TODO: flying_stars_chart <--- NOT IN USE
    // TODO: is_shan_xiang_flying_normal
    // TODO: get_xiaguatu_from_unpan_index

    // ===============================================
    // LO-SHU ORDER - Normal Order
    // ===============================================

    /// Fly *NORMAL* for Lo-Shu Order:
    /// [4] 五黄土星 (5 Green)
    #[test]
    fn fly_stars_normal_lo_shu_5_green() {
        let center: usize = 4; // [4] 五黄土星 (5 Green)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [5, 0, 7, 6, 4, 2, 1, 8, 3];

        assert_eq!(
            fly_flying_stars(center, order, false),
            exp
        );
    }

    /// Fly *NORMAL* for Lo-Shu Order:
    /// [5] 六白金星 (6 White)
    #[test]
    fn fly_stars_normal_lo_shu_6_white() {
        let center: usize = 5; // [5] 六白金星 (6 White)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [6, 1, 8, 7, 5, 3, 2, 0, 4];

        assert_eq!(
            fly_flying_stars(center, order, false),
            exp
        );
    }

    /// Fly *NORMAL* for Lo-Shu Order:
    /// [6] 七赤金星 (7 Red)
    #[test]
    fn fly_stars_normal_lo_shu_7_red() {
        let center: usize = 6; // [6] 七赤金星 (7 Red)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [7, 2, 0, 8, 6, 4, 3, 1, 5];

        assert_eq!(
            fly_flying_stars(center, order, false),
            exp
        );
    }

    /// Fly *NORMAL* for Lo-Shu Order:
    /// [7] 八白土星 (8 White)
    #[test]
    fn fly_stars_normal_lo_shu_8_white() {
        let center: usize = 7; // [7] 八白土星 (8 White)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [8, 3, 1, 0, 7, 5, 4, 2, 6];

        assert_eq!(
            fly_flying_stars(center, order, false),
            exp
        );
    }

    /// Fly *NORMAL* for Lo-Shu Order:
    /// [8] 九紫火星 (9 Purple)
    #[test]
    fn fly_stars_normal_lo_shu_9_purple() {
        let center: usize = 8; // [8] 九紫火星 (9 Purple)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [0, 4, 2, 1, 8, 6, 5, 3, 7];

        assert_eq!(
            fly_flying_stars(center, order, false),
            exp
        );
    }

    // ===============================================
    // LO-SHU ORDER - Reverse Order
    // ===============================================

    /// Fly *REVERSE* for Lo-Shu Order (North):
    /// [4] 五黄土星 (5 Green)
    #[test]
    fn fly_stars_reverse_5_green_north() {
        let center: usize = 4; // [4] 五黄土星 (5 Green)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("n")
                .unwrap();
        let exp: [usize; 9] =
            [3, 8, 1, 2, 4, 6, 7, 0, 5];

        assert_eq!(
            fly_flying_stars(center, order, true),
            exp
        );
    }

    /// Fly *REVERSE* for Lo-Shu Order (North-East):
    /// [4] 五黄土星 (5 Green)
    #[test]
    fn fly_stars_reverse_lo_shu_5_green_north_east() {
        let center: usize = 4; // [4] 五黄土星 (5 Green)
        let order: &[usize; 9] =
            JIU_XING_DI_PAN_POSITIONS
                .get("ne")
                .unwrap();
        let exp: [usize; 9] =
            [8, 1, 6, 3, 4, 5, 2, 7, 0];

        assert_eq!(
            fly_flying_stars(center, order, true),
            exp
        );
    }

    // ===============================================
    // COMPASS CLOCKWISE - Normal Order
    // ===============================================

    // Fly *NORMAL* for COMPASS CLOCKWISE:
    // [4] 五黄土星 (5 Yellow)
    // #[test]
    // fn fly_stars_normal_lo_shu_5_yellow() {
    //     let center: usize = 4; // [4] 五黄土星 (5 Yellow)
    //     let order: &[usize; 8] = &JIU_XING_DI_PAN_POSITIONS_CLOCKWISE;
    //     let exp: [usize; 8] = [0, 7, 2, 3, 8, 1, 6, 5];

    //     assert_eq!(fly_flying_stars(center, order,false), exp);
    // }
}
