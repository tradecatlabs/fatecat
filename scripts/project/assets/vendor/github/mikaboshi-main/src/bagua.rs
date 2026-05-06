//! 八卦 (Ba-Gua) is a concept in 易経 (I-Ching) which
//! is merely a concept in fortune telling, but also
//! appears frequently in a variety of Chinese philosophy.
//! "Gua" (卦) is a conventional unit which characterizes
//! certain aspects/qualities in life. "Ba" simply
//! means "8" in Chinese. So, "Ba-Gua" (八卦) tells
//! that it consists of 8 卦 (Gua). To the eyes of
//! ancient Chinese, everything in this world was of
//! either 陰 (Yin) or 陽 (Yang). Or, you could say,
//! the world is divided into 2. However, if you
//! observe more carefully, you notice some in Yang
//! may slightly lean toward Yin, and some in Yin
//! toward Yang. So, you could probably have another
//! division there, for this time, divisions of 4.
//! For greater Yang, you have lesser "Yin" and "Yang",
//! or you may call them, "Yang-Yang" and "Yang-Yin".
//! Likewise, for Yin, you will have "Yin-Yang" and
//! "Yin-Yin". If you are brave enough, you could
//! repeat the process for the one last time.
//! This time, you would divide the world into 8.
//! For ancient Chinese perceived the last division
//! of 8 being the basic building blocks for observing
//! nature, and called them, 八卦 (Ba-Gua)
//!
//! Now, when we say 八卦 (Ba-Gua), we usually refer to
//! 2 different systems. For the division just described
//! above is called "先天八卦" (or _"The Primordial
//! Heaven"_), and a diagram to represent this order
//! is called "河圖" (He-Tu) (or 伏羲八卦 (Fu-Xi Ba-Gua)).
//! Another one is called "後天八卦" (or _"The Manifested
//! Heaven"_), and its diagram is called "洛書" (Lo-Shu)
//! (or 文王八卦 (King Wen Ba-Gua)). For the former
//! illustrates the world of the original heaven, and
//! the latter, the manifested world (for which elements
//! in nature play active roles to produce gross material
//! plane of our reality).
//!
//! Order of 河圖 (He-Tu) (for 先天八卦 _"The Primordial
//! Heaven"_)
//!
//! [0] 乾 (Qian)  
//! [1] 兌 (Dui)  
//! [2] 離 (Li)  
//! [3] 震 (Zhen)  
//! [4] 巽 (Xun)  
//! [5] 坎 (Kan)  
//! [6] 坤 (Kun)  
//! [7] 艮 (Gen)  
//!
//! Order of 洛書 (Lo-Shu) (for 後天八卦 _"The Manifested
//! Heaven"_)
//!
//! [0] 坎 (Kan)  
//! [1] 坤 (Kun)  
//! [2] 震 (Zhen)  
//! [3] 巽 (Xun)  
//! [4] 乾 (Qian)  
//! [5] 兌 (Dui)  
//! [6] 艮 (Gen)  
//! [7] 離 (Li)  
//!
//! So, when we talk about 八卦 (Ba-Gua), we need to be
//! specific about which world we referring to. As you
//! can see, there are 3 sets of vectors defined in this
//! program, namely:
//!
//! - `BAGUA_HE_TU_ORDER`  
//! - `BAGUA_LO_SHU_ORDER`  
//! - `BAGUA_LO_SHU_ORDER_WITH_CENTER`
//!
//! Notice that the first 2 consists of 8 items, but
//! the third one consists of 9. When using 八卦 (Ba-Gua)
//! for Feng-Shui, we usually refer to 洛書 (Lo-Shu)
//! diagram (which is `BAGUA_LO_SHU_ORDER`). However,
//! we usually plot 洛書 (Lo-Shu) into 9 boxes because
//! it is often associated with 九星 (Jiu-Xing) which
//! requires not only 8 compass directions, but with
//! an extra box in the middle. So, in addition to
//! 八卦 (Ba-Gua), when managing 洛書 (Lo-Shu) for
//! Feng-Shui, we need CENTER (or "中" (Zhong)
//! in Chinese), and that is what we have for
//! `BAGUA_LO_SHU_ORDER_WITH_CENTER`.
//!
//! Also, notice, another vector defined in
//! the program, `BAGUA_LO_SHU_COMPASS_ORDER`.
//! This is a special vector for which the order is
//! _conceptually_ in "Lo-Shu" order, however, mapped to
//! 8 compass directions as each 卦 (Gua) plotted in
//! clockwise manner. This is specially useful when we
//! have an app with a compass UI because you can
//! directly plot 卦 (Gua) out of this vector.

use serde::{Deserialize, Serialize};

use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};

use crate::utils::{get_json, make_sort};

/// A struct representing 卦 (Gua) and stores its
/// attributes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Gua {
    pub name: Language,
    pub jiuxing_num: u8,
    pub direction: String,
    pub element: u8,
}

/// A temporary struct for loading JSON data when
/// defining a various vectors for 八卦 (Ba-Gua).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GuaRaw {
    pub name: LanguageData,
    pub jiuxing_num: u8,
    pub direction: String,
    pub element: u8,
}

impl LanguageTrait for Gua {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for GuaRaw {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

lazy_static! {
    /// This is a vector for 八卦 (Ba-Gua) with 9 items
    /// where the 5th item being "中" (Zhong). By having
    /// 9 items instead of 8, it can be directly mapped
    /// to 9 stars of 九星 (Jiu-Xing). Since 九星
    /// (Jiu-Xing) is mapped in "Lo-Shu" (洛書) order,
    /// so is this vector. Check out the attribute
    /// `jiuxing_num` for each data, and you will notice
    /// it corresponds to the Jiu-Xing number.
    ///
    /// 八卦 (Ba-Gua) in "Lo-Shu" (洛書) order with
    /// 中 (Zhong) in the middle:
    ///
    /// [0] 坎 (Kan) -> No. 1
    /// [1] 坤 (Kun) -> No. 2
    /// [2] 震 (Zhen) -> No. 3
    /// [3] 巽 (Xun) -> No. 4
    /// [4] 中 (Zhong) -> No. 5
    /// [5] 乾 (Qian) -> No. 6
    /// [6] 兌 (Dui) -> No. 7
    /// [7] 艮 (Gen) -> No. 8
    /// [8] 離 (Li) -> No. 9
    ///
    /// For attributes details stored in the vector is
    /// found in JSON file:
    /// `src/json/bagua.json`
    pub static ref BAGUA_LO_SHU_ORDER_WITH_CENTER: Vec<Gua> = {
        let json = &include_str!("../json/bagua.json");
        let data: Vec<GuaRaw> = get_json::<GuaRaw>(json);
        data.iter().map(|item| {
            let item = item.clone();
            Gua {
                name: item.language_from_data(),
                direction: item.direction,
                jiuxing_num: item.jiuxing_num,
                element: item.element,
            }
        }).collect()
    };

    /// [INDEX] 八卦 (Ba-Gua) in "He-Tu" (河圖) order.
    pub static ref BAGUA_HE_TU_ORDER_INDEXES: Vec<u8> = vec![0, 1, 2, 3, 5, 6, 7, 8];

    /// [ACTUAL DATA] 八卦 (Ba-Gua) in "He-Tu" (河圖)
    /// order.
    ///
    /// [0] 乾 (Qian)
    /// [1] 兌 (Dui)
    /// [2] 離 (Li)
    /// [3] 震 (Zhen)
    /// [4] 巽 (Xun)
    /// [5] 坎 (Kan)
    /// [6] 坤 (Kun)
    /// [7] 艮 (Gen)
    pub static ref BAGUA_HE_TU_ORDER: Vec<Gua> = make_sort(
        BAGUA_HE_TU_ORDER_INDEXES.to_vec() // order
    )(
        BAGUA_LO_SHU_ORDER_WITH_CENTER.to_vec() // data source
    );

    /// [INDEX] 八卦 (Ba-Gua) in "Lo-Shu" (洛書) order.
    pub static ref BAGUA_LO_SHU_ORDER_INDEXES: Vec<u8> = vec![0, 1, 2, 3, 5, 6, 7, 8];

    /// [ACTUAL DATA] 八卦 (Ba-Gua) in "Lo-Shu" (洛書)
    /// order.
    ///
    /// [0] 坎 (Kan)
    /// [1] 艮 (Gen)
    /// [2] 震 (Zhen)
    /// [3] 巽 (Xun)
    /// [4] 離 (Li)
    /// [5] 坤 (Kun)
    /// [6] 兌 (Dui)
    /// [7] 乾 (Qian)
    pub static ref BAGUA_LO_SHU_ORDER: Vec<Gua> = make_sort(
        BAGUA_LO_SHU_ORDER_INDEXES.to_vec() // order
    )(
        BAGUA_LO_SHU_ORDER_WITH_CENTER.to_vec() // data source
    );

    /// [INDEX] 八卦 (Ba-Gua) in "Lo-Shu" order, however,
    /// mapped to 8 compass directions.
    pub static ref BAGUA_LO_SHU_COMPASS_ORDER_INDEXES: Vec<u8> = vec![0, 7, 2, 3, 8, 1, 6, 5];

    /// [ACTUAL DATA] 八卦 (Ba-Gua) in "Lo-Shu" order,
    /// however, mapped to 8 compass directions. When
    /// "Lo-Shu" (洛書) order is mapped to 8 compass
    /// directions, it is convenient to have a vector
    /// which starts with 卦 (Gua) for _"NORTH"_ which
    /// is "坎" (Kan). Likewise, we want the second
    /// item being 卦 (Gua) for _"NORTH EAST"_ which is
    /// "艮" (Gen). For the third item, likewise, for
    /// _"EAST"_ or "震" (Zhen).
    ///
    /// 八卦 (Ba-Gua) in "Lo-Shu" order mapped to
    /// 8 directions (starting NORTH):
    ///
    /// [0] 坎 (Kan)
    /// [1] 艮 (Gen)
    /// [2] 震 (Zhen)
    /// [3] 巽 (Xun)
    /// [4] 離 (Li)
    /// [5] 坤 (Kun)
    /// [6] 兌 (Dui)
    /// [7] 乾 (Qian)
    pub static ref BAGUA_LO_SHU_COMPASS_ORDER: Vec<Gua> = make_sort(
        BAGUA_LO_SHU_COMPASS_ORDER_INDEXES.to_vec() // order
    )(
        BAGUA_LO_SHU_ORDER_WITH_CENTER.to_vec() // data source
    );
}

/// A getter for `BAGUA_LO_SHU_COMPASS_ORDER`.
///
/// Example:
/// ```rust
/// use mikaboshi::bagua::{get_gua_compass_order, Gua};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(index: usize) -> JsValue {
///     let gua: Option<&Gua> = get_gua_compass_order(index);
///     JsValue::from_serde(&gua).unwrap()
/// }
/// ```
pub fn get_gua_compass_order(
    index: usize,
) -> Option<&'static Gua> {
    match BAGUA_LO_SHU_COMPASS_ORDER.get(index) {
        Some(gua) => Some(gua),
        None => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_constant_bagua_list_full() {
        assert_eq!(
            BAGUA_LO_SHU_ORDER_WITH_CENTER[0]
                .jiuxing_num,
            1
        );
    }

    // TODO: BAGUA_LO_SHU_COMPASS_ORDER_INDEXES
    // TODO: BAGUA_LO_SHU_COMPASS_ORDER
    // TODO: gua_for_start_north
}
