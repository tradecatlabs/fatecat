//! Information about planets in our solar system.
//! Notice the planets in `PLANETS` are stored in
//! a special order known as _the Ptolemaic Order_.
//! In many ancient traditions, when a man is deceased,
//! he will depart the Earth, and head toward the Moon.
//! Leaving the Moon behind, the Mercury, the Venus,
//! and the Sun. He will continue his journey after
//! the Sun, this time, to _the outer planets_,
//! that are the Mars, the Jupiter, and the Saturn.
//!
//! After all, this library provides methodologies
//! _NOT_ for _"astronomy"_, but for _"astrology"_,
//! hence, follows the tradition which was common to
//! the ancients.
//!
//! Also noteworthy that, according to Rudolf Steiner,
//! "Mercury" was formerly known as "Venus" in ancient
//! times. Yet, it is only so when we are talking about
//! the order of the _physical_ planets, not in its
//! _symbolical_ sense. For instance, when ancients
//! mentioned of "Mercury", it was simply about
//! "Mercury" and not "Venus".
use serde::{Deserialize, Serialize};

use crate::language::{
    Language, LanguageData, LanguageTrait,
    NameDataTrait,
};
use crate::utils::get_json;

/// A struct representing a planet and stores its
/// attributes.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Planet {
    pub name: Language,
}

/// A temporary struct for loading JSON data when
/// defining a static const `PLANETS`.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlanetRawData {
    pub name: LanguageData,
}

impl LanguageTrait for Planet {
    fn name(&self) -> Box<Language> {
        Box::new(self.name.clone())
    }
}

impl NameDataTrait for PlanetRawData {
    fn name(&self) -> Box<LanguageData> {
        Box::new(self.name.clone())
    }
}

lazy_static! {
    /// A static vector with 11 items, each represents
    /// a planet in our solar system. Planets are in
    /// Ptolemaic order.
    ///
    /// [0] Earth
    /// [1] Moon
    /// [2] Mercury
    /// [3] Venus
    /// [4] Sun
    /// [5] Mars
    /// [6] Jupiter
    /// [7] Saturn
    /// [8] Uranus
    /// [9] Neptune
    /// [10] Pluto
    ///
    /// For attributes details stored in the vector is
    /// found in JSON file:
    /// `src/json/planets.json`
    pub static ref PLANETS: Vec<Planet> = {
        let json = &include_str!("../json/planet.json");
        let data: Vec<PlanetRawData> = get_json::<PlanetRawData>(json);
        data.iter()
            .map(|item| Planet {
                name: item.language_from_data(),
            })
            .collect()
    };
}
