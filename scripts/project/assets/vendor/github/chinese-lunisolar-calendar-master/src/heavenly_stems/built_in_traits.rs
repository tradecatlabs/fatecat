use core::str::FromStr;

use super::HeavenlyStems;

impl TryFrom<char> for HeavenlyStems {
    type Error = ();

    #[inline]
    fn try_from(value: char) -> Result<Self, Self::Error> {
        Self::from_char(value).ok_or(())
    }
}

impl FromStr for HeavenlyStems {
    type Err = ();

    #[inline]
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Self::parse_str(s).ok_or(())
    }
}

impl From<HeavenlyStems> for char {
    #[inline]
    fn from(value: HeavenlyStems) -> Self {
        value.to_char()
    }
}

impl AsRef<str> for HeavenlyStems {
    #[inline]
    fn as_ref(&self) -> &str {
        self.to_str()
    }
}
