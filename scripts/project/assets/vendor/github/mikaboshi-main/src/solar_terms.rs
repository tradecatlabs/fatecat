//! A module for 二十四节气 (Er-Shi-Si Jie-Qi).
//! Or, for calculating 立春 (Li-Chun).

use chrono::naive::NaiveDate;
use chrono::Datelike;
use serde::{Deserialize, Serialize};
use sowngwala::time::add_date;

use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};
use crate::utils::{
    get_json, longitude_of_the_sun_from_generic_date,
};

#[derive(Debug)]
pub struct SolarTerm {
    pub id: u8,
    pub name: Language,
    pub angle: u16,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SolarTermRawData {
    pub id: u8,
    pub name: LanguageData,
    pub angle: u16,
}

impl LanguageTrait for SolarTerm {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for SolarTermRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

lazy_static! {
    pub static ref SOLAR_TERMS: Vec<SolarTerm> = {
        let json =
            &include_str!("../json/solar_terms.json");
        let data: Vec<SolarTermRawData> =
            get_json::<SolarTermRawData>(json);
        data.iter()
            .map(|item| {
                let item = item.clone();
                SolarTerm {
                    id: item.id,
                    name: item.language_from_data(),
                    angle: item.angle,
                }
            })
            .collect()
    };
}

#[allow(clippy::many_single_char_names)]
pub fn get_last_term(
    date: NaiveDate,
) -> (f64, NaiveDate) {
    let lng_0: f64 =
        longitude_of_the_sun_from_generic_date(date);
    // For the unit of 15, we want the last term.
    // Ex.
    //   317.435511 --> 315.0
    let target = (lng_0 / 15.0).abs().floor() * 15.0;

    let mut next = NaiveDate::from_ymd(
        date.year(),
        date.month(),
        date.day(),
    );

    let mut prev: Option<NaiveDate> = None;
    let mut term: Option<NaiveDate> = None;

    // Go back by one day a time.
    while term.is_none() {
        let lng: f64 =
            longitude_of_the_sun_from_generic_date(
                next,
            );
        // See if the target falls in the current date.
        if lng <= target && lng > (target - 1.0) {
            term = prev;
        } else {
            prev = Some(next);
            next = add_date(next, -1_i64);
        }
    }
    (target, term.unwrap())
}

/// Example:
/// ```rust
/// use chrono::Datelike;
/// use mikaboshi::solar_terms::get_lichun;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(year: i32) -> JsValue {
///     let lichun = get_lichun(year);
///     JsValue::from_str(&format!(
///         "{:04}-{:02}-{:02}",
///         lichun.year(),
///         lichun.month(),
///         lichun.day(),
///     ))
/// }
/// ```
#[allow(clippy::many_single_char_names)]
pub fn get_lichun(year: i32) -> NaiveDate {
    let date = NaiveDate::from_ymd(year, 2, 6);
    let (_lng, lichun) = get_last_term(date);
    lichun
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_last_term() {
        let (_lng, term): (f64, NaiveDate) =
            get_last_term(NaiveDate::from_ymd(
                2022, 2, 6,
            ));
        assert_eq!(term.year(), 2022);
        assert_eq!(term.month(), 2);
        assert_eq!(term.day(), 4);
    }
}
