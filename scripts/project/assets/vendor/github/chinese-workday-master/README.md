## chinese-workday

今天要上班吗？


[![Build Status][travis-image]][travis-url]

## Install

```bash
$ npm install chinese-workday
```

## Usage

```js
// const { isWorkday, isHoliday, getFestival } = require('chinese-workday');
const ww = require('chinese-workday');
const isWorkday = ww.isWorkday;
const isHoliday = ww.isHoliday;
const getFestival = ww.getFestival;
const isAddtionalWorkday = ww.isAddtionalWorkday;

isWorkday('2022-10-01')
// => false
isHoliday('2022-10-01')
// => true
isAddtionalWorkday('2022-01-29')
// => true
getFestival('2022-10-01')
// => 国庆节
```

[travis-image]: https://travis-ci.org/yize/chinese-workday.svg?branch=master
[travis-url]: https://travis-ci.org/yize/chinese-workday

**Note**: Since 2018
