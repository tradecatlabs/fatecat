//! A module for 五行 (Wu-Xing).
use serde::{Deserialize, Serialize};

use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};
use crate::utils::get_json;

/// A struct representing 五行 (Wu-Xing).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WuXing {
    pub name: Language,
}

/// A temporary struct for loading JSON data when
/// defining a static const `WU_XING`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WuXingRawData {
    pub name: LanguageData,
}

impl LanguageTrait for WuXing {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for WuXingRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

lazy_static! {
    /// A static vector with 5 items, each represents
    /// 五行 (Wu-Xing).
    ///
    /// For attributes details stored in the vector is
    /// found in JSON file:
    /// `src/json/wuxing.json`
    pub static ref WU_XING: Vec<WuXing> = {
        let json = &include_str!("../json/wuxing.json");
        let data: Vec<WuXingRawData> = get_json::<WuXingRawData>(json);
        data.iter()
            .map(|item| {
                let item = item.clone();
                WuXing {
                    name: item.language_from_data(),
                }
            })
            .collect()
    };
}
