"use strict";

function init(lang) {
    if (window.location === window.parent.location) { 
        document.getElementById('wrapper0').style.display = "block";
        header(lang,'', 'Julian'); // print menu
        let dat = new Date(); // current time from computer's clock
        let y = dat.getFullYear();
        let mm = dat.getMonth()+1;
        let dd = dat.getDate();
        let h=12, m=0, s=0;
        document.getElementById('midnight').checked = false;
        document.getElementById('noon').checked = true;
        document.getElementById('custom').checked = false;
        document.getElementById('year').value = y;
        document.getElementById('month').value = mm;
        document.getElementById('date').value = dd;
        document.getElementById('hour').value = h;
        document.getElementById('minute').value = m;
        document.getElementById('second').value = s;
        document.getElementById('hour').disabled = true;
        document.getElementById('minute').disabled = true;
        document.getElementById('second').disabled = true;
        getJDSexagenary(lang, document.getElementById('calendarDate'));
        
        let input = document.getElementById('JD');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('JDBtn').click();
            }
        });
        input = document.getElementById('year');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
        input = document.getElementById('month');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
        input = document.getElementById('date');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
        input = document.getElementById('hour');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
        input = document.getElementById('minute');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
        input = document.getElementById('second');
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('tabBtn').click();
            }
        });
    } else {
        exception_handler();
    }
}

function changeInputTime(lang, s) {
    s = parseInt(s, 10);
    if (s==0 || s==12) {
        document.getElementById('hour').value = s;
        document.getElementById('minute').value = 0;
        document.getElementById('second').value = 0;
        document.getElementById('hour').disabled = true;
        document.getElementById('minute').disabled = true;
        document.getElementById('second').disabled = true;
    } else {
        document.getElementById('hour').disabled = false;
        document.getElementById('minute').disabled = false;
        document.getElementById('second').disabled = false;
    }
    if (document.getElementById('err').innerHTML == "") {
        getJDSexagenary(lang, document.getElementById('calendarDate'));
    }
}

function getJDSexagenary(lang, form) {
    document.getElementById('err').innerHTML = "";
    document.getElementById('output').innerHTML = "";
    // sanity check
    let errid = 'err';
    let y = parseInt(form.year.value, 10);
    let min = parseInt(form.year.min, 10);
    let max = parseInt(form.year.max, 10);
    let str = ['Year', '年份', '年份'];
    let message = generate_message(lang, str[lang], min, max);
    sanityCheck(y, 'year', min, max, message, errid);
    let mm = parseInt(form.month.value, 10);
    min = parseInt(form.month.min, 10);
    max = parseInt(form.month.max, 10);
    str = ['Month', '月份', '月份'];
    message = generate_message(lang, str[lang], min, max);
    sanityCheck(mm, 'month', min, max, message, errid);
    let dd = parseInt(form.date.value, 10);
    min = parseInt(form.date.min, 10);
    max = parseInt(form.date.max, 10);
    str = ['Date', '日期', '日期'];
    message = generate_message(lang, str[lang], min, max);
    sanityCheck(dd, 'date', min, max, message, errid);
    let h = parseInt(form.hour.value, 10);
    min = parseInt(form.hour.min, 10);
    max = parseInt(form.hour.max, 10);
    str = ['Hour', '小時', '小时'];
    message = generate_message(lang, str[lang], min, max);
    sanityCheck(h, 'hour', min, max, message, errid);
    let m = parseInt(form.minute.value, 10);
    min = parseInt(form.minute.min, 10);
    max = parseInt(form.minute.max, 10);
    str = ['Minute', '分鐘', '分钟'];
    message = generate_message(lang, str[lang], min, max);
    sanityCheck(m, 'minute', min, max, message, errid);
    let s = parseInt(form.second.value, 10);
    min = parseInt(form.second.min, 10);
    max = parseInt(form.second.max, 10);
    str = ['Second', '秒的', '秒的'];
    message = generate_message(lang, str[lang], min, max);
    sanityCheck(s, 'second', min, max, message, errid);
    
    if (document.getElementById('err').innerHTML=='') {
        if (y==1582 && mm==10 && dd>4 && dd<15) { dd += 10;}
        let JDnoon = getJDnoon(y,mm,dd);
        let facJD = h/24.0 + m/1440.0 + s/86400.0 - 0.5;
        //if (h==0 && m==0 && s==0) { facJD += (jd < 0 ? -1e-7:1e-7);}
        let jd = JDnoon + facJD;
        write_output(lang, JDnoon, jd);
        // reset background color for JD
        document.getElementById('JD').style.backgroundColor = 'transparent';
    }
}

function JDtoCalendar(lang) {
    document.getElementById('err').innerHTML = "";
    document.getElementById('output').innerHTML = "";
    let jd = parseFloat(document.getElementById('JD').value);
    let max = 5373850.499988, min = -1931442.5;
    let message;
    if (lang==0) {
        message = 'Invalid Julian date input! Please enter a number between '+min+' and '+max+'.';
    } else if (lang==1) {
        message = '儒略日數輸入錯誤!請輸入在 '+min+' 和 '+max+' 之間的數字。' ;
    } else {
        message = '儒略日数输入错误!请输入在 '+min+' 和 '+max+' 之间的数字。' ;
    }
    sanityCheck(jd, 'JD', min, max, message, 'err');
    
    if (document.getElementById('err').innerHTML=='') {
        let JDnoon = Math.floor(jd+0.5);
        write_output(lang, JDnoon, jd);
        // reset background colors
        let id = ['year', 'month', 'date', 'hour', 'minute', 'second'];
        id.forEach(x => document.getElementById(x).style.backgroundColor = 'transparent');
    }
}

function generate_message(lang, str, min, max) {
    let txt;
    if (lang==0) {
        txt = 'Invalid '+str+' input! Please input a number between '+min+' and '+max+'.';
    } else if (lang==1) {
        txt = str+'輸入錯誤!請輸入包括 '+min+' 和 '+max+' 之間的整數。';
    } else {
        txt = str+'输入错误！请输入包括 '+min+' 和 '+max+' 之间的整数。';
    }
    return txt;
}

function write_output(lang, JDnoon, jd) {
    let jdRound = parseFloat(jd.toFixed(6));
    document.getElementById('JD').value = jdRound;
    let dat = CalDat(jd);
    let langVars = langConstant(lang);
    let y = dat.yy, mm = dat.mm, dd = dat.dd;
    let h = dat.h, m = dat.m, s = dat.s;
    let form = document.getElementById('calendarDate');
    form.year.value = y;
    form.month.value = mm;
    form.date.value = dd;
    form.hour.value = h;
    form.minute.value = m;
    form.second.value = s;
    let noon = document.getElementById('noon');
    let midnight = document.getElementById('midnight');
    let custom = document.getElementById('custom');
    if (h==0 && m==0 && s==0) {
        if (noon.checked) {
            noon.checked = false;
            midnight.checked = true;
        }
    } else if (h==12 && m==0 && s==0) {
        if (midnight.checked) {
            midnight.checked = false;
            noon.checked = true;
        }
    } else {
        if (midnight.checked || noon.checked) {
            midnight.checked = false;
            noon.checked = false;
            custom.checked = true;
            document.getElementById('hour').disabled = false;
            document.getElementById('minute').disabled = false;
            document.getElementById('second').disabled = false;
        }
    }
    let txt, cal,year;
    let w = (JDnoon + 1) % 7;
    if (w < 0) { w += 7;}
    let sexNum = (JDnoon - 11) % 60;
    if (sexNum < 0) {sexNum += 60;}
    let ih = sexNum % 10, ie = sexNum % 12;
    if (lang==0) {
        txt = '<br /><h3><u>Result</u></h3><p style="color:blue;">';
        cal = 'Date in '+(JDnoon > 2299160 ? 'Gregorian ':(y < 8 ? 'Proleptic Julian':'Julian'))+' calendar: ';
        year = (y > 0 ? y+' CE':(1-y)+' BCE');
        txt += cal+dd+' '+langVars.gMonth[mm-1]+', '+year;
        txt += '&nbsp;&nbsp;&nbsp; Time: '+dat.timeString+'</p>';
        txt += '<p style="color:blue;">Julian date = '+jdRound+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;day of week: ';
        txt += langVars.weeks[w]+'</p>'
        txt += '<p style="color:blue;">Sexagenary date: '+langVars.heaven[ih]+' '+langVars.earth[ie]+' (sexagenary number = '+(sexNum+1)+')</p>';
    } else if (lang==1) {
        txt = '<br /><h3><u>計 算 結 果</u></h3><p style="color:blue;">';
        cal = '公曆日期: ';
        year = (y > 0 ? '公元'+y:'公元前'+(1-y))+'年';
        txt += cal+year+mm+'月'+dd+'日';
        txt += ',&nbsp; 時間: '+dat.timeString+'</p>';
        txt += '<p style="color:blue;">儒略日數:'+jdRound+',&nbsp;';
        txt += langVars.weeks[w]+'</p>'
        txt += '<p style="color:blue;">日干支: '+langVars.heaven[ih]+langVars.earth[ie]+'(干支數='+(sexNum+1)+')</p>';
    } else {
        txt = '<br /><h3><u>计 算 结 果</u></h3><p style="color:blue;">';
        cal = '公历日期: ';
        year = (y > 0 ? '公元'+y:'公元前'+(1-y))+'年';
        txt += cal+year+mm+'月'+dd+'日';
        txt += ',&nbsp; 时间: '+dat.timeString+'</p>';
        txt += '<p style="color:blue;">儒略日数:'+jdRound+',&nbsp;';
        txt += langVars.weeks[w]+'</p>'
        txt += '<p style="color:blue;">日干支: '+langVars.heaven[ih]+langVars.earth[ie]+'(干支数='+(sexNum+1)+')</p>';
    }
    document.getElementById('output').innerHTML = txt;
}

// Compute JD at noon
function getJDnoon(yyyy,mm,dd) {
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
    let jd = 365*yy - 679004 + b + Math.floor(30.6001*(m1+1)) + dd + 2400001;
    return jd;
}

//----------------------------------------------------------
// CalDat: Calendar date and time from D (number of days 
// from J2000)
// 
// yy,mm,dd Calendar date components
// h, m, s hour, min, sec.
// 
// Ported from Astronomy on Personal Computer, p. 15-16
//-------------------------------------------------
function CalDat(jdin) {
    let a,b,c,d,e,f;
    // Convert Julian day number to calendar date
    let jd = jdin + 0.5/86400; // for rounding
    a = Math.floor(jd+0.5);
    if (a < 0) {
        return CalDatNegativeJD(jd);
    }
    if (a < 2299161) { //Julian calendar
        b = 0; c = a+1524;
    } else { // Gregorian calendar
        b = Math.floor((a-1867216.25)/36524.25);
        c = a + b - Math.floor(0.25*b) + 1525;
    }
    d = Math.floor((c-122.1)/365.25);
    if (d < 0) {d++;}
    e = 365*d + Math.floor(0.25*d);
    f = Math.floor((c-e)/30.6001);
    if (f < 0) {f++;}
    let dd = c-e - Math.floor(30.6001*f);
    let mm = f - 1 - 12*Math.floor(f/14+1e-5);
    let yy = d - 4715 - Math.floor((7+mm)/10+1e-5);
    let dateString = generateDateString(yy,mm,dd);
    let FracOfDay = jd - Math.floor(jd+0.5) + 0.5;
    let Hour = 24*FracOfDay;
    let h = Math.floor(Hour);
    let m = Math.floor(60*(Hour-h));
    let s = Math.floor((Hour - h - m/60)*3600);
    let timeString = generateTimeString(h,m,s);
    return {yy:yy, mm:mm, dd:dd, h:h, m:m, s:s, 
           dateString:dateString, timeString:timeString};
}

//----------------------------------------------------------
// CalDat: Calendar date and time from Julian date JD with JD<0
// 
// yy,mm,dd Calendar date components
// h, m, s hour, min, sec.
// 
//-------------------------------------------------
function CalDatNegativeJD(jdin) {
    let jd = jdin + 0.5/86400; // for rounding
    let mjd = -Math.floor(jd+0.5);
    let md = mjd - Math.floor(mjd/1461);
    let dyear = Math.floor(md/(365+1e-10)) + 1;
    let yyyy = -4712 - dyear;
    let mjd0 = dyear*365 + Math.floor(dyear/4) + 1;
    let dFromY = mjd0 - mjd;
    let monthTable;
    if (dyear % 4 ==0) {
       monthTable = [0, 31, 60, 91, 121, 152, 182, 213, 244, 
                    274, 305, 335, 366];
    } else {
       monthTable = [0, 31, 59, 90, 120, 151, 181, 212, 243, 
                    273, 304, 334, 365];
    }
    let i,mm,dd;
    for (i=1; i<13; i++) {
        if (dFromY <= monthTable[i]) {
            mm = i;
            dd = dFromY - monthTable[i-1];
            break;
        }
    }
    let dateString = generateDateString(yyyy,mm,dd);
    let FracOfDay = 0.5+ (jd + mjd);
    let Hour = 24*FracOfDay;
    let h = Math.floor(Hour);
    let m = Math.floor(60*(Hour-h));
    let s = Math.floor((Hour - h - m/60)*3600);
    let timeString = generateTimeString(h,m,s);
    return {yy:yyyy, mm:mm, dd:dd, h:h, m:m, s:s, 
           dateString:dateString, timeString:timeString};
}

// Generate date string from yyyy, mm and dd:
// return yyyy-mm-dd
function generateDateString(yyyy,mm,dd) {
    let absy = Math.abs(yyyy);
    if (absy < 10) {
        absy = "000"+absy;
    } else if (absy < 100) {
        absy = "00"+absy;
    } else if (absy < 1000) {
        absy = "0"+absy;
    } else {
        absy = absy.toString();
    }
    let yStr = absy;
    if (yyyy < 0) {yStr = "-"+yStr;}
    let mmString = mm.toString();
    if (mm < 10) {mmString = "0"+mmString;}
    let ddString = dd.toString();
    if (dd < 10) {ddString = "0"+ddString;}
    return yStr+"-"+mmString+"-"+ddString;
}

// Generate time string from h,m,s: 
// return hh:mm:ss 
function generateTimeString(h,m,s) {
    let hround = h + m/60 + (s+0.5)/3600;
    let hh = Math.floor(hround);
    let mm = Math.floor((hround-hh)*60);
    let ss= Math.floor(3600*(hround-hh-mm/60));
    hh = hh.toString(); mm = mm.toString(); ss = ss.toString();
    if (hh.length < 2) {hh = "0"+hh;}
    if (mm.length < 2) {mm = "0"+mm;}
    if (ss.length < 2) {ss = "0"+ss;}
    return hh+":"+mm+":"+ss;
}

// Language-specific constants
function langConstant(lang) {
    let gMonth, weeks, heaven, earth, animal, month_num, monthL, 
        Qnames, soltermNames, note_early, note_late, note1929, note1914;
    
    let gMonthEng = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"];
    let weeksEng = ["Sunday", "Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday"];
    let heavenEng = ["Ji&#462;","Y&#464;","B&#464;ng","D&#299;ng","W&#249;", 
                  "J&#464;", "G&#275;ng","X&#299;n","R&#233;n", "Gu&#464;"];
    let earthEng = ["z&#464;", "ch&#466;u", "y&#237;n", "m&#462;o", "ch&#233;n", 
                "s&#236;", "w&#468;", "w&#232;i", "sh&#275;n", "y&#466;u", 
                "x&#363;", "h&#224;i"];
    let gMonthChi = ["1 月;", "2 月", "3 月", 
                  "4 月", "5 月", "6 月", 
                  "7 月", "8 月", "9 月", 
                  "10 月", "11 月", 
                  "12 月"];
    let weeksChi =["星期日", "星期一", "星期二", "星期三", "星期四", 
                   "星期五", "星期六"];
    let heavenChi = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"];
    let earthChi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    
    if (lang==0) {
        // English
        gMonth = gMonthEng;
        weeks = weeksEng;
        heaven = heavenEng;
        earth = earthEng;
    } else {
        // Chinese
        gMonth = gMonthChi;
        weeks = weeksChi;
        heaven = heavenChi;
        earth = earthChi;
    } 
    
    return {gMonth:gMonth, weeks:weeks, lang:lang, heaven:heaven, earth:earth};
}

// sanity check
// If there are errors, print message in red at the place 
// indicated by the id errid
function sanityCheck(x,inputId,min,max,message,errid) {
    document.getElementById(inputId).style.backgroundColor = 'transparent';
    if (isNaN(x) || x < min || x > max) {
        document.getElementById(inputId).style.backgroundColor = "#e2a8a8";
        let text = '<p style="color:red;">'+message+'</p>';
        document.getElementById(errid).innerHTML += text;
    }
}
