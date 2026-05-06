# 二十四节气 (Er-Shi-Si Jie-Qi) and 立春 (Li-Chun)

Source: [src/solar_terms.rs](../src/solar_terms.rs)

A module for 二十四节气 (Er-Shi-Si Jie-Qi).
Or, for calculating 立春 (Li-Chun).

Reference:
- [Solar term - Wiki](https://en.wikipedia.org/wiki/Solar_term)


## solar_terms::SolarTerm

```rust
#[derive(Debug)]
pub struct SolarTerm {
    pub id: u8,
    pub name: Language,
    pub angle: u16,
}
```

## solar_terms::SolarTermRawData

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SolarTermRawData {
    pub id: u8,
    pub name: LanguageData,
    pub angle: u16,
}
```

## solar_terms::SOLAR_TERMS

`Vec<SolarTerm>`

## solar_terms::get_last_term

## solar_terms::get_lichun

Example:

```rust
use mikaboshi::solar_terms::get_lichun;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn xx(year: i16) -> JsValue {
    let lichun = get_lichun(year);
    JsValue::from_str(&format!(
        "{:04}-{:02}-{:02}",
        lichun.year as u16, lichun.month as u8, lichun.day as u8
    ))
}
```
