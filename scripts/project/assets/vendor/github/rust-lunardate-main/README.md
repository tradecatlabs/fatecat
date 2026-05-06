# rust-lunardate

[![GitHub Actions](https://github.com/messense/rust-lunardate/workflows/CI/badge.svg)](https://github.com/messense/rust-lunardate/actions?query=workflow%3ACI)
[![Crates.io](https://img.shields.io/crates/v/lunardate.svg)](https://crates.io/crates/lunardate)
[![codecov](https://codecov.io/gh/messense/rust-lunardate/branch/master/graph/badge.svg)](https://codecov.io/gh/messense/rust-lunardate)
[![docs.rs](https://docs.rs/lunardate/badge.svg)](https://docs.rs/lunardate/)

A Chinese Calendar Library in Rust

## Limits

This library can only deal with year from 1900 to 2099 (in Chinese calendar).

## Installation

Add it to your ``Cargo.toml``:

```toml
[dependencies]
lunardate = "0.2"
```

Add ``extern crate lunardate`` to your crate root if you are using Rust 2015 edition and your're good to go!

## License

This work is released under the MIT license. A copy of the license is provided in the [LICENSE](./LICENSE) file.
