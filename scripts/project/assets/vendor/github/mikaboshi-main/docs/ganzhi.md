# 干支 (Gan-Zhi)

Source: [src/ganzhi.rs](../src/ganzhi.rs)

Based on 5 elements in nature with its 陰 (Yin) and 陽 (Yang) for each,
ancient Chinese described the plant growth using 10 conventional symbols
known as "10 Gan" (十干). Also, they tracked the motion of Jupiter
(which has 12 year cycle) and so they did divided the night sky into 12 regions,
and this is known as "12 Zhi" (十二支). When they record time and space,
they used the combinations of 10 Gan (干) and 12 Zhi (支)
which makes 60 patterns, and this is called 干支 (Gan-Zhi).

10 Gan (干):

[0] 甲 (Jia)  
[1] 乙 (Yi)  
[2] 丙 (Bing)  
[3] 丁 (Ding)  
[4] 戊 (Wu)  
[5] 己 (Ji)  
[6] 庚 (Geng)  
[7] 辛 (Xin)  
[8] 壬 (Ren)  
[9] 癸 (Gui)  

12 Zhi (支):

[0] 子 (Zi)  
[1] 丑 (Chou)  
[2] 寅 (Yin)  
[3] 卯 (Mao)  
[4] 辰 (Chen)  
[5] 巳 (Si)  
[6] 午 (Wu)  
[7] 未 (Wei)  
[8] 申 (Shen)  
[9] 酉 (You)  
[10] 戌 (Xu)  
[11] 亥 (Hai)  

Reference:
- [Sexagenary cycle - Wiki](https://en.wikipedia.org/wiki/Sexagenary_cycle)


## ganzhi::Stem

A struct representing 干 (Gan) or "Stem" and stores its attributes.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Stem {
    pub num: u8,
    pub name: Language,
}
```

## ganzhi::Branch

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Branch {
    pub num: u8,
    pub name: Language,
}
```

A struct representing 支 (Zhi) or "Branch" and stores its attributes.

## ganzhi::StemRawData

A temporary struct for loading JSON data when defining a static const `STEMS`.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StemRawData {
    pub num: u8,
    pub name: LanguageData,
}
```

## ganzhi::BranchRawData

A temporary struct for loading JSON data when defining a static const `BRANCHES`.

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BranchRawData {
    pub num: u8,
    pub name: LanguageData,
}
```

## ganzhi::GanZhi

A struct for holding `Stem` and `Branch`, or denoted as 干支 (Gan-Zhi).

```
#[derive(Debug, Serialize)]
pub struct GanZhi<'a> {
    pub stem: &'a Stem,
    pub branch: &'a Branch,
}
```

## ganzhi::Bazi

A struct representing 八字 (Bazi) and stores `GanZhi` as its attributes.
It is referred as _"The Four Pillars of Destiny"_ in English
mainly because the structure of 八字 (Bazi) necessary
for divinations in 四柱命理学 (_"The Four Pillars of Destiny"_).

```rust
#[derive(Debug, Serialize)]
pub struct Bazi<'a> {
    pub year: GanZhi<'a>,
    pub month: GanZhi<'a>,
    pub day: GanZhi<'a>,
    pub hour: GanZhi<'a>,
}
```

## ganzhi::STEMS

`Vec<Stem>`

A static vector with 10 items, each represents 干 (Gan).
Each stores associated attributes for the 干 (Gan).

[0] 甲 (Jia)  
[1] 乙 (Yi)  
[2] 丙 (Bing)  
[3] 丁 (Ding)  
[4] 戊 (Wu)  
[5] 己 (Ji)  
[6] 庚 (Geng)  
[7] 辛 (Xin)  
[8] 壬 (Ren)  
[9] 癸 (Gui)  

For attributes details stored in the vector is found in JSON file:
[json/ganzhi_stems.json](../json/ganzhi_stems.json)

## ganzhi::BRANCHES

`Vec<Branch>`

A static vector with 10 items, each represents 支 (Zhi).
Each stores associated attributes for the 支 (Zhi).

[0] 子 (Zi)  
[1] 丑 (Chou)  
[2] 寅 (Yin)  
[3] 卯 (Mao)  
[4] 辰 (Chen)  
[5] 巳 (Si)  
[6] 午 (Wu)  
[7] 未 (Wei)  
[8] 申 (Shen)  
[9] 酉 (You)  
[10] 戌 (Xu)  
[11] 亥 (Hai)  

For attributes details stored in the vector is found in JSON file:
`src/json/ganzhi_branches.json`

## ganzhi::GANZHI_SEXAGESIMAL

`Vec<(usize, usize)>`

A static vector with 60 items. `Vec<usize, usize>` where the first
`usize` being the `STEMS` index, and the second for the `BRANCHES`.
It is simply the combination of 10 stems and 12 branches
which eventually adds up to 60 patterns.

## ganzhi::HOUR_STEM_TABLE

`[[usize; 5]; 12]`

This is a table used when finding "Hour Stem".
Columns represents "Day Stem" groups, and there are 5 groups.
For insntace, if you have 甲 for "Day Stem",
you are looking into the first column (group).
Rows represents "Hour Branches" for which there are 12.
For instance, if you have 子 for "Hour Branch",
you are looking into the first row.
So, when you have 甲 for "Day Stem",
and 子 for "Hour Branch", "Hour Stem" is located
in the first column in the first row, which is 甲.

&nbsp; &nbsp; &nbsp; 甲乙丙丁戊  
&nbsp; &nbsp; &nbsp; 己庚辛壬癸  
&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;&dash;  
子: 甲丙戊庚壬  
丑: 乙丁己辛癸  
寅: 丙戊庚壬甲  
卯: 丁己辛癸乙  
辰: 戊庚壬甲丙  
巳: 己辛癸乙丁  
午: 庚壬甲丙戊  
未: 辛癸乙丁己  
申: 壬甲丙戊庚  
酉: 癸乙丁己辛  
戌: 甲丙戊庚壬  
亥: 乙丁己辛癸  

## ganzhi::Bazi::from_fixed

Returns `Bazi` from localtime (chrono's `DateTime<FixedOffset>`) and zone (`u32`).

Example:

```rust
use chrono::DateTime;
use chrono::offset::FixedOffset;
use mikaboshi::ganzhi::{ Bazi, GanZhi };

let zone: u32 = 9;
let fixed: DateTime<FixedOffset> = FixedOffset::east(zone * 3600)
    .ymd(2021, 7, 7)
    .and_hms(0, 0, 0);

let bazi: Bazi = Bazi::from_fixed(fixed, zone);

let year: GanZhi = bazi.year;
let month: GanZhi = bazi.month;
let day: GanZhi = bazi.day;
let hour: GanZhi = bazi.hour;

println!("年: {} ({})", year.alphabet(), year.alphabet_ja());
println!("月: {} ({})", month.alphabet(), month.alphabet_ja());
println!("日: {} ({})", day.alphabet(), day.alphabet_ja());
println!("時: {} ({})", hour.alphabet(), hour.alphabet_ja());

// 年: 辛丑 (かのと・うし)
// 月: 甲午 (きのえ・うま)
// 日: 乙卯 (きのと・う)
// 時: 癸未 (みずのと・ひつじ)
```

Example using `js_sys`:

```rust
use chrono::DateTime;
use chrono::offset::FixedOffset;
use mikaboshi::ganzhi::Bazi;
use wasm_bindgen::prelude::*;
    
#[wasm_bindgen]
pub fn get_bazi(params: &JsValue) -> JsValue {
    let zone: u32 = 9;
    let fixed: DateTime<FixedOffset> = FixedOffset::east(zone * 3600)
        .ymd(1985, 11, 5)
        .and_hms(1, 35, 0);

    JsValue::from_serde(
      &Bazi::from_fixed(fixed)
    ).unwrap()
}
```
