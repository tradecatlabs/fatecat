use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageDetails {
    pub alphabet: String, // Ex. "甲"
    pub phonetic: String, // Ex. "jiǎ"
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Language {
    pub en: String,
    pub ja: LanguageDetails,
    pub vi: LanguageDetails,
    pub zh_cn: LanguageDetails,
    pub zh_tw: LanguageDetails,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LanguageData {
    pub en: String,
    pub ja: Vec<String>,
    pub vi: Vec<String>,
    pub zh_cn: Vec<String>,
    pub zh_tw: Vec<String>,
}

impl LanguageDetails {
    pub fn new(
        alphabet: &str,
        phonetic: &str,
    ) -> Self {
        LanguageDetails {
            alphabet: alphabet.to_string(),
            phonetic: phonetic.to_string(),
        }
    }
}

pub trait LanguageTrait {
    fn name(&self) -> Box<Language>;

    /// Chinese character in Taiwanese
    fn alphabet(&self) -> String {
        self.name().zh_tw.alphabet
    }

    /// Chinese phonetic in Taiwanese
    fn phonetic(&self) -> String {
        self.name().zh_tw.phonetic
    }

    /// Japanese character
    fn alphabet_ja(&self) -> String {
        self.name().ja.alphabet
    }
}

pub trait NameDataTrait {
    fn name(&self) -> Box<LanguageData>;

    fn language_details(
        details: &[String],
    ) -> LanguageDetails {
        if details.is_empty() {
            LanguageDetails::new("", "")
        } else {
            LanguageDetails::new(
                &details[0],
                &details[1],
            )
        }
    }

    fn language_from_data(&self) -> Language {
        let name = &self.name();
        Language {
            en: self.name().en,
            ja: Self::language_details(&name.ja),
            vi: Self::language_details(&name.vi),
            zh_cn: Self::language_details(
                &name.zh_cn,
            ),
            zh_tw: Self::language_details(
                &name.zh_tw,
            ),
        }
    }
}
