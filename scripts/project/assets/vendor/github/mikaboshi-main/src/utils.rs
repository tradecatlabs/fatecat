use chrono::Datelike;

// use core::iter::FromIterator;
// use std::iter::FromIterator;
use serde::Deserialize;

// use sowngwala::sun::ecliptic_position_of_the_sun_from_generic_date;

pub fn get_json<'a, T: Deserialize<'a>>(
    json: &'a str,
) -> Vec<T> {
    match serde_json::from_str(json) {
        Ok(json) => json,
        Err(err) => panic!("Error: {}", err),
    }
}

/// For the given Vec, sorts by given order.
pub fn make_sort<T: Clone>(
    order: Vec<u8>,
) -> Box<dyn Fn(Vec<T>) -> Vec<T>> {
    Box::new(move |source: Vec<T>| -> Vec<T> {
        order
            .clone()
            .into_iter()
            .map(|index| {
                source[index as usize].clone()
            })
            .collect()
    })
}

/// Increments by the given step until it becomes more than 0.
pub fn make_positive(
    step: u32,
) -> Box<dyn Fn(i32) -> u32> {
    Box::new(move |mut num: i32| -> u32 {
        let limit = 10000;
        let mut cnt = 0;
        while num < 0 {
            if cnt > limit {
                panic!(
                    "Iteration reached: {}",
                    limit
                );
            }
            num += step as i32;
            cnt += 1;
        }
        num as u32
    })
}

pub fn longitude_of_the_sun_from_generic_date<T>(
    date: T,
) -> f64
where
    T: Datelike,
    T: std::marker::Copy,
    T: std::fmt::Debug,
    T: std::fmt::Display,
{
    // ecliptic_position_of_the_sun_from_generic_date(
    //     date,
    // )
    // 临时返回值
    0.0
}
