use std::convert::TryFrom;
use std::fmt::{Display, Error, Formatter};

#[derive(Debug, PartialEq)]
pub enum DayOfWeek {
    Sunday = 0,
    Monday = 1,
    Tuesday = 2,
    Wednesday = 3,
    Thursday = 4,
    Friday = 5,
    Saturday = 6,
}

impl TryFrom<u8> for DayOfWeek {
    type Error = String;

    fn try_from(x: u8) -> Result<Self, Self::Error> {
        use DayOfWeek::*;
        match x {
            0 => Ok(Sunday),
            1 => Ok(Monday),
            2 => Ok(Tuesday),
            3 => Ok(Wednesday),
            4 => Ok(Thursday),
            5 => Ok(Friday),
            6 => Ok(Saturday),
            _ => Err("Invalid day of week".to_string()),
        }
    }
}

impl Display for DayOfWeek {
    fn fmt(&self, f: &mut Formatter) -> Result<(), Error> {
        f.write_str(format!("{:?}", self).as_str())
    }
}

pub trait ShortTitle {
    fn short_title(&self) -> String;
}

impl ShortTitle for DayOfWeek {
    fn short_title(&self) -> String {
        (&format!("{}", self)[..3]).to_string()
    }
}
