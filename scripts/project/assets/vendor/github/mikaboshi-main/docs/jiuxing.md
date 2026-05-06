# 九星 (Jiu-Xing)

Source: [src/jiuxing.rs](../src/jiuxing.rs)

九星 (Jiu-Xing) means "9 stars" in Chinese.
In 風水 (Feng-Shui), 9 boxes are drawn to represent
the spatial condition of the place in concern.
The box in the middle represents where you are,
and 8 boxes which surrounding the middle represent
8 compass directions. For these 9 boxes, plotted
special symbols, each of which is called, a "Star" (星).
When we say 九星 (Jiu-Xing) in Chinese, "Jiu" means "9",
and "Xing" means a "Star". While 九星 (Jiu-Xing)
has fixed positions (associated with 洛書 (Lo-Shu)),
they change positions over time, and this movement
is called 飞泊 (Fei-Po) or "flying" because of how it
appears to our eyes when they move.
//!
As explained in 八卦 (Ba-Gua) (see: `src/bagua.rs`),
there are 2 worldly systems concerned, namely,
先天八卦 (or "the Primordial Heaven") and
後天八卦 (or "the Manifested Heaven"), and we deal
with the latter system when we talk about 風水 (Feng-Shui).

In 玄空飞星風水 (Xuan-Kong Fei-Xing Feng-Shui), there is
a special name given to the latter system, and is called,
地盤 (Di-Pan). "Di" means "earth", and "Pan" means "board".
So, it is basically a board which is drawn at the bottom
of any Feng-Shui charts. On 地盤 (Di-Pan), 九星 (Jiu-Xing)
are plotted for which the order is fundamentally that of
洛書 (Lo-Shu) order in 八卦 (Ba-Gua). However, they move
(or "fly") over 地盤 (Di-Pan) as time goes.
In 玄空飞星風水 (Xuan-Kong Fei-Xing Feng-Shui), there are
3 other boards that are drawn on top of 地盤 (Di-Pan), namely:

- 運盤 (Un-Pan) or 天盤 (Tien-Pan)  
- 山星 (Shan-Xing)  
- 向星 (Xiang-Xing)  

For 運盤 (Un-Pan), positions of 九星 (Jiu-Xing) are determined
by construction year for the building in concern which is
calculated based on 三元九運 (Sang-Yuan Jiu-Yun),
or "9 Yearly Cycles". We could say that 運盤 (Un-Pan)
essentially describes the temporal aspect.
山星 (Shan-Xing) and 向星 (Xiang-Xing) are determined
by spatial aspects of the building (however, in actual
calculations, some temporal aspects comes in).

When these 3 extra boards are placed on top of 地盤 (Di-Pan),
the whole thing is called, 下卦図 (Xia-Gua-Tu), or simply
referred as 飞星図 (Fei-Xing-Tu), or "The Flying Star Chart".

Jiu-Xing (九星):

[0] 一白水星 (1 White)  
[1] 二黒土星 (2 Black)  
[2] 三碧木星 (3 Jade)  
[3] 四緑木星 (4 Green)  
[4] 五黄土星 (5 Yellow)  
[5] 六白金星 (6 White)  
[6] 七赤金星 (7 Red)  
[7] 八白土星 (8 White)  
[8] 九紫火星 (9 Purple)  


Reference:
- [Flying Star Feng Shui - Wiki](https://en.wikipedia.org/wiki/Flying_Star_Feng_Shui)


## jiuxing::JiuXing

A struct representing 九星 (Jiu-Xing).

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JiuXing {
    pub num: u8,
    pub direction: String,
    pub name: Language,
    pub color: String,
    pub element: WuXing,
    pub planet: Planet,
}
```

## jiuxing::JiuXingRawData

A temporary struct for loading JSON data when defining a static const `JIU_XING`.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JiuXingRawData {
    pub num: u8,
    pub direction: String,
    pub name: LanguageData,
    pub color: String,
    pub element: u8,
    pub planet: u8,
}
```

## jiuxing::XiaGuaTuKind

```rust
#[derive(Debug, Clone, Serialize, Deserialize, Copy)]
pub enum XiaGuaTuKind {
    UnPanXing, // 運盤
    ShanXing, // 山星
    XiangXing, // 向星
}
```

## jiuxing::XiaGuaTu

A struct representing 下卦図 (Xia-Gua-Tu).

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct XiaGuaTu<'a> {
    pub kind: XiaGuaTuKind,
    pub center: Option<usize>,
    pub direction: Option<&'a str>,
    pub sector: Option<usize>,
    pub chart: Option<[usize; 9]>,
}
```

## jiuxing::DIRECTION_TO_JIU_XING

`HashMap<&str, usize>`

## jiuxing::JIU_XING

`[JiuXing; 9]`

A static vector with 9 items, each represents 九星 (Jiu-Xing).

[0] 一白水星 (1 White)  
[1] 二黒土星 (2 Black)  
[2] 三碧木星 (3 Jade)  
[3] 四緑木星 (4 Green)  
[4] 五黄土星 (5 Yellow)  
[5] 六白金星 (6 White)  
[6] 七赤金星 (7 Red)  
[7] 八白土星 (8 White)  
[8] 九紫火星 (9 Purple)  

For attributes details stored in the vector is found in JSON file:
[json/jiuxing.json](../json/jiuxing.json)

## jiuxing::JIU_XING_DI_PAN_POSITIONS

`HashMap<&str, [usize; 9]>`

Although 洛書 (Lo-Shu) order is fixed, when 地盤 (Di-Pan)
is drawn on a device screen, the mapping for
九星 (Jiu-Xing) changes as the device rotates.
For example, 一白水星 (1 White) usually comes to the top
of the board when a device is pointing north. However,
when pointing north east, 一白水星 (1 White) moves
to the top left (which is north west).
For 8 compass directions, this constant provides
a mapping for the 洛書 (Lo-Shu) order.
For "n", 一白水星 (1 White) is the 2nd in the array.
For "ne", 一白水星 (1 White) is the 1st in the array.

It would look like this:

[5] 六白 [0] 一白 [7] 八白  
[6] 七赤 [4] 五黄 [2] 三碧  
[1] 二黒 [8] 九紫 [3] 四緑  
n: [5, 0, 7, 6, 4, 2, 1, 8, 3]

[0] 一白 [7] 八白 [2] 三碧  
[5] 六白 [4] 五黄 [3] 四緑  
[6] 七赤 [1] 二黒 [8] 九紫  
ne: [0, 7, 2, 5, 4, 3, 6, 1, 8]

[7] 八白 [2] 三碧 [3] 四緑  
[0] 一白 [4] 五黄 [8] 九紫  
[5] 六白 [6] 七赤 [1] 二黒  
e: [7, 2, 3, 0, 4, 8, 5, 6, 1]

[2] 三碧 [3] 四緑 [8] 九紫  
[7] 八白 [4] 五黄 [1] 二黒  
[0] 一白 [5] 六白 [6] 七赤  
se: [2, 3, 8, 7, 4, 1, 0, 5, 6]

[3] 四緑 [8] 九紫 [1] 二黒  
[2] 三碧 [4] 五黄 [6] 七赤  
[7] 八白 [0] 一白 [5] 六白  
s: [3, 8, 1, 2, 4, 6, 7, 0, 5]

[8] 九紫 [1] 二黒 [6] 七赤  
[3] 四緑 [4] 五黄 [5] 六白  
[2] 三碧 [7] 八白 [0] 一白  
sw: [8, 1, 6, 3, 4, 5, 2, 7, 0]

[1] 二黒 [6] 七赤 [5] 六白  
[8] 九紫 [4] 五黄 [0] 一白  
[3] 四緑 [2] 三碧 [7] 八白  
w: [1, 6, 5, 8, 4, 0, 3, 2, 7]

[6] 七赤 [5] 六白 [0] 一白  
[1] 二黒 [4] 五黄 [7] 八白  
[8] 九紫 [3] 四緑 [2] 三碧  
nw: [6, 5, 0, 1, 4, 7, 8, 3, 2]

## jiuxing::get_jiuxing_dipan_positions_from_direction

A getter for `JIU_XING_DI_PAN_POSITIONS`.

## jiuxing::get_jiuxing_from_index

A getter for `JIU_XING`.

Example:

```rust
use mikaboshi::jiuxing::{get_jiuxing_from_index, JiuXing};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn xx(index: usize) -> JsValue {
    let dir: &JiuXing = get_jiuxing_from_index(index);
    JsValue::from_serde(dir).unwrap()
}
```

## jiuxing::normalize_jiuxing

Given incorrect value for Jiu-Xing index, applies a modulo
to normalize it to fit within the range of 0 to 8.

Example:  
0 --> 0 ... Stays the same. "0" being "一白水星 (1 White)".  
8 --> 8 ... Stays the same. "8" being "九紫火星 (9 Purple)".  
9 --> 0 ... "9" is too much for the range, and becoming "0" which is "一白水星".  
10 --> 1 ... "10" is too much, and becoming "1" which is "二黒土星 (2 Black)".  
-1 --> 8 ... Making it positive. "8" being "九紫火星 (9 Purple)".  
-2 --> 7 ... Making it positive. "8" being "八白土星 (8 White)".  


## jiuxing::fly_flying_stars

This is a function for 飞泊 (Fei-Po) or "flying".
The idea is quite simple. Given the order (which is
the second argument `order` in array) of
九星 (Jiu-Xing) indexes, increments or decrements
each in the array, and simply return the array.
Depending on whichever currently resides in the center of
the board (which is the first argument `center`),
the value to increment or decrement changes.
For `order` is fundamentally that of the Lo-Shu order
(which is defined in `JIU_XING_DI_PAN_POSITIONS`),
however, the layout is always different since
the position changes depending on which direction
the device is pointing as the device rotates.


## jiuxing::get_xiaguatu_from_unpan_index

Calculates for 下卦図 (Xia-Gua-Tu). 1st and 2nd
arguments (`unpan_xing_center` and `unpan_xing_order`)
are required for all. For calculating a chart
for 運盤星 (Un-Pan Xing), that is all we need.
However, to calculate charts for 山星 (Shan-Xing)
and 向星 (Xiang-Xing), requires 3rd and 4th arguments
(`xiang_xing_direction` and `xiang_xing_sector`.

Example:
```rust
use std::collections::HashMap;
use std::convert::TryInto;
use mikaboshi::jiuxing::{get_xiaguatu_from_unpan_index, XiaGuaTu};
use mikaboshi::test_mods::XiaGuaTuParams;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn xx(params: &JsValue) -> JsValue {
    let params: XiaGuaTuParams = params.into_serde().unwrap();
    let unpan_xing_order: [usize; 9] =
        params
            .unpan_xing_order
            .try_into()
            .unwrap_or_else(|v: Vec<usize>| {
                panic!("Expected a Vec of length 9 but it was {}", v.len())
            });
    let xia_gua_tu: HashMap<&str, XiaGuaTu> = get_xiaguatu_from_unpan_index(
        params.unpan_xing_center,
        &unpan_xing_order,
        params.xiang_xing_direction.as_str(),
        params.xiang_xing_sector,
    );
    JsValue::from_serde(&xia_gua_tu).unwrap()
}
```
