//! A module for compass directions. When dividing 360
//! degrees into 8, we get 45 degrees. Ancient Chinese
//! further divided them each into 3 (called "sectors"),
//! each having 15 degrees. Meaning, there are 24 sectors
//! as a total. This is called, 二十四山向 (Er-Shi-Si
//! Shan-Xiang). Not only for 8 directions, but these
//! 24 directions (sectors) are used in Feng-Shui, and
//! this is the module for these directions.
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

use crate::bagua::{
    Gua, BAGUA_LO_SHU_ORDER_WITH_CENTER,
};
use crate::ganzhi::{Branch, Stem, BRANCHES, STEMS};

/// 二十四山向 (Er-Shi-Si Shan-Xiang) can be
/// either 卦 (Gua), 干 (Gan), or 支 (Zhi).
pub enum TwentyFourType<'a> {
    Gua(&'a Gua),
    Stem(&'a Stem),
    Branch(&'a Branch),
}

/// A struct representing compass direction.
/// For each direction, there are 3 sectors.
#[derive(
    Debug, Clone, PartialEq, Serialize, Deserialize,
)]
pub struct Direction {
    pub direction: String,
    pub sector: usize,
}

impl Direction {
    pub fn new(
        direction: &str,
        sector: usize,
    ) -> Direction {
        Direction {
            direction: direction.to_string(),
            sector,
        }
    }
}

/// An array for 8 directions.
pub const DIRECTIONS: [&str; 8] =
    ["n", "ne", "e", "se", "s", "sw", "w", "nw"];

lazy_static! {
    /// A hash map with 9 items.
    /// Say, we have 9 boxes displayed on a device
    /// screen. Except for the box in the middle, we
    /// have 8 boxes around the middle to represent
    /// 8 compass directions. When facing "n" (north),
    /// for the first row, we have "nw", "n", and "ne".
    /// For the second row, we have "w", "", and "e"
    /// (where "" being the middle box). For the last,
    /// we have "sw", "s", and "se".
    ///
    /// [0] nw  [1] n   [2] ne
    /// [3] w   [4]     [5] e
    /// [6] sw  [7] s   [8] se
    ///
    /// Now, consider when the device rotates.
    /// Depending on which direction the device is
    /// facing, we have different labels. For all
    /// 8 directions, this HashMap provides a map for
    /// the positions.
    pub static ref DIRECTION_POSITIONS_IN_CHART: HashMap<&'static str, [&'static str; 9]> = [
        ("n", ["nw", "n", "ne", "w", "", "e", "sw", "s", "se"]),
        ("ne", ["n", "ne", "e", "nw", "", "se", "w", "sw", "s"]),
        ("e", ["ne", "e", "se", "n", "", "s", "nw", "w", "sw"]),
        ("se", ["e", "se", "s", "ne", "", "sw", "n", "nw", "w"]),
        ("s", ["se", "s", "sw", "e", "", "w", "ne", "n", "nw"]),
        ("sw", ["s", "sw", "w", "se", "", "nw", "e", "ne", "n"]),
        ("w", ["sw", "w", "nw", "s", "", "n", "se", "e", "ne"]),
        ("nw", ["w", "nw", "n", "sw", "", "ne", "s", "se", "e"]),
    ].iter().cloned().collect();
}

/// An getter for `DIRECTION_POSITIONS_IN_CHART`.
///
/// Example:
/// ```rust
/// use mikaboshi::compass::get_direction_positions_in_chart;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(direction: &str) -> JsValue {
///     JsValue::from(
///         (match get_direction_positions_in_chart(direction) {
///             Some(positions) => positions.to_vec(),
///             _ => Vec::new(),
///         })
///         .into_iter()
///         .map(JsValue::from)
///         .collect::<js_sys::Array>(),
///     )
/// }
/// ```
pub fn get_direction_positions_in_chart(
    direction: &str,
) -> Option<&[&str; 9]> {
    DIRECTION_POSITIONS_IN_CHART.get(direction)
}

lazy_static! {
    /// A hash map for the opposite direction.
    pub static ref OPPOSITE_DIRECTION: HashMap<&'static str, &'static str> = [
        ("n", "s"),
        ("ne", "sw"),
        ("e", "w"),
        ("se", "nw"),
        ("s", "n"),
        ("sw", "ne"),
        ("w", "e"),
        ("nw", "se"),
    ]
    .iter()
    .cloned()
    .collect();
}

/// A getter for `OPPOSITE_DIRECTION`.
///
/// Example:
/// ```rust
/// use mikaboshi::compass::get_opposite_direction;
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(direction: &str) -> JsValue {
///     JsValue::from(get_opposite_direction(direction))
/// }
/// ```
pub fn get_opposite_direction(dir: &str) -> &str {
    if !OPPOSITE_DIRECTION.contains_key(dir) {
        panic!("Invalid direction: {}", dir);
    }
    OPPOSITE_DIRECTION[dir]
}

/// An array with 24 items. Imagine having a circlar
/// disc displayed on a device screen. When dividing 360
/// by 8 directions, we get 45 degrees for each. When
/// each direction is further divided into 3, then each
/// is called a "sector", and it has 15 degrees for each
/// "sector". Sectors are placed in clockwise order
/// (left to right) for each direction, so that you see
/// the sector 1 being placed on your very left. Then,
/// you see the sector 2 in the middle, and the sector 3
/// on your right. Imagine the device pointing north.
/// On the circular disc, what you see at the very top
/// is the sector 2 of "N" (north), denoted as "N2".
/// On your left, you see "N1". On your right, "N3".
///
/// When we want to express all the 24 sectors, we want
/// an array with 24 items. For the first item in the
/// array [0], it is convenient to have "N2". Then, for
/// the second item in the array [1], we want "N3".
/// For [2], we want "NE1". For [3], we want "NE2".
/// And, so on. As you can imagine, "N1" comes to the
/// very last in the array, or [23].
pub const TWENTYFOUR_SECTORS: [u8; 24] = [
    2, // 0: n
    3, // 1: n
    1, // 2: ne
    2, // 3: ne
    3, // 4: ne
    1, // 5: e
    2, // 6: e
    3, // 7: e
    1, // 8: se
    2, // 9: se
    3, // 10: se
    1, // 11: s
    2, // 12: s
    3, // 13: s
    1, // 14: sw
    2, // 15: sw
    3, // 16: sw
    1, // 17: w
    2, // 18: w
    3, // 19: w
    1, // 20: nw
    2, // 21: nw
    3, // 22: nw
    1, // 23: n
];

lazy_static! {
    /// An array with 24 items, for each represents
    /// each in 二十四山向 (Er-Shi-Si Shan-Xiang).
    /// Note, the array begins with "N2"
    /// (and "N1" is stored at the very last, or [23]).
    /// Ex.
    /// 0: Direction { direction: "n", sector: 2 }
    /// 1: Direction { direction: "n", sector: 3 }
    /// 2: Direction { direction: "ne", sector: 1 }
    /// 3: Direction { direction: "ne", sector: 2 }
    pub static ref TWENTYFOUR_INDEX_TO_DIRECTIONS: Vec<Direction> = {
        let mut vec: Vec<Direction> = DIRECTIONS
            .iter()
            .fold(Vec::new(), |mut acc: Vec<Direction>, &direction: &&str| {
                acc.append(
                    &mut (1..4).map(|sector: usize| {
                        Direction {
                            direction: direction.to_string(),
                            sector,
                        }
                    }).collect()
                );
                acc
            });
        vec.rotate_left(1);
        vec
    };
}

/// A getter for `TWENTYFOUR_INDEX_TO_DIRECTIONS`
///
/// Example:
/// ```rust
/// use mikaboshi::compass::{get_twentyfour_direction_from_index, Direction};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(index: usize) -> JsValue {
///     let dir: &Direction = get_twentyfour_direction_from_index(index);
///     JsValue::from_serde(dir).unwrap()
/// }
/// ```
pub fn get_twentyfour_direction_from_index(
    index: usize,
) -> &'static Direction {
    &TWENTYFOUR_INDEX_TO_DIRECTIONS[index]
}

lazy_static! {
    /// A HashMap mapping direction (combination of "direction" and "sector")
    /// to the corresponding index.
    ///
    /// n2: 0
    /// n3: 1
    /// ne1: 2
    /// ne2: 3
    /// ...
    /// ...
    pub static ref TWENTYFOUR_DIRECTIONS_TO_INDEX: HashMap<String, usize> = TWENTYFOUR_INDEX_TO_DIRECTIONS
        .iter()
        .enumerate()
        .map(|(i, dir)| {
            let key = format!("{}{}", dir.direction, dir.sector);
            (key, i)
        })
        .collect();
}

/// An array with 24 items, each being a tuple.
/// For each tuple, the first represents the type of
/// 二十四山向 (Er-Shi-Si Shan-Xiang), and the second
/// is the index of the type. The type being:
/// [0] BAGUA, [1] STEM, or [2] BRANCH.
pub const TWENTYFOUR_ORDER_START_NORTH: [(
    usize,
    usize,
); 24] = [
    (2, 0),  // 0: [0] 子
    (1, 9),  // 1: [9] 癸
    (2, 1),  // 2: [1] 丑
    (0, 7),  // 3: [7] 艮
    (2, 2),  // 4: [2] 寅
    (1, 0),  // 5: [0] 甲
    (2, 3),  // 6: [3] 卯
    (1, 1),  // 7: [1] 乙
    (2, 4),  // 8: [4] 辰
    (0, 3),  // 9: [3] 巽
    (2, 5),  // 10: [5] 巳
    (1, 2),  // 11: [2] 丙
    (2, 6),  // 12: [6] 午
    (1, 3),  // 13: [3] 丁
    (2, 7),  // 14: [7] 未
    (0, 1),  // 15: [1] 坤
    (2, 8),  // 16: [8] 申
    (1, 6),  // 17: [6] 庚
    (2, 9),  // 18: [9] 酉
    (1, 7),  // 19: [7] 辛
    (2, 10), // 20: [10] 戌
    (0, 5),  // 21: [5] 乾
    (2, 11), // 22: [11] 亥
    (1, 8),  // 23: [8] 壬
];

/// From index, simply returns the corresponding
/// `TwentyFourType`.
///
/// Example:
/// ```rust
/// use mikaboshi::compass::{get_twentyfour_data_from_index, TwentyFourType};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(index: usize) -> JsValue {
///     let t_type: TwentyFourType = get_twentyfour_data_from_index(index);
///     match t_type {
///         TwentyFourType::Gua(gua) => JsValue::from_serde(gua).unwrap(),
///         TwentyFourType::Stem(stem) => JsValue::from_serde(stem).unwrap(),
///         TwentyFourType::Branch(branch) => JsValue::from_serde(branch).unwrap(),
///     }
/// }
/// ```
pub fn get_twentyfour_data_from_index(
    index: usize,
) -> TwentyFourType<'static> {
    let (t_type, t_index) =
        TWENTYFOUR_ORDER_START_NORTH[index];
    match t_type {
        0 => TwentyFourType::Gua(
            &BAGUA_LO_SHU_ORDER_WITH_CENTER[t_index],
        ),
        1 => TwentyFourType::Stem(&STEMS[t_index]),
        2 => {
            TwentyFourType::Branch(&BRANCHES[t_index])
        }
        _ => panic!("Unknown type: {}", t_type),
    }
}

// ===========================================================
// From **DEGREES**
// ===========================================================

/// From the given degrees, returns the corresponding
/// `Direction`.
///
/// Example:
/// ```rust
/// use mikaboshi::compass::{get_twentyfour_direction_from_degrees, Direction};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(degrees: f32) -> JsValue {
///     let dir: Direction = get_twentyfour_direction_from_degrees(degrees);
///     JsValue::from_serde(&dir).unwrap()
/// }
/// ```
pub fn get_twentyfour_direction_from_degrees(
    d: f32,
) -> Direction {
    if !(7.5..352.5).contains(&d) {
        // d >= 352.5 || d < 7.5
        Direction::new("n", 2)
    } else if d < 22.5 {
        Direction::new("n", 3)
    } else if d < 37.5 {
        Direction::new("ne", 1)
    } else if d < 52.5 {
        Direction::new("ne", 2)
    } else if d < 67.5 {
        Direction::new("ne", 3)
    } else if d < 82.5 {
        Direction::new("e", 1)
    } else if d < 97.5 {
        Direction::new("e", 2)
    } else if d < 112.5 {
        Direction::new("e", 3)
    } else if d < 127.5 {
        Direction::new("se", 1)
    } else if d < 142.5 {
        Direction::new("se", 2)
    } else if d < 157.5 {
        Direction::new("se", 3)
    } else if d < 172.5 {
        Direction::new("s", 1)
    } else if d < 187.5 {
        Direction::new("s", 2)
    } else if d < 202.5 {
        Direction::new("s", 3)
    } else if d < 217.5 {
        Direction::new("sw", 1)
    } else if d < 232.5 {
        Direction::new("sw", 2)
    } else if d < 247.5 {
        Direction::new("sw", 3)
    } else if d < 262.5 {
        Direction::new("w", 1)
    } else if d < 277.5 {
        Direction::new("w", 2)
    } else if d < 292.5 {
        Direction::new("w", 3)
    } else if d < 307.5 {
        Direction::new("nw", 1)
    } else if d < 322.5 {
        Direction::new("nw", 2)
    } else if d < 337.5 {
        Direction::new("nw", 3)
    } else {
        // d < 352.5
        Direction::new("n", 1)
    }
}

// ===========================================================
// From **DIRECTION**
// ===========================================================

/// From the given direction and sector, finds the
/// corresponding index in
/// `TWENTYFOUR_DIRECTIONS_TO_INDEX`
pub fn get_twentyfour_index_from_direction(
    direction: &str,
    sector: usize,
) -> usize {
    *TWENTYFOUR_DIRECTIONS_TO_INDEX
        .get(
            format!("{}{}", direction, sector)
                .as_str(),
        )
        .unwrap()
}

/// From the given direction and sector, returns
/// `TwentyFourType`.
///
/// Example:
/// ```rust
/// use mikaboshi::compass::{get_twentyfour_data_from_direction, TwentyFourType};
/// use wasm_bindgen::prelude::*;
///
/// #[wasm_bindgen]
/// pub fn xx(direction: &str, sector: usize) -> JsValue {
///     let t_type: TwentyFourType = get_twentyfour_data_from_direction(direction, sector);
///     match t_type {
///         TwentyFourType::Gua(gua) => JsValue::from_serde(gua).unwrap(),
///         TwentyFourType::Stem(stem) => JsValue::from_serde(stem).unwrap(),
///         TwentyFourType::Branch(branch) => JsValue::from_serde(branch).unwrap(),
///     }
/// }
/// ```
pub fn get_twentyfour_data_from_direction(
    direction: &str,
    sector: usize,
) -> TwentyFourType<'static> {
    get_twentyfour_data_from_index(
        get_twentyfour_index_from_direction(
            direction, sector,
        ),
    )
}

/// From the given direction and sector, returns
/// `Direction`.
pub fn get_twentyfour_direction_from_direction(
    direction: &str,
    sector: usize,
) -> &Direction {
    &TWENTYFOUR_INDEX_TO_DIRECTIONS
        [get_twentyfour_index_from_direction(
            direction, sector,
        )]
}

#[cfg(test)]
mod tests {
    use super::*;

    // TODO: DIRECTION
    // TODO: DIRECTION_POSITIONS_IN_CHART

    #[test]
    fn test_get_direction_positions_in_chart() {
        let exp = [
            "nw", "n", "ne", "w", "", "e", "sw", "s",
            "se",
        ];
        assert_eq!(
            get_direction_positions_in_chart("n")
                .unwrap(),
            &exp
        );
    }

    // TODO: OPPOSITE_DIRECTION
    // TODO: get_opposite_direction
    // TODO: TWENTYFOUR_SECTORS

    #[test]
    fn test_constant_twentyfour_index_to_directions()
    {
        assert_eq!(
            TWENTYFOUR_INDEX_TO_DIRECTIONS[0],
            Direction {
                direction: String::from("n"),
                sector: 2,
            }
        );
    }

    #[test]
    fn test_get_twentyfour_direction_from_index() {
        let exp = Direction {
            direction: String::from("n"),
            sector: 2,
        };
        assert_eq!(
            get_twentyfour_direction_from_index(0),
            &exp
        );
    }

    #[test]
    fn test_constant_twentyfour_directions_to_index()
    {
        assert_eq!(
            *TWENTYFOUR_DIRECTIONS_TO_INDEX
                .get("n2")
                .unwrap(),
            0_usize
        );
    }

    // Only for test
    impl TwentyFourType<'static> {
        fn is_branch(&self) -> bool {
            match self {
                TwentyFourType::Branch(_) => true,
                _ => false,
            }
        }
    }

    // TODO: TWENTYFOUR_ORDER_START_NORTH

    #[test]
    fn test_get_twentyfour_data_from_index() {
        assert!(get_twentyfour_data_from_index(0)
            .is_branch());
    }

    #[test]
    fn test_get_twentyfour_direction_from_degrees() {
        assert_eq!(
            get_twentyfour_direction_from_degrees(
                0_f32
            ),
            Direction {
                direction: String::from("n"),
                sector: 2,
            }
        );
    }

    // TODO: get_twentyfour_index_from_direction
    // TODO: get_twentyfour_data_from_direction
    // TODO: get_twentyfour_direction_from_direction
}
