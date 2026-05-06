//! 生死衰旺 (Sheng-Si Shuai-Wang) is just a
//! combination of 4 Chinese characters, each being:
//!
//! (1) Growing --> 生 (Sheng)  
//! (2) Deadly --> 死 (Si)  
//! (3) Perishing --> 衰 (Shuai)  
//! (4) Prosperous --> 旺 (Wang)  
//!
//! They are often used in 四柱命理学 (The Four Pillars
//! of Destiny), but used in Feng-Shui as well.
//! It simply suggests that there are 4 states to
//! the energy occupying the space. In 玄空飞星風水
//! (Xuan-Kong Fei-Xing Feng-Shui), it describes
//! the state for the target year in 三元九運
//! (Sang-Yuan Jiu-Yun), especially, for its 向星
//! (Xiang-Xing).
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::jiuxing::normalize_jiuxing;

/// A struct representing 生死衰旺 (Sheng-Si
/// Shuai-Wang). `key` would be: "sheng", "si",
/// "shuai", or "wang".
#[derive(
    Debug, Clone, Deserialize, Serialize, PartialEq,
)]
pub struct ShengSi<'a> {
    pub key: &'a str,
    pub kanji: &'a str,
    pub meaning: &'a str,
}

/// A struct holding allocations of 生死衰旺
/// (Sheng-Si Shuai-Wang) for the given year.
/// For `usize` (in `Vec<usize>`) is 九星
/// (Jiu-Xing) index.
#[derive(Debug, Clone)]
pub struct ShengSiYearlyAlloc {
    pub wang: Vec<usize>,
    pub sheng: Vec<usize>,
    pub shuai: Vec<usize>,
    pub si: Vec<usize>,
}

impl ShengSiYearlyAlloc {
    pub fn accessor(
        &self,
        name: &str,
    ) -> Option<&Vec<usize>> {
        match name {
            "wang" => Some(&self.wang),
            "sheng" => Some(&self.sheng),
            "shuai" => Some(&self.shuai),
            "si" => Some(&self.si),
            _ => None,
        }
    }
}

lazy_static! {
    /// A HashMap for 生死衰旺 (Sheng-Si Shuai-Wang)
    /// by key (for each holds `ShengSi`).
    pub static ref SHENG_SI: HashMap<&'static str, ShengSi<'static>> = HashMap::from([
        ("sheng", ShengSi { key: "sheng", kanji: "生", meaning: "growth" }),
        ("si", ShengSi { key: "si", kanji: "死", meaning: "death" }),
        ("shuai", ShengSi { key: "shuai", kanji: "衰", meaning: "perishing" }),
        ("wang", ShengSi { key: "wang", kanji: "旺", meaning: "prosperous" }),
    ]);

    /// For every year, some 九星 (Jiu-Xing) maybe in
    /// 旺 (Wang = Prospering) phase, but some maybe
    /// in 死 (Si = Dying). 生死衰旺 (Sheng-Si
    /// Shuai-Wang) for 九星 (Jiu-Xing) is no random,
    /// but has certain patterns, and is repeated every
    /// 9 years. This cycle is called 三元九運
    /// (Sang-Yuan Jiu-Yun), and given the 運盤星
    /// (Un-Pan Xing) index for the specific year, you
    /// can tell of 生死衰旺 (Sheng-Si Shuai-Wang) for
    /// all the other 九星 (Jiu-Xing). Here, it is
    /// constructing the patterns for 9 years, and
    /// making them into a static vector for which each
    /// index being the 運盤星 (Un-Pan Xing) index.
    /// If you know the 運盤星 (Un-Pan Xing) index for
    /// the year, this static vector will tell you
    /// 生死衰旺 (Sheng-Si Shuai-Wang) for all 九星
    /// (Jiu-Xing).
    pub static ref SHENG_SI_ALLOC: Vec<ShengSiYearlyAlloc> = (0..9)
        .map(|i: i32| {
            // 旺 (Wang)
            let unpan_id = i;

            // 生 (Sheng)
            let sheng: Vec<usize> = [1, 2]
                .iter()
                .map(|num| {
                    normalize_jiuxing(unpan_id + num)
                })
                .collect::<Vec<usize>>();

            // 衰 (Shuai)
            let shuai: Vec<usize> = [1, 2]
                .iter()
                .map(|num| {
                    normalize_jiuxing(unpan_id - num)
                })
                .collect::<Vec<usize>>();

            // 死 (Si)
            let si: Vec<usize> = [1, 2, 3, 4]
                .iter()
                .map(|num| -> usize{
                    normalize_jiuxing(shuai[1] as i32 - num)
                })
                .collect::<Vec<usize>>();

            ShengSiYearlyAlloc {
                // 運盤星 (Un-Pan Xing) is always the
                // 旺 (wang) for the year.
                wang: vec!(unpan_id as usize),

                // Two 九星 (Jiu-Xing) that *proceed*
                // 運盤星 (Un-Pan Xing) is always the
                // 生 (Sheng).
                sheng,

                // Two 九星 (Jiu-Xing) that *preceed*
                // 運盤星 (Un-Pan Xing) is always the
                // 衰 (Shuai). However, there is
                // an exceptional case when 一白水星
                // (1 White) were given for the 運盤星
                // (Un-Pan Xing) because it should be
                // converted to 九紫火星 (9 Purple).
                shuai: if unpan_id == 0 {
                    vec!(8)
                } else {
                    shuai
                },

                // Calculation for 死 (Si) is tricky...
                si: si
                    .iter()
                    .filter_map(|&index| {
                        if unpan_id < 7 {
                            if index != 0 && index != 7 {
                                Some(index)
                            } else {
                                None
                            }
                        } else {
                            Some(index)
                        }
                    })
                    .collect::<Vec<usize>>(),
            }
        })
        .collect();
}

/// Given 運盤 (Un-Pan) index and a layout for the
/// current 運盤 (Un-Pan) positions (`&[usize; 9]`),
/// returns the corresponding 生死衰旺 (Sheng-Si
/// Shuai-Wang) situation.
///
/// Example:
/// ```rust
/// use std::convert::TryInto;
/// use mikaboshi::shengsi::{get_shengsi_mapping, ShengSi};
/// use mikaboshi::test_mods::ShengSiParams;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(params: &JsValue) -> JsValue {
///     let params: ShengSiParams = params.into_serde().unwrap();
///     let unpan_id: usize = params.unpan_id;
///     let chart: [usize; 9] = params
///         .unpan_xing_chart
///         .try_into()
///         .unwrap_or_else(|v: Vec<usize>| {
///             panic!("Expected a Vec of length 9 but it was {}", v.len())
///         });
///     let mapping: Vec<Option<&ShengSi>> = get_shengsi_mapping(unpan_id, &chart);
///     JsValue::from_serde(&mapping).unwrap()
/// }
/// ```
pub fn get_shengsi_mapping(
    unpan_id: usize,
    unpan_xing_chart: &[usize; 9],
) -> Vec<Option<&ShengSi>> {
    // At first, we will get 生死衰旺 (Sheng-Si
    // Shuai-Wang) for the given 運盤星 (Un-Pan
    // Xing).
    let yearly_allocs: &ShengSiYearlyAlloc =
        &SHENG_SI_ALLOC[unpan_id];

    // Now, 生死衰旺 (Sheng-Si Shuai-Wang) just obtained
    // is mapped by "sheng", "si", "shuai", and "wang".
    // However, we rather want to look up by 九星
    // (Jiu-Xing) index. So, we are creating a temporary
    // mapping here. Though, in the next line, we are
    // just initializing each in the mapping with `None`.
    let mut lookup: HashMap<usize, Option<&ShengSi>> =
        (0..9)
            .map(|index: usize| (index, None))
            .collect();

    // Once the mapping being initialized, we are
    // creating the mapping.
    for key in ["sheng", "si", "shuai", "wang"] {
        let data: Option<&ShengSi> =
            SHENG_SI.get(key);

        for index in
            yearly_allocs.accessor(key).unwrap()
        {
            *lookup.get_mut(index).unwrap() = data;
        }
    }

    // We have 運盤 (Un-Pan) chart given. All we want
    // is to find 生死衰旺 (Sheng-Si Shuai-Wang) for
    // each  九星 (Jiu-Xing) in the 運盤 (Un-Pan)
    // chart (using the temporary mapping just created).
    unpan_xing_chart
        .iter()
        .map(|index: &usize| {
            *lookup.get(index).unwrap()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_constant_sheng_si() {
        assert_eq!(
            SHENG_SI.get("sheng").unwrap().key,
            "sheng"
        );
    }

    #[test]
    fn test_constant_sheng_si_alloc_for_wang() {
        assert_eq!(SHENG_SI_ALLOC[0].wang[0], 0);
    }

    #[test]
    fn test_constant_sheng_si_alloc_for_shuai() {
        assert_eq!(SHENG_SI_ALLOC[6].shuai[0], 5);
        assert_eq!(SHENG_SI_ALLOC[6].shuai[1], 4);
    }

    #[test]
    fn test_get_shengsi_mapping() {
        let res = get_shengsi_mapping(
            6,
            &[2, 0, 4, 7, 6, 5, 8, 3, 1],
        );
        assert_eq!(res[0].unwrap().key, "si"); // 2
        assert_eq!(res[1], None); // 0
        assert_eq!(res[2].unwrap().key, "shuai"); // 4
        assert_eq!(res[3].unwrap().key, "sheng"); // 7
        assert_eq!(res[4].unwrap().key, "wang"); // 6
        assert_eq!(res[5].unwrap().key, "shuai"); // 5
        assert_eq!(res[6].unwrap().key, "sheng"); // 8
        assert_eq!(res[7].unwrap().key, "si"); // 3
        assert_eq!(res[8].unwrap().key, "si"); // 1
    }
}

// 生入 Sheng-Ru (Shēng Rù)
// 剋入 Ke-Ru (Kè Rù)
// 生出 Sheng-Chu (Shēng Chū)
// 剋出 Ke-Chu (Kè Chū)
// 差錯 Cha-Cuo

// 旺 Prosperous
// 相 Supportive
// 休 Rest
// 囚 Inprisoned
// 死 Death

// Chang Sheng 12 Qi Phase (十二運)
//
// 长生 chang sheng
// 沐浴 mu yu
// 冠带 guan dai
// 临官 lin guān
// 帝旺 di wang
// 衰 Shuāi
// 病 Bing
// 死 Si
// 墓 Mu
// 绝 Jue
// 胎 Tai
// 养 Yang
