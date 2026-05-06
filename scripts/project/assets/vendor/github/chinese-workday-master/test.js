var ww = require('./index');
// const { isWorkday, isHoliday, getFestival, isAddtionalWorkday } = require('./index');
var isWorkday = ww.isWorkday;
var isHoliday = ww.isHoliday;
var getFestival = ww.getFestival;
var isAddtionalWorkday = ww.isAddtionalWorkday;

test('isWorkday', function () {
  expect(isWorkday('2018-10-07')).toBe(false);
  expect(isWorkday('2018-10-08')).toBe(true);
  expect(isWorkday('2018-10-21')).toBe(false);
});

test('isHoliday', function () {
  expect(isHoliday('2018-10-07')).toBe(true);
  expect(isHoliday('2018-10-08')).toBe(false);
  expect(isHoliday('2018-10-21')).toBe(true);
});

test('isAddtionalWorkday', function () {
  expect(isAddtionalWorkday('2019-02-02')).toBe(true);
  expect(isAddtionalWorkday('2019-02-01')).toBe(false);
});

test('getFestival', function () {
  expect(getFestival('2018-02-11')).toBe('补春节');
  expect(getFestival('2018-10-07')).toBe('国庆节');
  expect(getFestival('2018-10-08')).toBe('工作日');
  expect(getFestival('2018-10-21')).toBe('周末');
});

test('dateformat', function () {
  expect(isWorkday('2018/10/08')).toBe(true);
  expect(isWorkday(1538981142948)).toBe(true);
  expect(isWorkday('2018-10-07')).toBe(false);
  expect(isWorkday()).toBe(true);
})