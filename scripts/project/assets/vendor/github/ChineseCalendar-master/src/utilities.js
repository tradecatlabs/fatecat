"use strict";

/* Gather functions related to dates and years */

// Compute JD at midnight UT
function getJD(yyyy,mm,dd) {
    let m1 = mm, yy = yyyy;
    if (m1 <= 2) {m1 +=12; yy--;}
    let b;
    if (10000*yy+100*m1+dd <= 15821004) {
        // Julian calendar
        b = -2 + Math.floor((yy+4716)/4) - 1179;
    } else {
        // Gregorian calendar
        b = Math.floor(yy/400) - Math.floor(yy/100) + Math.floor(yy/4);
    }
    let jd = 365*yy - 679004 + b + Math.floor(30.6001*(m1+1)) + dd + 2400000.5;
    return jd;
}

// Number of days in a Gregorian/Julian year
function NdaysGregJul(y) {
  let ndays = (y==1582 ? 355:365) + (Math.abs(y) % 4 == 0 ? 1:0);
  if (y > 1582) {
     ndays += (y % 100 == 0 ? -1:0) + (y % 400 == 0 ? 1:0);
  }
  return ndays;
}

// Name of Western Calendar
function get_Western_calendar_name(y) {
    if (y >1582) {
        return ['Gregorian','格里曆','格里历'];
    } else if (y==1582) {
        return ['Julian/Gregorian','儒略曆/格里曆','儒略历/格里历'];
    } else if (y > 7) {
        return ['Julian','儒略曆','儒略历'];
    } else {
        return ['(Proleptic) Julian','逆推儒略曆','逆推儒略历'];
    }
}
