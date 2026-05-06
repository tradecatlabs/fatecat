use std::f64::consts::PI;

pub use dow::DayOfWeek;
use std::convert::TryInto;
use std::fmt::{Display, Error, Formatter};

pub mod dow;

pub const TZ: f64 = 7.0;

pub trait Calendar {
    fn to_julian_days(&self) -> i32;
    fn from_julian_days(_: i32) -> Self;
    fn to_gregorian(&self) -> GregorianDay {
        GregorianDay::from_julian_days(self.to_julian_days())
    }
    fn to_lunar(&self) -> LunarDay {
        LunarDay::from_julian_days(self.to_julian_days())
    }

    fn day_of_week(&self) -> DayOfWeek {
        (((self.to_julian_days() + 1) % 7) as u8)
            .try_into()
            .unwrap()
    }
}

#[derive(Debug, Clone)]
pub struct Day {
    pub day: i32,
    pub month: i32,
    pub year: i32,
}

#[derive(Debug, Clone)]
pub struct GregorianDay {
    pub inner: Day,
}

#[derive(Debug)]
pub struct LunarDay {
    pub inner: Day,
    pub leap: bool,
}

impl Display for LunarDay {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result<(), Error> {
        f.write_str(
            format!(
                "{:02}/{:02}/{:04}{}AL",
                self.inner.day,
                self.inner.month,
                self.inner.year,
                if self.leap { "*" } else { " " }
            )
            .as_str(),
        )
    }
}

impl Display for GregorianDay {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result<(), Error> {
        f.write_str(
            format!(
                "{:02}/{:02}/{:04}",
                self.inner.day, self.inner.month, self.inner.year
            )
            .as_str(),
        )
    }
}

#[derive(Debug)]
pub struct GregorianMonth {
    year: i32,
    month: i32,
}

#[derive(Debug)]
pub struct GregorianDayRange {
    begin: GregorianDay,
    end: GregorianDay,
}

impl GregorianDayRange {
    pub fn iter(&self) -> GregorianIter {
        GregorianIter {
            inner: self.begin.clone(),
            left: self.end.to_julian_days() - self.begin.to_julian_days() + 1,
        }
    }

    pub fn to_tuple(&self) -> (GregorianDay, GregorianDay) {
        (self.begin.clone(), self.end.clone())
    }
}

pub struct GregorianIter {
    inner: GregorianDay,
    left: i32,
}

impl<'a> Iterator for GregorianIter {
    type Item = GregorianDay;

    fn next(&mut self) -> Option<Self::Item> {
        if self.left <= 0 {
            return None;
        }
        let ret = Some(self.inner.clone());
        self.left -= 1;
        self.inner = GregorianDay::from_julian_days(self.inner.to_julian_days() + 1);
        ret
    }
}

impl GregorianMonth {
    pub fn new(year: i32, month: i32) -> GregorianMonth {
        Self { month, year }
    }
    pub fn get_bound(&self) -> GregorianDayRange {
        let mut last_day_of_month = 32;
        while GregorianDay::from_julian_days(
            GregorianDay::new(last_day_of_month, self.month, self.year).to_julian_days(),
        )
        .inner
        .day > 1
        {
            last_day_of_month -= 1;
        }
        GregorianDayRange {
            begin: GregorianDay {
                inner: Day {
                    month: self.month,
                    year: self.year,
                    day: 1,
                },
            },
            end: GregorianDay {
                inner: Day {
                    month: self.month,
                    year: self.year,
                    day: last_day_of_month - 1,
                },
            },
        }
    }
    pub fn previous(&self) -> GregorianMonth {
        let mut year = self.year;
        let mut month = self.month - 1;
        if month <= 0 {
            month += 12;
            year -= 1;
        }
        GregorianMonth { month, year }
    }
    pub fn next(&self) -> GregorianMonth {
        let mut year = self.year;
        let mut month = self.month + 1;
        if month > 12 {
            month -= 12;
            year += 1;
        }
        GregorianMonth { month, year }
    }

    pub fn to_title(&self) -> String {
        format!("Am lich {:02}/{:04}", self.month, self.year)
    }
}

impl GregorianDay {
    pub fn new(day: i32, month: i32, year: i32) -> Self {
        Self {
            inner: Day { day, month, year },
        }
    }

    pub fn to_month(&self) -> GregorianMonth {
        GregorianMonth {
            year: self.inner.year,
            month: self.inner.month,
        }
    }
}

impl Calendar for GregorianDay {
    // Check: Passed
    fn to_julian_days(&self) -> i32 {
        let a = ((14 - self.inner.month) / 12) as f64;
        let y = (self.inner.year as f64 + 4800.0) - a;
        let m = self.inner.month as f64 + 12.0 * a - 3.0;
        let mut jd = self.inner.day as f64
            + ((153.0 * m + 2.0) / 5.0).floor()
            + 365.0 * y
            + (y / 4.0).floor()
            - (y / 100.0).floor()
            + (y / 400.0).floor()
            - 32045.0;
        if jd < 2299161.0 {
            jd = self.inner.day as f64
                + ((153.0 * m + 2.0) / 5.0).floor()
                + 365.0 * y
                + (y / 4.0).floor()
                - 32083.0;
        }
        jd as i32
    }

    // Check: Passed
    fn from_julian_days(jd: i32) -> Self {
        let jd = jd as f64;
        let (b, c) = if jd > 2299160.0 {
            // After 5/10/1582, Gregorian calendar
            let a = jd + 32044.0;
            let b = ((4.0 * a + 3.0) / 146097.0).floor();
            let c = a - (b * 146097.0 / 4.0).floor();
            (b, c)
        } else {
            (0.0, jd + 32082.0)
        };
        let d = ((4.0 * c + 3.0) / 1461.0).floor();
        let e = c - ((1461.0 * d) / 4.0).floor();
        let m = ((5.0 * e + 2.0) / 153.0).floor();
        let day = e - ((153.0 * m + 2.0) / 5.0).floor() + 1.0;
        let month = m + 3.0 - 12.0 * (m / 10.0).floor();
        let year = b * 100.0 + d - 4800.0 + (m / 10.0).floor();
        Self {
            inner: Day {
                day: day as i32,
                month: month as i32,
                year: year as i32,
            },
        }
    }
}

impl LunarDay {
    // Check: Passed
    fn get_new_moon_day(k: f64, tz: f64) -> f64 {
        let t = k / 1236.85; // Time in Julian centuries from 1900 January 0.5
        let tt = t * t;
        let ttt = tt * t;
        let dr = PI / 180.0;
        let mut jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * tt - 0.000000155 * ttt;
        jd1 = jd1 + 0.00033 * ((166.56 + 132.87 * t - 0.009173 * tt) * dr).sin(); // Mean new moon
        let m = 359.2242 + 29.10535608 * k - 0.0000333 * tt - 0.00000347 * ttt; // Sun's mean anomaly
        let mpr = 306.0253 + 385.81691806 * k + 0.0107306 * tt + 0.00001236 * ttt; // Moon's mean anomaly
        let f = 21.2964 + 390.67050646 * k - 0.0016528 * tt - 0.00000239 * ttt; // Moon's argument of latitude
        let mut c1 = (0.1734 - 0.000393 * t) * (m * dr).sin() + 0.0021 * (2.0 * dr * m).sin();
        c1 = c1 - 0.4068 * (mpr * dr).sin() + 0.0161 * (dr * 2.0 * mpr).sin();
        c1 = c1 - 0.0004 * (dr * 3.0 * mpr).sin();
        c1 = c1 + 0.0104 * (dr * 2.0 * f).sin() - 0.0051 * (dr * (m + mpr)).sin();
        c1 = c1 - 0.0074 * (dr * (m - mpr)).sin() + 0.0004 * (dr * (2.0 * f + m)).sin();
        c1 = c1 - 0.0004 * (dr * (2.0 * f - m)).sin() - 0.0006 * (dr * (2.0 * f + mpr)).sin();
        c1 = c1 + 0.0010 * (dr * (2.0 * f - mpr)).sin() + 0.0005 * (dr * (2.0 * mpr + m)).sin();
        let delta_t = if t < -11.0 {
            0.001 + 0.000839 * t + 0.0002261 * tt - 0.00000845 * ttt - 0.000000081 * t * ttt
        } else {
            -0.000278 + 0.000265 * t + 0.000262 * tt
        };
        let jd_new = jd1 + c1 - delta_t;
        (jd_new + 0.5 + tz / 24.0).floor()
    }

    // Check: Passed
    fn get_sun_longitude(jd: f64, tz: f64) -> f64 {
        let t = (jd - 2451545.5 - tz / 24.0) / 36525.0; // Time in Julian centuries from 2000-01-01 12:00:00 GMT
        let tt = t * t;
        let dr = PI / 180.0; // degree to radian
        let m = 357.52910 + 35999.05030 * t - 0.0001559 * tt - 0.00000048 * t * tt; // mean anomaly, degree
        let l0 = 280.46645 + 36000.76983 * t + 0.0003032 * tt; // mean longitude, degree
        let mut dl = (1.914600 - 0.004817 * t - 0.000014 * tt) * (dr * m).sin();
        dl =
            dl + (0.019993 - 0.000101 * t) * (dr * 2.0 * m).sin() + 0.000290 * (dr * 3.0 * m).sin();
        let mut l = l0 + dl; // true longitude, degree
        l = l * dr;
        l = l - PI * 2.0 * ((l / (PI * 2.0)).floor()); // Normalize to (0, 2*PI)
        (l / PI * 6.0).floor()
    }

    // Check: Passed
    fn get_lunar_month_11(y: f64, tz: f64) -> f64 {
        let off = GregorianDay::new(31, 12, y as i32).to_julian_days() as f64 - 2415021.0;
        let k = (off / 29.530588853).floor();
        let mut nm = Self::get_new_moon_day(k, tz);
        let sun_long = Self::get_sun_longitude(nm, tz); // sun longitude at local midnight
        if sun_long >= 9.0 {
            nm = Self::get_new_moon_day(k - 1.0, tz);
        }
        nm
    }

    fn get_leap_month_offset(a11: f64, tz: f64) -> f64 {
        let k = ((a11 - 2415021.076998695) / 29.530588853 + 0.5).floor();
        let mut last;
        let mut i = 1.0; // We start with the month following lunar month 11
        let mut arc = Self::get_sun_longitude(Self::get_new_moon_day(k + i, tz), tz);
        loop {
            last = arc;
            i += 1.0;
            arc = Self::get_sun_longitude(Self::get_new_moon_day(k + i, tz), tz);
            if arc == last || i >= 14.0 {
                break;
            }
        }
        i - 1.0
    }
}

impl Calendar for LunarDay {
    fn to_julian_days(&self) -> i32 {
        let a11;
        let b11;
        if self.inner.month < 11 {
            a11 = Self::get_lunar_month_11(self.inner.year as f64 - 1.0, TZ);
            b11 = Self::get_lunar_month_11(self.inner.year as f64, TZ);
        } else {
            a11 = Self::get_lunar_month_11(self.inner.year as f64, TZ);
            b11 = Self::get_lunar_month_11(self.inner.year as f64 + 1.0, TZ);
        }
        let mut off = self.inner.month as f64 - 11.0;
        if off < 0.0 {
            off += 12.0;
        }
        let mut leap_month;
        let leap_off;
        if b11 - a11 > 365.0 {
            leap_off = Self::get_leap_month_offset(a11, TZ);
            leap_month = leap_off - 2.0;
            if leap_month < 0.0 {
                leap_month += 12.0;
            }
            if self.leap && self.inner.month as f64 != leap_month {
                panic!("WRONG!");
            } else if self.leap || off >= leap_off {
                off += 1.0;
            }
        }
        let k = (0.5 + (a11 - 2415021.076998695) / 29.530588853).trunc();
        let month_start = Self::get_new_moon_day(k + off, TZ);
        (month_start + self.inner.day as f64 - 1.0) as i32
    }

    fn from_julian_days(jd: i32) -> Self {
        let greg = GregorianDay::from_julian_days(jd);
        let jd = jd as f64;
        let k = ((jd - 2415021.076998695) / 29.530588853).trunc();
        let mut month_start = Self::get_new_moon_day(k + 1.0, TZ);
        if month_start > jd {
            month_start = Self::get_new_moon_day(k, TZ);
        }
        let mut a11 = Self::get_lunar_month_11(greg.inner.year as f64, TZ);
        let mut b11 = a11;
        let mut lunar_year;
        if a11 >= month_start {
            lunar_year = greg.inner.year;
            a11 = Self::get_lunar_month_11(greg.inner.year as f64 - 1.0, TZ);
        } else {
            lunar_year = greg.inner.year + 1;
            b11 = Self::get_lunar_month_11(greg.inner.year as f64 + 1.0, TZ);
        }
        let lunar_day = jd - month_start + 1.0;
        let diff = ((month_start - a11) / 29.0).trunc();
        let mut lunar_leap = 0;
        let mut lunar_month = diff + 11.0;
        let leap_month_diff;
        if b11 - a11 > 365.0 {
            leap_month_diff = Self::get_leap_month_offset(a11, TZ);
            if diff >= leap_month_diff {
                lunar_month = diff + 10.0;
                if diff == leap_month_diff {
                    lunar_leap = 1;
                }
            }
        }
        if lunar_month > 12.0 {
            lunar_month = lunar_month - 12.0;
        }
        if lunar_month >= 11.0 && diff < 4.0 {
            lunar_year -= 1;
        }
        Self {
            inner: Day {
                day: lunar_day as i32,
                month: lunar_month as i32,
                year: lunar_year,
            },
            leap: lunar_leap == 1,
        }
    }
}
