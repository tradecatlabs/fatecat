extern crate chrono;

use chrono::Datelike;
use chrono::naive::NaiveDate;

use mikaboshi::bagua::{get_gua_compass_order as _gua_compass_order, Gua};
use mikaboshi::compass::{
    get_direction_positions_in_chart as _direction_positions_in_chart,
    get_opposite_direction as _opposite_direction,
    get_twentyfour_data_from_direction as _twentyfour_data_from_direction,
    get_twentyfour_data_from_index as _twentyfour_data_from_index,
    get_twentyfour_direction_from_degrees as _twentyfour_direction_from_degrees,
    get_twentyfour_direction_from_index as _twentyfour_direction_from_index, Direction,
    TwentyFourType,
};
use mikaboshi::ganzhi::Bazi;
use mikaboshi::jiuxing::{
    get_jiuxing_dipan_positions_from_direction as _jiuxing_dipan_positions_from_direction,
    get_jiuxing_from_index as _jiuxing_from_index,
    get_xiaguatu_from_unpan_index as _xiaguatu_from_unpan_index,
    unpan_xing_index as _unpan_xing_index, JiuXing, XiaGuaTu,
};
use mikaboshi::shengsi::{get_shengsi_mapping as _get_shengsi_mapping, ShengSi};
use mikaboshi::solar_terms::get_lichun as _get_lichun;
use std::collections::HashMap;
use std::convert::{From, TryInto};
use wasm_bindgen::prelude::*;

pub mod structs;

use crate::structs::{
    DateParams,
    DateTimeParams,
    ShengSiParams,
    XiaGuaTuParams,
};

/// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);
}

#[wasm_bindgen(start)]
pub fn main() {
    console_error_panic_hook::set_once();
}

// ================================================================
// 八卦 (Gua)
// ================================================================

#[wasm_bindgen]
pub fn get_gua_compass_order(index: usize) -> JsValue {
    let gua: Option<&Gua> = _gua_compass_order(index);
    JsValue::from_serde(&gua).unwrap()
}

// ================================================================
// 二十四山向 (Er-Shi Si-Shan Xiang)
// ================================================================

// *** NOT IN USE ***
// A simple accessor for getting values in DIRECTION_POSITIONS_IN_CHART.
#[wasm_bindgen]
pub fn get_direction_positions_in_chart(direction: &str) -> JsValue {
    JsValue::from(
        (match _direction_positions_in_chart(direction) {
            Some(positions) => positions.to_vec(),
            _ => Vec::new(),
        })
        .into_iter()
        .map(JsValue::from)
        .collect::<js_sys::Array>(),
    )
}

// *** NOT IN USE ***
// A simple accessor for getting values in OPPOSITE_DIRECTION.
#[wasm_bindgen]
pub fn get_opposite_direction(direction: &str) -> JsValue {
    JsValue::from(_opposite_direction(direction))
}

#[wasm_bindgen]
pub fn get_twentyfour_direction_from_index(index: usize) -> JsValue {
    let dir: &Direction = _twentyfour_direction_from_index(index);
    JsValue::from_serde(dir).unwrap()
}

#[wasm_bindgen]
pub fn get_twentyfour_data_from_index(index: usize) -> JsValue {
    let t_type: TwentyFourType = _twentyfour_data_from_index(index);
    match t_type {
        TwentyFourType::Gua(gua) => JsValue::from_serde(gua).unwrap(),
        TwentyFourType::Stem(stem) => JsValue::from_serde(stem).unwrap(),
        TwentyFourType::Branch(branch) => JsValue::from_serde(branch).unwrap(),
    }
}

#[wasm_bindgen]
pub fn get_twentyfour_direction_from_degrees(degrees: f32) -> JsValue {
    let dir: Direction = _twentyfour_direction_from_degrees(degrees);
    JsValue::from_serde(&dir).unwrap()
}

#[wasm_bindgen]
pub fn get_twentyfour_data_from_direction(direction: &str, sector: usize) -> JsValue {
    let t_type: TwentyFourType = _twentyfour_data_from_direction(direction, sector);
    match t_type {
        TwentyFourType::Gua(gua) => JsValue::from_serde(gua).unwrap(),
        TwentyFourType::Stem(stem) => JsValue::from_serde(stem).unwrap(),
        TwentyFourType::Branch(branch) => JsValue::from_serde(branch).unwrap(),
    }
}

// ================================================================
// 干支 (Gan-Zhi)
// ================================================================

#[wasm_bindgen]
pub fn get_bazi(params: &JsValue) -> JsValue {
    let params: DateTimeParams = params.into_serde().unwrap();

    JsValue::from_serde(
        &Bazi::from_fixed(
            params.into()
        )
    ).unwrap()
}

#[wasm_bindgen]
pub fn get_lichun(year: i32) -> JsValue {
    let lichun = _get_lichun(year);
    JsValue::from_str(&format!(
        "{:04}-{:02}-{:02}",
        lichun.year(),
        lichun.month(),
        lichun.day(),
    ))
}

// ================================================================
// 九星 (Jiu-Xing)
// ================================================================

#[wasm_bindgen]
pub fn get_jiuxing_from_index(index: usize) -> JsValue {
    let dir: &JiuXing = _jiuxing_from_index(index);
    JsValue::from_serde(dir).unwrap()
}

#[wasm_bindgen]
pub fn get_unpan_xing_index(current: &JsValue, lichun: &JsValue) -> JsValue {
    let params_1: DateParams = current.into_serde().unwrap();
    let params_2: DateParams = lichun.into_serde().unwrap();

    let current = NaiveDate::from(params_1);
    let lichun = NaiveDate::from(params_2);

    let index: usize = _unpan_xing_index(current, lichun);

    JsValue::from_f64(index as f64)
}

#[wasm_bindgen]
pub fn get_xiaguatu_from_unpan_index(params: &JsValue) -> JsValue {
    let params: XiaGuaTuParams = params.into_serde().unwrap();

    let unpan_xing_order: [usize; 9] =
        params
            .unpan_xing_order
            .try_into()
            .unwrap_or_else(|v: Vec<usize>| {
                panic!("Expected a Vec of length 9 but it was {}", v.len())
            });

    let xia_gua_tu: HashMap<&str, XiaGuaTu> = _xiaguatu_from_unpan_index(
        params.unpan_xing_center,
        &unpan_xing_order,
        params.xiang_xing_direction.as_str(),
        params.xiang_xing_sector,
    );

    JsValue::from_serde(&xia_gua_tu).unwrap()
}

// A simple accessor for getting values in JIU_XING_DI_PAN_POSITIONS.
#[wasm_bindgen]
pub fn get_jiuxing_dipan_positions_from_direction(direction: &str) -> JsValue {
    JsValue::from(
        (match _jiuxing_dipan_positions_from_direction(direction) {
            Some(positions) => positions.to_vec(),
            _ => Vec::new(),
        })
        .into_iter()
        .map(|index| JsValue::from(index as u32))
        .collect::<js_sys::Array>(),
    )
}

// ================================================================
// 生死衰旺 (Sheng-Si Shuai-Wang)
// ================================================================

#[wasm_bindgen]
pub fn get_shengsi_mapping(params: &JsValue) -> JsValue {
    let params: ShengSiParams = params.into_serde().unwrap();
    let unpan_id: usize = params.unpan_id;

    let chart: [usize; 9] = params
        .unpan_xing_chart
        .try_into()
        .unwrap_or_else(|v: Vec<usize>| {
            panic!("Expected a Vec of length 9 but it was {}", v.len())
        });

    let mapping: Vec<Option<&ShengSi>> = _get_shengsi_mapping(unpan_id, &chart);

    JsValue::from_serde(&mapping).unwrap()
}
