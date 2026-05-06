"use strict";

function init(lang) {
    if (window.location === window.parent.location) {
        document.getElementById("wrapper0").style.display = "block";
        header(lang,'calendar', 'index'); // print menu
        let year = 99999999;
        let input = document.getElementById('year');
        // Get input from url
        const p = new URLSearchParams(window.location.search);
        if (p.has('y')) {
            year = parseInt(p.get('y'), 10);
        }
        if (isNaN(year) || year < -721 || year > 2200) {
        let d = new Date(); // current time from computer's clock
        year = d.getFullYear();
        }
        input.value = year;
        input.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                document.getElementById('myBtn').click();
            }
        });
        if (p.has('showJD')) {
            if (p.get('showJD')=='true') {
                document.getElementById('Julian1').checked = true;
                document.getElementById('Julian0').checked = false;
            }
        }
        submitYear(lang);
    } else {
        exception_handler();
    } 
    // *** TEST ***
    //outputContent_forTesting_allYears_default(lang);
    //outputContent_forTesting_period(lang, 'SpringWarring');
    //outputContent_forTesting_period(lang, 'ShuWu');
    //outputContent_forTesting_period(lang, 'SouthNorth');
    //outputContent_forTesting_period(lang, 'LiaoJinYuan');
    // ***
}

function submitYear(lang) {
    document.getElementById('err').innerHTML = "";
    let year = parseInt(document.getElementById('year').value, 10);
    if (isNaN(year) || year < -721 || year > 2200) {
        let message = ['Invalid input! Please enter an integer between -721 and 2200.', 
        '輸入錯誤﹗請輸入包括 -721 和 2200 之間的整數。','输入错误！请输入包括 -721 和 2200 之间的整数。'];
        document.getElementById('err').innerHTML = message[lang];
    } else {
        if (year < -220) {
           ancient_calendar_handler(lang, year);
        } else {
            document.getElementById("Spring").style.display = "none"; 
            document.getElementById("Warring").style.display = "none"; 
        }
        calendar(lang, year);
    }
}

// Show/hide between show/hide Jilian day number at noon
function showHideJulian(lang,ins) {
    let s = parseInt(ins, 10);
    document.getElementById('Julian'+ins).checked = true;
    document.getElementById('Julian'+(1-s)).checked = false;
    if (document.getElementById('err').innerHTML == '') {
        submitYear(lang);
    }
}

// Language-specific constants
function langConstant(lang) {
    let gMonth, weeks, heaven, earth, animal, month_num, monthL, 
        Qnames, soltermNames, note_early, note_late, note1929, note1914;
    
    let gMonthEng = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"];
    let weeksEng = ["Sun", "Mon", "Tue","Wed","Thu","Fri","Sat"];
    let heavenEng = ["Ji&#462;","Y&#464;","B&#464;ng","D&#299;ng","W&#249;", 
                  "J&#464;", "G&#275;ng","X&#299;n","R&#233;n", "Gu&#464;"];
    let earthEng = ["z&#464;", "ch&#466;u", "y&#237;n", "m&#462;o", "ch&#233;n", 
                "s&#236;", "w&#468;", "w&#232;i", "sh&#275;n", "y&#466;u", 
                "x&#363;", "h&#224;i"];
    let animalEng = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Goat",
                 "Monkey","Chicken","Dog","Pig"];
    let month_numEng = ["1","2","3","4","5","6","7","8","9","10","11","12"];
    let monthLEng = ["S", "L"];
    let QnamesEng = ["Q0", "Q1", "Q2", "Q3"];
    let note_earlyEng = "The lunar conjunction/new moon (Q0) is close to the midnight. The start day of the month may be one day earlier.";
    let note_lateEng = "The lunar conjunction/new moon (Q0) is close to the midnight. The start day of the month may be one day later.";
    let note1929Eng = "Note that the lunar conjunction/new moon (Q0) occurred past the midnight of the second day of the month. Before 1929, the times of lunar conjunction were calculated for the Beijing meridian (116&deg;25' E), which are about 14 minutes earlier than the times listed here based on the meridians of 120&deg;E. This explains why the lunar conjunction date listed here is one day later than the first day of the month.";
    let note1914Eng = "Note that the lunar conjunction/new moon (Q0) did not fall on the first day of the month. This was caused by two factors: 1) Before 1929, the times of lunar conjunction were calculated for the Beijing meridian (116&deg;25'E), which are about 14 minutes earlier than the times listed here based on the meridians of 120&deg;E; 2) Before 1914, the method used to calculate the lunar conjunction was not very accurate.";
    let soltermNamesEng = ["J12", "Z12", "J1", "Z1", "J2", "Z2 (March equinox)", "J3","Z3", 
                         "J4", "Z4", "J5", "Z5 (June solstice)", "J6", "Z6", "J7", "Z7", 
                        "J8", "Z8 (Sep. equinox)", "J9", "Z9", "J10", "Z10", "J11", "Z11 (Dec. solstice)", "J12"];
    
    let gMonthChi = ["1 月", "2 月", "3 月", "4 月", "5 月", "6 月", 
                  "7 月", "8 月", "9 月", "10 月", "11 月", "12 月"];
    let weeksChi =["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    let heavenChi = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"];
    let earthChi = ["子","丑","寅","卯","辰", "巳", "午", "未", "申", "酉", "戌", "亥"];
    let animalChi = ["鼠", "牛", "虎", "兔", "龍", "蛇", "馬", "羊", "猴", "雞", "狗", "豬"];
    let animalSim = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"];
    let month_numChi = ["正","二","三","四","五", "六","七","八","九","十", 
                    "十一","十二"];
    let date_numChi = ["初一"];
    for (let i=2; i<11; i++) {
        date_numChi.push("初"+month_numChi[i-1]);
    }
    date_numChi.push("十一");
    for (let i=12; i<20; i++) {
        date_numChi.push("十"+month_numChi[i-11]);
    }
    date_numChi.push("二十");
    date_numChi.push("廿一");
    for (let i=22; i<30; i++) {
        date_numChi.push("廿"+month_numChi[i-21]);
    }
    date_numChi.push("三十");
    let monthLChi = ["小","大"];
    let QnamesChi = ["朔", "上弦", "望", "下弦"];
    let soltermNamesChi = ["小寒", "大寒", "立春", "雨水", "驚蟄", "春分", 
                          "清明", "穀雨", "立夏", "小滿", "芒種", "夏至", 
                          "小暑", "大暑", "立秋", "處暑", "白露", "秋分", 
                          "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", 
                          "小寒"];
    let soltermNamesSim = ["小寒", "大寒", "立春", "雨水", "惊蛰", "春分", 
                           "清明", "谷雨", "立夏", "小满", "芒种", "夏至", 
                           "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", 
                           "小寒"];
        
    let note_earlyChi = "朔的時刻接近午夜零時，初一或會提早一天。";
    let note_lateChi = "朔的時刻接近午夜零時，初一或會推遲一天。";
    let note_earlySim = "朔的时刻接近午夜零时，初一或会提早一天。";
    let note_lateSim = "朔的时刻接近午夜零时，初一或会推迟一天。";
    let note1929Chi = "注意朔的時刻稍稍過了初二的零時。這是因為1929年以前的朔日計算是用北京地方時(東經116&deg;24')，而本網頁列出的時間卻是用現時全國通行的東經120&deg;標準時。 東經120&deg;標準時比北京地方時遲約14分鐘，這就是朔的時刻過了初二零時的緣故。";
    let note1914Chi = "注意合朔時刻不在初一日，這是由兩個因數造成。其一是1929年以前的朔日計算是用北京地方時(東經116&deg;24')，而本網頁列出的時間卻是用現時全國通行的東經120&deg;標準時， 東經120&deg;標準時比北京地方時遲約14分鐘。其二是1914年前用的合朔計算方法不是很準確。";
    let note1929Sim = "注意朔的时刻稍稍过了初二的零时。这是因为1929年以前的朔日计算是用北京地方时(东经116&deg;24')，而本网页列出的时间却是用现时全国通行的东经120&deg;标准时。 东经120&deg;标准时比北京地方时迟约14分钟，这就是朔的时刻过了初二零时的缘故。";
    let note1914Sim = "注意合朔时刻不在初一日，这是由两个因数造成。其一是1929年以前的朔日计算是用北京地方时(东经116&deg;24')，而本网页列出的时间却是用现时全国通行的东经120&deg;标准时， 东经120&deg;标准时比北京地方时迟约14分钟。其二是1914年前用的合朔计算方法不是很准确。";
    
    if (lang==0) {
        // English
        gMonth = gMonthEng;
        weeks = weeksEng;
        heaven = heavenEng;
        earth = earthEng;
        animal = animalEng;
        month_num = month_numEng;
        monthL = monthLEng;
        Qnames = QnamesEng;
        soltermNames = soltermNamesEng;
        note_early = note_earlyEng;
        note_late = note_lateEng;
        note1929 = note1929Eng;
        note1914 = note1914Eng;
    } else if (lang==1) {
        // Chinese
        gMonth = gMonthChi;
        weeks = weeksChi;
        heaven = heavenChi;
        earth = earthChi;
        animal = animalChi;
        Qnames = QnamesChi;
        soltermNames = soltermNamesChi;
        month_num = month_numChi;
        monthL = monthLChi;
        note_early = note_earlyChi;
        note_late = note_lateChi;
        note1929 = note1929Chi;
        note1914 = note1914Chi;
    } else {
        // Simplified Chinese
        gMonth = gMonthChi;
        weeks = weeksChi;
        heaven = heavenChi;
        earth = earthChi;
        animal = animalSim;
        Qnames = QnamesChi;
        soltermNames = soltermNamesSim;
        month_num = month_numChi;
        monthL = monthLChi;
        note_early = note_earlySim;
        note_late = note_lateSim;
        note1929 = note1929Sim;
        note1914 = note1914Sim;
    }
    let julian; 
    try {
        julian = document.getElementById('Julian1').checked;
    }
    catch (err) {
        julian = false;
    }
    return {gMonth:gMonth, weeks:weeks, lang:lang, heaven:heaven, earth:earth, animal:animal, region:'default', cmonth:month_num, monthL:monthL, Qnames:Qnames, soltermNames:soltermNames, julian:julian, li_ancient:null, 
    date_numChi:date_numChi, note_early:note_early, 
    note_late:note_late, note1929:note1929, note1914:note1914};
}

// Convert the jian number to month number, determine the year number offset 
// and the month number for the first month of a year.
// jian number: 1=yin, 2=mao, ..., 11=zi, 12 = chou
// month number depends on the jian of the month 1, which is
// usually the same as the jian number but they are different
// in certain periods in the Chinese history. 
// year offset: 0 if the year number doesn't change, 
//             -1 if in the previous year,  +1 if in the following year.
function jianToMonthYearoffset(jianIn, y, region) {
    let jian = Math.abs(jianIn);
    let yearOffset=0, monNum=jian;
    
    // Han dynasty
    if (y < -103 && jian > 9) {
        yearOffset = 1;
    }
    
    // Xin dynasty
    if (y==8 && jian==12) {
        monNum = 1;
        yearOffset = 1;
    }
    if (y > 8 && y < 23) {
        monNum = (jian==12 ? 1:jian+1);
        if (jian==12) { yearOffset = 1;}
    }
    if (y==23 && jian<12) {
        monNum = jian+1;
    }
    
    // Wei dynasty (Three-Kingdom period)
    if ( ( (y==237 && jian>2) || (y==238) || (y==239 && jian<12) ) && region=='default') {
        monNum = (jian==12 ? 1:jian+1);
        if (jian==12) { yearOffset = 1;}
    }
    
    // Tang dynasty
    if (y > 688 && y < 700) {
        if (jian > 10) { yearOffset = 1;}
    }
    if (y==761 && jian > 10) {
        monNum = jian - 10;
        yearOffset = 1;
    }
    if (y==762 && jian < 4) {
        monNum = jian + 2;
    }
    
    if (jianIn < 0) { monNum = -monNum; }
    
    return {monNum:monNum, yearOffset:yearOffset};
}

// Determine the month number for the first month of a year.
// This is usually just 1 but is different in some periods
function firstMonthNum(y) {
    let firstMonth = 1;
    if (y < -102) { firstMonth = 10;}
    if (y > 689 && y < 701) { firstMonth = 11;}
    return firstMonth;
}

// Decompress time: time t has been compressed to retain information 
// to the nearest minute. The compression algorithm is 
// t = floor(x)*1441 + m, where x is the original time expressed 
// in the number of days from Jan 0. The inverse transform is 
// y = floor(t/1441), x_approx = y + (t - y*1441)/1440
function decompress_time(t) {
    let x = [];
    for (let i=0; i<t.length; i++) {
        let y = Math.floor(t[i]/1441);
        let m = t[i] - 1441*y;
        if (m > 1439.5) { m = 1439.9;}
        x.push(y + m/1440.0);
    }
    return x;
}

// Calendrical data for year y
function calDataYear(y, langVars) {
    // *** Data for Gregorian/Julian calendar ***
    
    // Is y a leap year?
    let ndays = NdaysGregJul(y);
    let leap = (ndays==366 ? 1:0);
    // number of days in the beg of the 12 months
    let mday = [0, 31, 59+leap, 90+leap, 120+leap, 151+leap, 181+leap, 212+leap, 243+leap, 273+leap, 304+leap, 334+leap, 365+leap];
    if (y==1582) {
        mday = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 294, 324, 355];
    }
    // Julian day on Dec 30, y-1 at noon UT
    let jd0 = Math.floor(getJD(y-1,12,30) + 1);
    // number of days in year y-1, will be used below
    let ndays1 = NdaysGregJul(y-1);
    
    // *** 24 solar terms in year y **
    let offsets = offsets_sunMoon();
    let solarAll = solarTerms();
    let inds = y - solarTermMoonPhase_ystart();
    let solar = solarAll[inds];
    let solar2 = [solar.pop()];
    solar = decompress_solarTerms(y, 1, offsets.solar, solar);
    // solar[] contains solar terms in year y starting from 
    // J12 (Xiaohan) to J11 (daxue). It stores the dates 
    // of the solar terms counting from Dec. 31, y-1 at 0h (UTC+8).
    
    // solar2[] contains the compressed winter solstice in year y.
    // Add one more to solar2 if J12 occurs before Jan 3.
    if (solar[0] < 4323) {
        solar2.push(solarAll[inds+1][0]);
    }
    solarAll = null; // remove large array
    solar2 = decompress_solarTerms(y+1, 0, offsets.solar, solar2);
    let i;
    for (i=0; i < solar2.length; i++) { solar.push(solar2[i]+ndays*1441);}
    solar = decompress_time(solar);
    
    // ** new moons, quarters and full moons in year y **
    let Q0 = (newMoons())[inds]; Q0.unshift(0);
    let Q1 = (firstQuarters())[inds]; Q1.unshift(1);
    let Q2 = (fullMoons())[inds]; Q2.unshift(2);
    let Q3 = (thirdQuarters())[inds]; Q3.unshift(3);
    Q0 = decompress_moonPhases(y, offsets.lunar, Q0, 1);
    Q1 = decompress_moonPhases(y, offsets.lunar, Q1, 1);
    Q2 = decompress_moonPhases(y, offsets.lunar, Q2, 1);
    Q3 = decompress_moonPhases(y, offsets.lunar, Q3, 1);
    // decompress moon phase data
    Q0 = decompress_time(Q0); Q1 = decompress_time(Q1); 
    Q2 = decompress_time(Q2); Q3 = decompress_time(Q3); 
    // Q0 contains all the new moons in year y in chronological order.
    // It stores the dates of new moons counting from 
    // Dec. 31, y-1 at 0h (UTC+8).
    // Q1-Q3 are the same but for 1st quarters, full moons 
    // and 3rd quarters
    
    // eclipses
    let iec = y - eclipse_year_range()[0];
    // sol_eclipse is a 2D array that stores the info of solar 
    // eclipses in year y. It has the form 
    // [[d_eclipse1, ind_eclipse1, type_eclipse1], 
    //  [d_eclipse2, ind_eclipse2, type_eclipse2], ...]
    // d: eclipse day counting from Dec 31, y-1.
    // ind: index of the eclipse (for eclipse link)
    // type: type of eclipse (0=partial, 1=annular, 2=total, 3=hybrid)
    let links = solar_eclipse_link();
    let sol_eclipse = links[iec];
    let extra_links = links[iec-1];
    extra_links.forEach(function(e) {
        if (ndays1 - e[0] < 3) {
            // this is close to Jan 1, y; add it to be safe
            sol_eclipse.push([e[0]-ndays1, e[1], e[2]]);
        }
    });
    extra_links = links[iec+1];
    extra_links.forEach(function(e) {
        if (e[0] < 3) {
            // this is close to Dec 31, y; add it to be safe
            sol_eclipse.push([e[0]+ndays, e[1], e[2]]);
        }
    });
    // lun_eclipse is a 2D array that stores the info of lunar 
    // eclipses in year y. It has the form 
    // [[d_eclipse1, ind_eclipse1, type_eclipse1], 
    //  [d_eclipse2, ind_eclipse2, type_eclipse2], ...]
    // d: eclipse day counting from Dec 31, y-1.
    // ind: index of the eclipse (for eclipse link)
    // type: type of eclipse (0=penumbral, 1=partial, 2=total)
    links = lunar_eclipse_link();
    let lun_eclipse = links[iec];
    extra_links = links[iec-1];
    extra_links.forEach(function(e) {
        if (ndays1 - e[0] < 3) {
            // this is close to Jan 1, y; add it to be safe
            lun_eclipse.push([e[0]-ndays1, e[1], e[2]]);
        }
    });
    extra_links = links[iec+1];
    extra_links.forEach(function(e) {
        if (e[0] < 3) {
            // this is close to Dec 31, y; add it to be safe
            lun_eclipse.push([e[0]+ndays, e[1], e[2]]);
        }
    });
    links = null;
    
    // Before year -104
    if (y < -104) {
        let out = calDataYear_ancient(y, jd0, ndays, mday, solar, Q0, Q1, Q2, Q3, langVars.li_ancient);
        out.sol_eclipse = sol_eclipse;
        out.lun_eclipse = lun_eclipse;
        return out;
    }
    
    // *** Data for Chinese calendar ***
    let region = langVars.region;
    let cdate, ind, cmdate1, cmdate, pingqi, ncdays, ncdays1;
    if (region=='default') {
        cdate = ChineseToGregorian();
        // cdate is a 2D array. Each row contains data for a Chinese year
        // columns: year, first date of month 1, 2,... , 12, leap month, 
        //          month # that is leaped, # of days in the year
        // leap month = month # = 0 if no leap month
        ind = y - cdate[0][0];
        // Chinese months in the previous year
        cmdate1 = sortMonths(cdate[ind-1]);
        ncdays1 = cdate[ind-1][15]; // Number of days in the previous year
        // Chinese months in the current year
        cmdate = sortMonths(cdate[ind]);
        ncdays = cdate[ind][15]; // Number of days in this year
        cdate = null;
    } else {
        cdate = setup_region_calendar(region, y-1, false);
        cmdate1 = sortMonths(cdate);
        ncdays1 = cdate[15];
        cdate = setup_region_calendar(region, y, true);
        cmdate = sortMonths(cdate.cm); pingqi = cdate.pingqi;
        ncdays = cdate.cm[15];
        cdate = null;
    }
    // Gather Chinese months within year y
    let d, n = cmdate1.cmonthDate.length;
    let cmonthDate=[], cmonthJian=[], cmonthNum=[], cmonthLong = [], cmonthYear = [];
    // cmonthXiaYear: Chinese year according to the Xia calendar (yin month being the 
    //                first month); 0 means previous year, 1 current year.
    let cmonthXiaYear = []; 
    let jian, jianInfo; // jian number: 1=yin, 2=mao, ...
    for (i=2; i<n; i++) {
        if (cmdate1.cmonthDate[i] > ndays1+1) {
            // cmdate1.cmonthDate[i-1] is the last month before Jan 1, y
            for (let j=i-1; j<n; j++) {
                cmonthDate.push(cmdate1.cmonthDate[j] - ndays1);
                cmonthXiaYear.push(0);
                jian = cmdate1.cmonthNum[j];
                cmonthJian.push(jian);
                jianInfo = jianToMonthYearoffset(jian, y-1, region);
                cmonthNum.push(jianInfo.monNum);
                cmonthYear.push(jianInfo.yearOffset);
                if (j < n-1) {
                    d = cmdate1.cmonthDate[j+1] - cmdate1.cmonthDate[j];
                } else {
                    d = ncdays1 - cmdate1.cmonthDate[j] + cmdate1.cmonthDate[0];
                }
                cmonthLong.push(d==30 ? 1:0);
            }
            break;
        }
        if (i==n-1) {
            // The last Chinese month is the last month before Jan 1, y
           cmonthDate.push(cmdate1.cmonthDate[i] - ndays1);
           cmonthXiaYear.push(0);
           jian = cmdate1.cmonthNum[i];
           cmonthJian.push(jian); 
           jianInfo = jianToMonthYearoffset(jian, y-1, region);
           cmonthNum.push(jianInfo.monNum);
           cmonthYear.push(jianInfo.yearOffset);
           d = ncdays1 - cmdate1.cmonthDate[i] + cmdate1.cmonthDate[0];
           cmonthLong.push(d==30 ? 1:0);
        }
    }
    n = cmdate.cmonthDate.length;
    for (i=0; i<n; i++) {
        if (cmdate.cmonthDate[i] <= ndays) {
           cmonthDate.push(cmdate.cmonthDate[i]); 
           cmonthXiaYear.push(1);
           jian = cmdate.cmonthNum[i];
           cmonthJian.push(jian);
           jianInfo = jianToMonthYearoffset(jian, y, region);
           cmonthNum.push(jianInfo.monNum);
           cmonthYear.push(1 + jianInfo.yearOffset);
           if (i < n-1) {
                d = cmdate.cmonthDate[i+1] - cmdate.cmonthDate[i];
            } else {
                d = ncdays - cmdate.cmonthDate[i] + cmdate.cmonthDate[0];
            }
            cmonthLong.push(d==30 ? 1:0);
        }
    }
    
    let out = {jd0:jd0, mday:mday, cmonthDate:cmonthDate, cmonthXiaYear, 
               cmonthJian:cmonthJian, cmonthNum:cmonthNum, 
               cmonthYear:cmonthYear, cmonthLong:cmonthLong,             
               solar:solar,  Q0:Q0, Q1:Q1, Q2:Q2, Q3:Q3, year:y, 
               sol_eclipse:sol_eclipse, lun_eclipse:lun_eclipse};
    if (region != 'default') {
        out.pingqi = pingqi;
    }
    return out;
}

// Sort the Chinese months in chronological order by placing 
// the leap month to the appropriate place
function sortMonths(cmdate) {
    let cmonthDate = [];
    let cmonthNum = []; // Jian number
    let leapM = cmdate[14];
    let i;
    if (leapM==0) {
        for (i=0; i<12; i++) {
            cmonthDate.push(cmdate[i+1]);
            cmonthNum.push(i+1);
        }
    } else {
        for (i=0; i<leapM; i++) {
            cmonthDate.push(cmdate[i+1]);
            cmonthNum.push(i+1);
        }
        cmonthDate.push(cmdate[13]);
        cmonthNum.push(-leapM);
        for (i=leapM+1; i<13; i++) {
            cmonthDate.push(cmdate[i]);
            cmonthNum.push(i);
        }
    }
    return {cmonthDate:cmonthDate, cmonthNum:cmonthNum};
}

// Set up the calendar for the Gregorian/Julian year
function calendar(lang, year) {
    let langVars = langConstant(lang);
    langVars.region = split_calendar_handler(lang,year);
    let calVars = calDataYear(year, langVars);
    let txt = '';
    
    // How many Chinese years does this Gregorian/Julian calendar span?
    let n = calVars.cmonthDate.length;
    let Ncyear = calVars.cmonthYear[n-1] - calVars.cmonthYear[0] + 1;
    
    // Determine the date(s) of the Chinese new year
    let i,j,k,mm,dd;
    let mm1 = [], dd1 = [];
    let firstMonth = [0,0,0];
    for (i=0; i<3; i++) {
       if (year > -110) {
           firstMonth[i] = firstMonthNum(year-1+i);
       } else {
           firstMonth[i] = calVars.firstMonthNum;
       }
    }
    for (i=1; i<Ncyear; i++) {
        let firstMon = firstMonth[calVars.cmonthYear[0] + i];
        for(j=1; j<n; j++) {
            if (calVars.cmonthYear[j]==calVars.cmonthYear[0]+i && 
                calVars.cmonthNum[j]==firstMon) {
                dd = calVars.cmonthDate[j];
                for (k=0; k<13; k++) {
                    if (dd <= calVars.mday[k]) {
                        mm = k;
                        break;
                    }
                }
                mm1.push(mm); dd1.push(dd - calVars.mday[mm-1]);
            }
        }
    }
    
    let ih0 = (year + 725) % 10;
    let ie0 = (year + 727) % 12;
    if (ih0 < 0) { ih0 += 10;}
    if (ie0 < 0) { ie0 += 12;}
    let cyear = [" ", " ", " "];
    cyear[0] = langVars.heaven[ih0]+' '+langVars.earth[ie0]+' ('+langVars.animal[ie0]+')';
    let ih = (year + 726) % 10;
    let ie = (year + 728) % 12;
    if (ih < 0) { ih += 10;}
    if (ie < 0) { ie += 12;}
    cyear[1] = langVars.heaven[ih]+' '+langVars.earth[ie]+' ('+langVars.animal[ie]+')';
    let ih2 = (year + 727) % 10;
    let ie2 = (year + 729) % 12;
    if (ih2 < 0) { ih2 += 10;}
    if (ie2 < 0) { ie2 += 12;}
    cyear[2] = langVars.heaven[ih2]+' '+langVars.earth[ie2]+' ('+langVars.animal[ie2]+')';
    let gcal = (year > 1582 ? "Gregorian":(year > 7 ? "Julian":"(Proleptic) Julian"));
    if (year==1582) { gcal = "Gregorian/Julian";}
    let yearc = year.toString();
    if (year < 1) {
        yearc += (lang==0 ? ' ('+(1-year)+' BCE)':' (前'+(1-year)+')');
    }
    let cy0 = calVars.cmonthYear[0];
    if (lang==0) {
        txt += '<h1>'+gcal+' Year: '+yearc+'</h1>';
        txt += '<h1>Chinese year:</h1>'
        if (Ncyear==1) {
            txt += '<h2>'+cyear[cy0]+'</h2> <br />';
        } else if (Ncyear==2) {
            txt += '<h2>'+cyear[cy0]+' before '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+',<br />'+cyear[cy0+1]+' on and after '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+'</h2> <br />';
        } else {
            txt += '<h2>'+cyear[cy0]+' before '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+',<br />'+cyear[cy0+1]+' between '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+' and '+langVars.gMonth[mm1[1]-1]+' '+(dd1[1]-1)+',<br />'+cyear[cy0+2]+' on and after '+langVars.gMonth[mm1[1]-1]+' '+dd1[1]+'</h2> <br />';
        }      
    } else {
        if (lang==1) {
            gcal = '('+(year > 1582 ? '格里曆':(year > 7 ? '儒略曆':'逆推儒略曆'))+')';
            if (year==1582) { gcal = "(儒略曆/格里曆)";}
            cyear[0] += eraName(year-1, langVars.region);
            cyear[1] += eraName(year, langVars.region);
            cyear[2] += eraName(year+1, langVars.region);
        } else {
            gcal = '('+(year > 1582 ? '格里历':(year > 7 ? '儒略历':'逆推儒略历'))+')';
            if (year==1582) { gcal = "(儒略历/格里历)";}
            cyear[0] += eraNameSim(year-1, langVars.region);
            cyear[1] += eraNameSim(year, langVars.region);
            cyear[2] += eraNameSim(year+1, langVars.region);
        }
        if (lang==1) {
            txt += '<h1>公曆年'+gcal+': '+yearc+'</h1>';
            txt += '<h1>農曆年:</h1>';
        } else {
            txt += '<h1>公历年'+gcal+': '+yearc+'</h1>';
            txt += '<h1>农历年:</h1>';
        }
        let tmp;
        if (Ncyear==1) {
            txt += '<h2>'+cyear[cy0]+'</h2> <br />';
        } else if (Ncyear==2) {
            tmp = '<h2>'+mm1[0]+'月'+dd1[0]+'日前: '+cyear[cy0]+', ';
            if (year < 1912) {
                tmp += '<br />';
            }
            if (year==24 && lang > 0) { 
                tmp = '<h2>'+mm1[0]+'月'+dd1[0]+'日前: 癸 未 (羊)('+(lang==1 ? '漢':'汉')+'更始元年),<br />';
            }
            let tmp2 = (lang==1 ? '日及以後: ':'日及以后: ');
            tmp += mm1[0]+'月'+dd1[0]+tmp2+cyear[cy0+1]+'</h2><br />';
            txt += tmp;
        } else {
            let tmp2 = (lang==1 ? '日及以後: ':'日及以后: ');
            txt += '<h2>'+mm1[0]+'月'+dd1[0]+'日前: '+cyear[cy0]+',<br /> '+mm1[0]+'月'+dd1[0]+'日至'+mm1[1]+'月'+(dd1[1]-1)+'日: '+cyear[cy0+1]+',<br />'+mm1[1]+'月'+dd1[1]+tmp2+cyear[cy0+2]+'</h2><br />';
        }
    }
    
    if (lang==0) {
        cyear[0] = langVars.heaven[ih0]+' '+langVars.earth[ie0];
        cyear[1] = langVars.heaven[ih]+' '+langVars.earth[ie];
        cyear[2] = langVars.heaven[ih2]+' '+langVars.earth[ie2];
    } else {
        cyear[0] = langVars.heaven[ih0]+langVars.earth[ie0]+'年';
        cyear[1] = langVars.heaven[ih]+langVars.earth[ie]+'年';
        cyear[2] = langVars.heaven[ih2]+langVars.earth[ie2]+'年';
    }
    
    // Add additional information after the year info
    let info = addYearInfo(year, langVars, calVars);
    if (info != "") {
        let h3 = (lang==0 ? '<h3 style="color:brown;line-height:26px;">':'<h3 style="color:brown;letter-spacing:4px;line-height:30px;">');
        txt += h3+info+'</h3><br /><br />';
    }
    
    for (let m=0; m<12; m++) {
        txt += printMonth(m, lang, year, cyear, firstMonth, 
                                    langVars, calVars);
    }
    
    document.getElementById('calendar').innerHTML = txt;
}

function addYearInfo(y, langVars, calVars) {
    let info = '', lang = langVars.lang, region = langVars.region;
    
    // Qin and early Han dynasty
    if (y >= -220 && y <= -103) {
        if (lang==0) {
            info = "The calendars used between 221 BCE and 104 BCE were modified versions of the Zhuanxu calendar, one of the old calendars used in the third century BCE in the state of Qin. The first month was the h&#224;i month (present-day month 10). However, it was still called month 10 instead of month 1. The numerical order of the months in a year was 10, 11, 12, 1, 2, ..., 9. The intercalary month was placed at the end of a year, called post month 9. There was a major calendar reform in 104 BCE, where the first month of a year was changed to month 1 and the intercalary month was placed in the month that did not contain a major solar term. The Chinese year in 104 BCE had 15 Chinese months as a result of the change.<br />The calendars in this period are reconstructed according to the description in the article \"Researches on Calendars from Qin to early Han (246 B.C. to 104 B.C.) &mdash; centering on excavated calendrical bamboo slips\" (秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心), L&#464; Zh&#333;ngl&#237;n (李忠林), in <i>Studies in Chinese History</i> (《中国史研究》), issue no. 2, pp. 17&ndash;69 (2012). Our computation method is explained on <a href='QinHanCalendars.html'>this page</a>.";
        } else if (lang==1) {
            info = "秦朝及漢初(公元前221年 &ndash; 前104年)的曆法沿用顓頊曆的月序。顓頊曆是古六曆之一，據說戰國後期在秦國使用。顓頊曆以建亥(即今天的十月)為年首，但仍稱建亥為十月。月的數序是十月、十一月、十二月、正月、二月……九月，閏月置於年終，稱為後九月。秦朝的曆法與顓頊曆稍有不同。漢朝建立後基本上沿用秦曆，一百年間只作了少許修改，直到漢武帝太初元年(公元前104年)才頒行新曆法，以建寅(正月)為年首，並把閏月置於無中氣的月份，這使公元前104年的農曆年有十五個農曆月。秦朝為了避秦始皇名諱(正、政同音)，把正月改稱「端月」，到漢朝又改回正月。這裡沒有跟從歷史，在秦朝仍稱建寅為正月。<br />本網頁這時期的復原日曆是根據李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，發表於《中国史研究》2012年第2期第17&ndash;69頁。具體計算方法在<a href='QinHanCalendars_chinese.html'>秦與漢初曆法網頁</a>闡述。";
        } else {
            info = "秦朝及汉初(公元前221年 &ndash; 前104年)的历法沿用颛顼历的月序。颛顼历是古六历之一，据说战国后期在秦国使用。颛顼历以建亥(即今天的十月)为年首，但仍称建亥为十月。月的数序是十月、十一月、十二月、正月、二月……九月，闰月置于年终，称为后九月。秦朝的历法与颛顼历稍有不同。汉朝建立后基本上沿用秦历，一百年间只作了少许修改，直到汉武帝太初元年(公元前104年)才颁行新历法，以建寅(正月)为年首，并把闰月置于无中气的月份，这使公元前104年的农历年有十五个农历月。秦朝为了避秦始皇名讳(正、政同音)，把正月改称「端月」，到汉朝又改回正月。这里没有跟从历史，在秦朝仍称建寅为正月。<br />本网页这时期的复原日历是根据李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，发表于《中国史研究》2012年第2期第17&ndash;69页。具体计算方法在<a href='QinHanCalendars_simp.html'>秦与汉初历法网页</a>阐述。";
        }
    }
    
    // Xin dynasty
    if (y >= 9 && y <= 23) {
        if (lang==0) {
            info = "The Xin dynasty was established in 9 CE The ch&#466;u month (present day month 12) was designated as the first month of a year; the y&#237;n month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. As a result, the Chinese year in 8 CE (W&#249; ch&#233;n) had only 11 months. When the Xin dynasty was overthrown in 23 CE, the month numbers were switched back with month 1 being the y&#237;n month again.";
            if (y==23) {
                info += '<br />As a result, the Chinese year in 23 CE had two sets of calendar: one for the Xin dynasty (ch&#466;u month being the first month) and the other for the restored Han dynasty (y&#237;n month being the first month), also known as Gengshi. The two sets of calendar had 11 overlapping months: months 2-12 in the Xin calendar were the same as months 1-11 in the Gengshi calendar.';
            }
        } else if (lang==1) {
            info = "公元9年，王莽建立新朝，改正朔以殷正建丑(即現在的十二月)為年首，故公元8年的農曆年(戊辰年)只有十一個月。農曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。新朝於地皇四年(癸未年，公元23年)亡，綠林軍擁立漢淮南王劉玄为帝，改元更始元年，恢復以建寅(即現在的正月)為年首。";
            if (y==23) {
                info += '<br />地皇四年和更始元年有十一個月重疊。地皇四年用丑正、更始元年用寅正，所以地皇四年二至十二月相當於更始元年正至十一月。';
            }
        } else {
            info = "公元9年，王莽建立新朝，改正朔以殷正建丑(即现在的十二月)为年首，故公元8年的农历年(戊辰年)只有十一个月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。新朝于地皇四年(癸未年，公元23年)亡，绿林军拥立汉淮南王刘玄为帝，改元更始元年，恢复以建寅(即现在的正月)为年首。";
            if (y==23) {
                info += '<br />地皇四年和更始元年有十一个月重叠。地皇四年用丑正、更始元年用寅正，所以地皇四年二至十二月相当于更始元年正至十一月。';
            }
        }
    }
    
    // Wei dynasty 
    if (y >= 237 && y <= 240 && region=='default') {
        if (lang==0) {
            info = "In 237 CE, emperor Mingdi of the Wei dynasty declared that the ch&#466;u month (present day month 12) would be the first month of a year; the y&#237;n month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. The new system was imposed after month 2 in the Chinese year in 237, in which month 4 was followed by month 2. When the emperor died in 239 CE, the month numbers were switched back with month 1 being the y&#237;n month again in the following year. As a result, the Chinese year in 239 had 13 months, where month 12 appeared twice.";
        } else if (lang==1) {
            info = "魏青龍五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即現在的十二月)為年首，二月後實施，並改元景初元年。所以丁巳年沒有三月份，二月後的月份是四月。農曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。景初三年（公元239年）明帝駕崩,次年恢復以建寅(即現在的正月)為年首。景初三年有兩個十二月。";
        } else {
            info = "魏青龙五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即现在的十二月)为年首，二月后实施，并改元景初元年。所以丁巳年没有三月份，二月后的月份是四月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。景初三年（公元239年）明帝驾崩,次年恢复以建寅(即现在的正月)为年首。景初三年有两个十二月。";
        }
    }
    
    // Empress Consort Wu
    if (y >= 689 && y<= 700) {
        if (lang==0) {
            info = "In December 689, Empress Consort Wu designated the z&#464; month (month 11) as the first month of a year. However, the month numbers did not change. The z&#464; month was named Zheng, which is usually referred to month 1; ch&#466;u month was stilled called month 12; y&#237;n month was month 1 and so on. Here the Zheng month is still labelled as month 11. The first month of a year was changed back to month 1 in February 701. The Chinese year in 689 only had 11 months (one leap month), whereas the Chinese year in 700 had 15 months (one leap month).";
        } else if (lang==1) {
            info = "公元689年12月，武則天改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月，建寅（即現在的正月）改稱一月，其他農曆月的數序不變（即正月、十二月、一月、二月⋯⋯十月）。公元701年2月又改回以建寅為年首。公元689年的農曆年（己丑年）只有十一個月（其中一個月是閏月），而公元700年的農曆年（庚子年）有十五個月（其中一個月是閏月）。";
        } else {
            info = "公元689年12月，武则天改正朔，以周正建子(即现在的十一月)为年首，建子改称正月，建寅（即现在的正月）改称一月，其他农历月的数序不变（即正月、十二月、一月、二月__十月）。公元701年2月又改回以建寅为年首。公元689年的农历年（己丑年）只有十一个月（其中一个月是闰月），而公元700年的农历年（庚子年）有十五个月（其中一个月是闰月）。";
        }
    }
    
    // Tang dynasty
    if (y==761 || y==762) {
        if (lang==0) {
            info = "In December 761, emperor Suzong of the Tang dynasty designated the z&#464; month (present day month 11) as the first month of a year; the ch&#466;u month (present day month 12) became month 2; the y&#237;n month (present day month 1) became month 3 and so on. The Chinese month numbers were shifted by two. As a result, the Chinese year in 761 (X&#299;n ch&#466;u) had only 10 months. The month numbers ware switched back to the old system in April 762. The Chinese year in 762 (R&#233;n y&#237;n) had 14 months, with two month 4s and two month 5s.";
        } else if (lang==1) {
            info = "公元761年12月，唐肅宗改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月、建丑（即現在的十二月）改稱二月、建寅（即現在的正月）改稱三月等等，與現在通用的月序相差二個月。公元762年4月又把農曆月的數序改回以建寅為正月、建卯為二月等。公元761年的農曆年（辛丑年）只有十個月,而公元762年的農曆年（壬寅年）則有十四個月，其中有兩個四月和兩個五月。";
        } else {
            info = "公元761年12月，唐肃宗改正朔，以周正建子(即现在的十一月)为年首，建子改称正月、建丑（即现在的十二月）改称二月、建寅（即现在的正月）改称三月等等，与现在通用的月序相差二个月。公元762年4月又把农历月的数序改回以建寅为正月、建卯为二月等。公元761年的农历年（辛丑年）只有十个月,而公元762年的农历年（壬寅年）则有十四个月，其中有两个四月和两个五月。";
        }
    }
    
    // Gregorian calendar reform
    if (y==1582) {
        if (lang==0) {
            info = "Gregorian calendar reform: Julian calendar was used until October 4, after which the Gregorian calendar was used. To restore the March equinox to the date it had in 325 CE (March 21), the date was advanced so that October 4 was followed by October 15.";
        } else if (lang==1) {
            info = "格里高里曆改:公曆在10月4日及之前用儒略曆，之後用格里高里曆。為使春分的日期回復到3月21日(公元325年時的春分日期)，10月4日的下一日改為10月15日，跳了10日。";
        } else {
            info = "格里高里历改:公历在10月4日及之前用儒略历，之后用格里高里历。为使春分的日期回复到3月21日(公元325年时的春分日期)，10月4日的下一日改为10月15日，跳了10日。";
        }
    }
    
    // Calendar Case
    if (y > 1665.5 && y < 1670.5 && region=='default') {
        if (lang==0) {
            info = 'Following the Calendar Case (see, e.g., <a href="https://halshs.archives-ouvertes.fr/halshs-01222267/document" target="_blank">Jami 2015</a> and <a href="https://journals.sagepub.com/doi/full/10.1177/0021828620901887" target="_blank">Cullen &amp; Jami 2020</a>), the Qing government abolished the Western system of astronomy in the calendar computation in <strike>1666</strike> 1667-1669. The calendars in this period were calculated by the <i>D&#224;t&#466;ng</i> system, which was used in the Ming dynasty. The 24 solar terms were calculated based on the <i>p&#237;nq&#236;</i> rule, which took into account only the mean motion of the Sun. Two sets of calendrical solar terms are provided here for reference: the X&#299;nf&#462; solar terms are based on <i>3500 Years of Calendars and Astronomical Phenomena</i>, which are recomputed using the Western system; the <i>D&#224;t&#466;ng</i> solar terms are based on the <i>D&#224;t&#466;ng</i> system. As for the lunar conjunctions, the dates calculated using the <i>D&#224;t&#466;ng</i> astronomical system are identical to those computed using the Western system in these years.<br /><i>Update in May 2024:</i> There are imperial planetary ephemerides for 1662-1671 on the <a href="https://qingarchives.npm.edu.tw/index.php" target="_blank">Digital Library of Qing Archives</a> managed by the National Palace Museum in Taiwan. The dates and times of solar terms in the ephemeris for 1666 agree with the calculations by Western system, whereas those for 1667-1669 agree with the calculations by the <i>D&#224;t&#466;ng</i> system although there was a slight modification of the calculations in 1669. Readers who are interested in this issue can read <a href="http://ytliu.epizy.com/Shixian/N1667_1669.html" target="_blank">my article</a> on my analyses of the moon phases and solar terms in this period';
        } else if (lang==1) {
            info = '<strike>康熙五年</strike> 康熙六年至八年清政府因<a href="https://zh.wikipedia.org/zh-hant/%E5%BA%B7%E7%86%99%E5%8E%86%E7%8B%B1" target="_blank">曆獄</a>廢除西洋新法，復用明朝《大統曆》，二十四節氣改回平氣。這裡提供兩套曆書節氣:「新法節氣」根據《三千五百年历日天象》，此乃以後的欽天監依西洋新法追推的定氣;「大統曆節氣」根據明朝《大統曆》推算。至於朔日，依明朝《大統曆》和依《西洋新法曆書》計算結果在這幾年的日期完全一致。<br /><i>2024年5月更新:</i> 臺灣國立故宮博物院的<a href="https://qingarchives.npm.edu.tw/index.php" target="_blank">清代檔案檢索系統</a>藏有若干康熙初年的《大清七政經緯躔度時憲曆》，其中康熙五年所載的節氣日期和時刻符合《西洋新法曆書》的推步，康熙六年至八年則符合大統曆的推步，雖然康熙八年的計算有少許修改。對這幾年清朝曆書所載之月相和節氣時刻有興趣者，可參閱拙文<a href="http://ytliu.epizy.com/Shixian/N1667_1669_chinese.html" target="_blank">康熙六年至八年(1667-1669)的月相和節氣時刻</a>。';
        } else {
            info = '<strike>康熙五年</strike> 康熙六年至八年清政府因<a href="https://zh.wikipedia.org/zh-cn/%E5%BA%B7%E7%86%99%E5%8E%86%E7%8B%B1" target="_blank">历狱</a>废除西洋新法，复用明朝《大统历》，二十四节气改回平气。这里提供两套历书节气:「新法节气」根据《三千五百年历日天象》，此乃以后的钦天监依西洋新法追推的定气;「大统历节气」根据明朝《大统历》推算。至于朔日，依明朝《大统历》和依《西洋新法历书》计算结果在这几年的日期完全一致。<br /><i>2024年5月更新:</i> 台湾国立故宫博物院的<a href="https://qingarchives.npm.edu.tw/index.php" target="_blank">清代档案检索系统</a>藏有若干康熙初年的《大清七政经纬躔度时宪历》，其中康熙五年所载的节气日期和时刻符合《西洋新法历书》的推步，康熙六年至八年则符合大统历的推步，虽然康熙八年的计算有少许修改。对这几年清朝历书所载之月相和节气时刻有兴趣者，可参阅拙文<a href="http://ytliu.epizy.com/Shixian/N1667_1669_simp.html" target="_blank">康熙六年至八年(1667-1669)的月相和节气时刻</a>。';
        }
    }
    
    return info;
}

// Print the table for one Gregorian/Julian month
function printMonth(m,lang, year, cyear, firstMonth, langVars, calVars) {
    let cmon = addChineseMonths(m, lang, year, cyear, langVars, calVars);
    let nMonth=cmon.nMonth, cmyear=cmon.cmyear, cmonth=cmon.cmonth;
    let yearc = year.toString();
    if (year < 1) {
        yearc = (lang==0 ? (1-year).toString()+' BCE':'前'+(1-year).toString());
    }
    if (lang != 0) yearc += '年';
    
    let txt='<table>';
    let i;
    if (nMonth==1) {
        txt += '<tr><th colspan="2"><h2>'+yearc+'<br />'+langVars.gMonth[m]+'</h2></th>'+'<th colspan="5"><h3>'+cmyear[0]+' '+cmonth[0]+'</h3></th></tr>';
    } else {
        txt += '<tr><th colspan="2" rowspan="'+nMonth+'"><h2>'+yearc+'<br />'+langVars.gMonth[m]+'</h2></th>'+'<th colspan="5"><h3>'+cmyear[0]+' '+cmonth[0]+'</h3></th></tr>';
        for (i=1; i<nMonth; i++) {
            txt += '<tr><th colspan="5"><h3>'+cmyear[i]+' '+cmonth[i]+'</h3></th></tr>';
        }
    }

    // Week row
    txt += '<tr>';
    for (i=0; i<7; i++) {
        txt += '<th style="font-size:120%;">'+langVars.weeks[i]+'</th>';
    }
    txt += '</tr>';

    // Determine the day of week of the first date of month
    let week1 = (calVars.jd0 + calVars.mday[m] + 3) % 7;
    
    if (week1 > 0) {
        txt += '<tr>';
        txt += '<td colspan="'+week1+'"></td>';
    }
    // # of days in the months
    let n = calVars.mday[m+1] - calVars.mday[m];
    let week;
    for (i=1; i<=n; i++) {
        week = (week1 + i - 1) % 7;
        if (week==0) txt += '<tr>';
        if (n>25) {
            txt += '<td><h3 style="text-align:center;">'+i+'</h3>';
        } else {
            // Gregorian calendar reform: in 1582 Oct has only 21 days.
            // The day following Oct 4 is Oct 15
            if (i < 5) {
                txt += '<td><h3 style="text-align:center;">'+i+'</h3>';
            } else {
                txt += '<td><h3 style="text-align:center;">'+(i+10)+'</h3>';
            }
        }
        
        txt += addChineseDate(year,m,i, lang, langVars, calVars, firstMonth);
        txt += addSexagenaryDays(m, i, langVars, calVars);
        txt += '</td>'
        if (week==6) txt += '</tr>';
    }
    if (week != 6) {
        txt += '<td colspan="'+(6-week)+'"></td></tr>';
    }
    
    txt += '</table>';
    
    txt += addMoonPhases(m, lang, langVars, calVars);
    txt += add24solterms(m, lang, langVars, calVars);
    if (year < 1734) {
        //add calendrical solar terms
        txt += addCalSolterms(m, lang, langVars, calVars, 0);
        // add Datong solar terms in 1666-1670
        if (year > 1665.5 && year < 1670.5 && langVars.region=='default') {
            txt += addCalSolterms(m, lang, langVars, calVars, 1);
        }
    }
    let warn = warningMessage(year, m+1, lang, langVars);
    if (warn != '') {
        txt += '<p style="color:red;"><sup>*</sup>'+warn+'</p>';
    }
    txt += '<br /><br /><br />';
    
    return txt;
}

// Calculate the number of Chinese months spanned by 
// this Gregorian/Julian month m in year y. This is equal to 1 + number 
// of first dates of Chinese months occurring on and 
// after the second day of this month and before the 
// first date of the next month.
// Also calculate the sexagenary month cycle for years > -480.
function addChineseMonths(m, lang, y, cyear, langVars, 
                           calVars) {
    let i;
    let txt = ['leap ', '閏', '闰'];
    let leap = txt[lang];
    if (y==-104) {
        txt = ['post ', '後', '后'];
        leap = txt[lang];
    }
    if (y < -104) {
        leap = calVars.leap;
        if (lang==1) {
            leap = (calVars.leap=="post 9" ? "後九":"閏");
        }
        if (lang==2) {
            leap = (calVars.leap=="post 9" ? "后九":"闰");
        }
    }
    let m0 = calVars.mday[m];
    let m1 = calVars.mday[m+1];
    
    // Sexagenary year cycle for year y-1
    //let adj = (y > 10 ? 0:60*Math.floor(-y/60 + 2));
    let ihy1 = (y + 725) % 10;
    if (ihy1 < 0) { ihy1 += 10;}
    
    let nMonth = 1, j, tmp, cm, jian;
    let cmonth = [], cmyear = [];
    // Determine the Chinese month on the first day of 
    // this Gregorian/Julian month
    let n = calVars.cmonthDate.length;
    for (i=0; i<n; i++) {
        if (calVars.cmonthDate[i] <= m0+1 && calVars.cmonthDate[i+1] > m0+1) {
            cm = calVars.cmonthNum[i];
            jian = calVars.cmonthJian[i];
            // sexagenary month cycle
            let cmsex = '';
            if (cm > 0 && y > -104) {
                if (lang != 0) { cmsex = '建';}
                let mm = 12*(ihy1 + calVars.cmonthXiaYear[i]) + jian;
                mm = (mm+1) % 10;
                cmsex += langVars.heaven[mm];
                if (lang==0) cmsex += ' ';
                cmsex += langVars.earth[(jian+1) % 12];
                if (lang==0) {
                    cmsex = ', '+cmsex;
                } else {
                    cmsex = ' ('+cmsex+')';
                }
            }
            if (y <= -104) {
                if ('noZhong' in calVars) {
                    if (calVars.noZhong==i) {
                        if (lang==0) {
                            cmsex = ', no Zh&#333;ngq&#236;';
                        } else if (lang==1) {
                            cmsex = ' (無中氣)';
                        } else {
                            cmsex = ' (无中气)';
                        }
                    }
                }
            }
            if (lang==0) {
                tmp = 'month: ';
                if (cm > 0) {
                    tmp += cm;
                } else {
                    tmp += (y >= -104 ? leap+(-cm):leap);
                }
                tmp += ' ('+langVars.monthL[calVars.cmonthLong[i]]+cmsex+')';
            } else {
                if (cm > 0) {
                    tmp = langVars.cmonth[cm-1];
                } else {
                    tmp = (y >= -104 ? leap+langVars.cmonth[-cm-1]:leap);
                }
                
                if (y>688 && y <700 && Math.abs(cm)==11) {
                    // 11 yue -> zheng yue
                    tmp = '正';
                }
                if (y > 689 && y < 701 && Math.abs(cm)==1) {
                    // zheng yue -> yi yue
                    tmp = '一';
                }
                tmp += "月" + langVars.monthL[calVars.cmonthLong[i]]+cmsex;
            }
            cmonth.push(tmp);
            tmp = cyear[calVars.cmonthYear[i]];
            if (lang==0) tmp = 'year: '+tmp+', ';
            cmyear.push(tmp);
            j = i+1;
            break;
        }
    }
    for (i=j; i<n; i++) {
       let d1 = calVars.cmonthDate[i];
       if (d1 > m0+1 && d1 <= m1) {
           nMonth++;
           cm = calVars.cmonthNum[i];
           jian = calVars.cmonthJian[i];
           // sexagenary month cycle
            let cmsex = '';
            if (cm > 0 && y > -104) {
                if (lang != 0) { cmsex = '建';}
                let mm = 12*(ihy1 + calVars.cmonthXiaYear[i]) + jian;
                mm = (mm+1) % 10;
                cmsex += langVars.heaven[mm];
                if (lang==0) cmsex += ' ';
                cmsex += langVars.earth[(jian+1) % 12];
                if (lang==0) {
                    cmsex = ', '+cmsex;
                } else {
                    cmsex = ' ('+cmsex+')';
                }
            }
           if (y <= -104) {
                if ('noZhong' in calVars) {
                    if (calVars.noZhong==i) {
                        if (lang==0) {
                            cmsex = ', no Zh&#333;ngq&#236;';
                        } else if (lang==1) {
                            cmsex = ' (無中氣)';
                        } else {
                            cmsex = ' (无中气)';
                        }
                    }
                }
            }
            if (lang==0) {
                tmp = 'month: ';
                if (cm > 0) {
                    tmp += cm;
                } else {
                    tmp += (y >= -104 ? leap+(-cm):leap);
                }
                tmp += ' ('+langVars.monthL[calVars.cmonthLong[i]]+cmsex+')';
            } else {
                if (cm > 0) {
                    tmp = langVars.cmonth[cm-1];
                } else {
                    tmp = (y >= -104 ? leap+langVars.cmonth[-cm-1]:leap);
                }
                if (y>688 && y <700 && Math.abs(cm)==11) {
                    // 11 yue -> zheng yue
                    tmp = '正';
                }
                if (y > 689 && y < 701 && Math.abs(cm)==1) {
                    // zheng yue -> yi yue
                    tmp = '一';
                }
                tmp += "月" + langVars.monthL[calVars.cmonthLong[i]]+cmsex;
            }
            cmonth.push(tmp);
            tmp = cyear[calVars.cmonthYear[i]];
            if (lang==0) tmp = 'year: '+tmp+', ';
            cmyear.push(tmp);
       }
    }
    return {nMonth:nMonth, cmonth:cmonth, cmyear:cmyear};
}

function addChineseDate(y, m, d, lang, langVars, calVars, firstMonth) {
    // # of days from Dec 31 in the previous year
    let dd = calVars.mday[m] + d; 
    
    // Determine the month and date in Chinese calendar
    let i, cd, longM, cmIsFirstMonth, cm=0, n=calVars.cmonthDate.length;
    for (i=0; i<n-1; i++) {
        if (dd >= calVars.cmonthDate[i] && dd < calVars.cmonthDate[i+1]) {
            cm = calVars.cmonthNum[i];
            cd = dd - calVars.cmonthDate[i] + 1;
            longM = calVars.cmonthLong[i];
            cmIsFirstMonth = (cm == firstMonth[calVars.cmonthYear[i]]);
            if (y==-103 || y==700) {cmIsFirstMonth = false;}
        }
    }
    
    if (cm==0) { 
        cm = calVars.cmonthNum[n-1];
        cd = dd - calVars.cmonthDate[n-1] + 1;
        longM = calVars.cmonthLong[n-1];
        cmIsFirstMonth = (cm == firstMonth[calVars.cmonthYear[n-1]]);
        if (y==-103 || y==700) {cmIsFirstMonth = false;}
    }
    
    let txt, m1, warn;
    
    if (lang==0) {
        // English
        m1 = "0"+Math.abs(cm);
        m1 = m1.slice(-2);
        if (cm < 0) {
            if (y < -104) {
                m1 = calVars.leap;
            } else if (y==-104) {
                m1 = 'post 9';
            } else {
                m1 = 'leap '+m1;
            }
        }
        let d1 = "0"+cd;
        d1 = d1.slice(-2);
        if (cmIsFirstMonth && cd==1) {
            txt = '<p style="color:red;"><b>'+m1+'-'+d1;
            warn = newMoonCloseToMidnight(y,cm);
            if (warn==1) txt += '<sup>*</sup>';
            txt += '</b></p>';
        } else if (cd==1) {
            txt ='<p style="color:brown;"><b>'+m1+'-'+d1;
            warn = newMoonCloseToMidnight(y,cm);
            if (warn==1) txt += '<sup>*</sup>';
            txt += '</b></p>';
        } else {
            txt = '<p>'+m1+'-'+d1+'</p>';
        }
    } else {
      // Chinese
       if (cm > 0) {
           m1 = langVars.cmonth[cm-1]+"月";
       } else {
           if (y < -104) {
               if (lang==1) {
                   m1 = (calVars.leap=="post 9" ? "後九":"閏") + "月";
               } else {
                   m1 = (calVars.leap=="post 9" ? "后九":"闰") + "月";
               }
           } else {
               if (lang==1) {
                   m1 = (y==-104 ? '後':'閏') + langVars.cmonth[-cm-1] + "月";
               } else {
                   m1 = (y==-104 ? '后':'闰') + langVars.cmonth[-cm-1] + "月";
               }
           }
       }
       if (y>688 && y <700 && Math.abs(cm)==11) {
            // 11 yue -> zheng yue
            m1 = '正月';
        }
        if (y > 689 && y < 701 && Math.abs(cm)==1) {
            // zheng yue -> yi yue
            m1 = '一月';
        }
       if (cmIsFirstMonth && cd==1) {
           txt = '<p style="color:red;"><b>'+m1;
           warn = newMoonCloseToMidnight(y,cm);
           if (warn==1) txt += '<sup>*</sup>';
           txt += '</b></p>';
       } else if (cd==1) {
           txt = '<p style="color:brown;"><b>'+m1;
           warn = newMoonCloseToMidnight(y,cm);
           if (warn==1) txt += '<sup>*</sup>';
           txt += '</b></p>';
       } else if (dd==1) {
           txt = '<p>'+m1+langVars.date_numChi[cd-1]+'</p>';
       } else {
           txt = '<p>'+langVars.date_numChi[cd-1]+'</p>';
       }
    }
    
    return txt;
}

function addSexagenaryDays(m,d,langVars, calVars) {
    // # of days from Dec 31 in the previous year
    let dd = calVars.mday[m] + d; 
    let jd = calVars.jd0 + dd + 1;
    
    let h = langVars.heaven[(jd-1) % 10];
    let e = langVars.earth[(jd+1) % 12];
    let txt;
    if (langVars.lang==0) {
        txt ='<p>'+h+' '+e+'</p>';
    } else {
       txt ='<p>'+h+e+'</p>'; 
    }
    if (langVars.julian) {
        txt += '<p style="font-size:99%;letter-spacing:normal;">'+jd+'</p>';
    }
    return txt;
}

function addMoonPhases(m,lang,langVars, calVars) {
    let m0 = calVars.mday[m];
    let m1 = calVars.mday[m+1];
    let i, dd, h;
    let txt; 
    if (lang==0) {
        txt = '<p><b>Moon Phases</b>: '
    } else {
        txt = '<p style="letter-spacing:normal;"><b>月相</b>: '
    }
    
    let phases = [];
    // new moon
    let name = '['+langVars.Qnames[0]+'] ';
    let n = calVars.Q0.length;
    for (i=0; i<n; i++) {
        dd = Math.floor(calVars.Q0[i]);
        if (dd > m0 && dd <= m1) {
            let ec = '-';
            calVars.sol_eclipse.forEach(function(e) {
                if (Math.abs(dd - e[0]) < 5) {
                    let ybeg = 1 + 100*Math.floor(0.01*(calVars.year - 0.5));
                    if (calVars.year==ybeg && e[1] > 200) {
                        ybeg -= 100;
                    } else if (calVars.year-ybeg==99 && e[1] < 200){
                        ybeg += 100;
                    }
                    let type;
                    let linkg = 'http://ytliu.epizy.com/eclipse/';
                    if (lang==0) {
                        type = ['Partial solar eclipse', 'Annular solar eclipse', 'Total solar eclipse', 'Hybrid solar eclipse'];
                    } else if (lang==1) {
                        type = ['日偏食', '日環食', '日全食', '日全環食'];
                    } else {
                        type = ['日偏食', '日环食', '日全食', '日全环食'];
                    }
                    linkg += 'one_solar_eclipse_general.html?ybeg='+ybeg+'&ind='+e[1]+'&ep=DE431';
                    ec = '<a href="'+linkg+'" target="_blank">'+type[e[2]]+'</a>';
                }
            });
            phases.push({phase:name, time:calVars.Q0[i]-m0, ec:ec});
        }
    }
    // first quarter 
    name = '['+langVars.Qnames[1]+'] ';
    n = calVars.Q1.length;
    for (i=0; i<n; i++) {
        dd = Math.floor(calVars.Q1[i]);
        if (dd > m0 && dd <= m1) {
            phases.push({phase:name, time:calVars.Q1[i]-m0, ec:'-'});
        }
    }
    // full moon
    name = '['+langVars.Qnames[2]+'] ';
    n = calVars.Q2.length;
    for (i=0; i<n; i++) {
        dd = Math.floor(calVars.Q2[i]);
        if (dd > m0 && dd <= m1) {
            let ec = '-';
            calVars.lun_eclipse.forEach(function(e) {
                if (Math.abs(dd - e[0]) < 5) {
                    let ybeg = 1 + 100*Math.floor(0.01*(calVars.year - 0.5));
                    let type;
                    let linkg = 'http://ytliu.epizy.com/eclipse/';
                    if (lang==0) {
                        type = ['Penumbral lunar eclipse', 'Partial lunar eclipse', 'Total lunar eclipse'];
                    } else {
                        type = ['半影月食', '月偏食', '月全食'];
                    }
                    linkg += 'one_lunar_eclipse_general.html?ybeg='+ybeg+'&shrule=Danjon&ind='+e[1]+'&ep=DE431';
                    ec = '<a href="'+linkg+'" target="_blank">'+type[e[2]]+'</a>';
                }
            });
            phases.push({phase:name, time:calVars.Q2[i]-m0, ec:ec});
        }
    }
    // third quarter
    name = '['+langVars.Qnames[3]+'] ';
    n = calVars.Q3.length;
    for (i=0; i<n; i++) {
        dd = Math.floor(calVars.Q3[i]);
        if (dd > m0 && dd <= m1) {
            phases.push({phase:name, time:calVars.Q3[i]-m0, ec:'-'});
        }
    }
    
    // sort events in chronological order
    phases.sort((a,b) => a.time - b.time);
    
    // Correct for Gregorian calendar reform
    // Oct 1582 has only 21 days; The day after Oct 4 was Oct 15
    n = phases.length;
    if (m1-m0 < 25) {
        for (i=0; i<n; i++) {
            phases[i].time += (phases[i].time >= 5.0 ? 10.0:0.0);
        }
    }
    
    for (i=0; i<n; i++) {
        let h = 24.0*(phases[i].time - Math.floor(phases[i].time));
        txt += phases[i].phase + ' ' + Math.floor(phases[i].time) 
               + '<sup>d</sup>' + convertHM(h);
        if (phases[i].ec != '-') {
            txt += ' ('+phases[i].ec+')';
        }
        if (i < n-1) txt += '&nbsp;&nbsp;';
    }
    
    txt += '</p>';
    
    return txt;
}

function add24solterms(m,lang,langVars, calVars) {
    let m0 = calVars.mday[m];
    let m1 = calVars.mday[m+1];
    let txt; 
    if (lang==0) {
        txt = '<p><b>24 solar terms ';
        if (calVars.year < 1734) {
            txt += '(d&#236;ngq&#236;)';
        }
        txt +='</b>: ';
    } else if (lang==1) {
        txt = '<p style="letter-spacing:normal;"><b>二十四節氣';
        if (calVars.year < 1734) {
            txt += '(定氣)';
        }
        txt +='</b>: ';
    } else {
        txt = '<p style="letter-spacing:normal;"><b>二十四节气';
        if (calVars.year < 1734) {
            txt += '(定气)';
        }
        txt +='</b>: ';
    }
    
    let empty = 1;
    for (let i=0; i<calVars.solar.length; i++) {
        let dd = Math.floor(calVars.solar[i]);
        if (dd > m0 && dd <= m1) {
            if (empty==0) txt += '&nbsp;&nbsp;&nbsp;';
            txt += '['+langVars.soltermNames[i]+'] ';
            let h = 24.0*(calVars.solar[i] - dd);
            let d = dd - m0;
            // Correct for Gregorian calendar reform
            // Oct 1582 has only 21 days; The day after Oct 4 was Oct 15
            if (m1-m0 < 25) {
               d += (d > 4 ? 10:0);
            }
            txt += d+'<sup>d</sup>';
            txt += convertHM(h);
            empty = 0;
        }
    }
    txt += '</p>';
    
    return txt;
}

// Add calendrical solar terms
function addCalSolterms(m,lang,langVars, calVars, datong) {
    let solar;
    if (calVars.year >= -104) {
        if ('pingqi' in calVars) {
            solar = calVars.pingqi;
        } else {
            if (datong==0) {
                let calSolTerms = calendricalSolarTerms();
                let ind = calVars.year - calendricalSolarTerms_ystart();
                solar = calSolTerms[ind];
                // decompress
                let n = solar.length;
                for (let i=1; i<n; i++) { 
                    solar[i] += solar[i-1]+14;
                }
                // solar contains all the 24 solar terms in year y, starting from 
                // J12 (Xiaohan) to Z11 (winter solstice). It stores the dates 
                // of the solar terms counting from Dec. 31, y-1 at 0h (UTC+8).
                // Add one more to solar if J12 occurs before Jan 3.
                if (solar[0] < 3) {
                    solar.push(calSolTerms[ind+1][0] + NdaysGregJul(calVars.year));
                }
                calSolTerms = null;
            } else {
                solar = datongSolarTerms(calVars.year);
            }
        }
    } else {
        if ('pingqi' in calVars) {
            solar = calVars.pingqi;
        } else {
            return '';
        }
    }
    
    let m0 = calVars.mday[m];
    let m1 = calVars.mday[m+1];
    let txt = ''; 
    let split = false;
    if (calVars.year==1666 && m > 0.5 && langVars.region=='default') { split=true;}
    if (calVars.year > 1666 && calVars.year < 1670 && langVars.region=='default') { split=true;}
    if (calVars.year==1670 && m < 1.5  && langVars.region=='default') { split=true;}
    if (datong==0) {
        if (lang==0) {
            txt = '<p><b>Calendrical solar terms ';
            if (calVars.year < 1645 || (calVars.year==1645 && m==0) || langVars.region=='SouthernMing') {
                txt += '(p&#236;ngq&#236;)</b>: ';
            } else {
                txt += '(d&#236;ngq&#236;)</b>: ';
            }

            if (split) {
                txt = '<p><b>X&#299;nf&#462; solar terms (d&#236;ngq&#236;)</b>: ';
            }
        } else if (lang==1) {
            txt = '<p style="letter-spacing:normal;"><b>曆書節氣';
            if (calVars.year < 1645 || (calVars.year==1645 && m==0) || langVars.region=='SouthernMing') {
                txt += '(平氣)</b>: ';
            } else {
                txt += '(定氣)</b>: ';
            }

            if (split) {
                txt = '<p style="letter-spacing:normal;"><b>新法節氣(定氣)</b>: ';
            }
        } else {
            txt = '<p style="letter-spacing:normal;"><b>历书节气';
            if (calVars.year < 1645 || (calVars.year==1645 && m==0) || langVars.region=='SouthernMing') {
                txt += '(平气)</b>: ';
            } else {
                txt += '(定气)</b>: ';
            }

            if (split) {
                txt = '<p style="letter-spacing:normal;"><b>新法节气(定气)</b>: ';
            }
        }
    } else {
        if (split) {
            if (lang==0) {
                txt = '<p><b>D&#224;t&#466;ng solar terms (p&#236;ngq&#236;)</b>: ';
            } else if (lang==1) {
                txt = '<p style="letter-spacing:normal;"><b>大統曆節氣(平氣)</b>: ';
            } else {
                txt = '<p style="letter-spacing:normal;"><b>大统历节气(平气)</b>: ';
            }
        }
    }
    
    if (txt != '') {
        let empty = 1;
        for (let i=0; i<solar.length; i++) {
            let dd = solar[i];
            if (dd > m0 && dd <= m1) {
                if (empty==0) txt += '&nbsp;&nbsp;&nbsp;';
                txt += '['+langVars.soltermNames[i]+'] ';
                let d = dd - m0;
                // Correct for Gregorian calendar reform
                // Oct 1582 has only 21 days; The day after Oct 4 was Oct 15
                if (m1-m0 < 25) {
                   d += (d > 4 ? 10:0);
                }
                txt += d+'<sup>d</sup>';
                empty = 0;
            }
        }
        txt += '</p>';
    }
    
    return txt;
}

// Set up the solar terms according to the Datong system in year y
// This is for 1666-1669 when the Qing calendar was temporarily 
// switched to the Datong system.
function datongSolarTerms(y) {
    let ps = 365.2425; // solar cycle in the Datong system
    let JDw = 1721049.9175 + 1e-8; // Z11 epoch JD
    let jd0 = getJD(y-1,12,31); // JD on Dec 31, y-1 at noon
    let j = Math.floor((jd0 - JDw)/ps);
    let dqi = ps/24.0;
    let J12 = JDw + j*ps - jd0 + dqi; // JD of J12 in year y
    let qi = [];
    for (let i=0; i<25; i++) {
        qi.push(Math.floor(J12 + i*dqi));
    }
    return qi;
}

// hours -> hh:mm
function convertHM(h) {
    let h1 = h + 0.5/60.0;
    let hh = Math.floor(h1);
    let mm = Math.floor(60.0*(h1-hh));
    hh = '0'+hh; mm = '0'+mm;
    return hh.slice(-2)+'<sup>h</sup>'+mm.slice(-2)+'<sup>m</sup>';
}

// day from Dec 31, y-1 -> m, d (assume day > 0)
function ymd(day, leap) {
    let ndays = 365+leap;
    let m,d;
    if (day > ndays) {
        m = 13; d = day-ndays;
    } else {
        let mday = [0, 31, 59+leap, 90+leap, 120+leap, 151+leap, 181+leap, 212+leap,
               243+leap, 273+leap, 304+leap, 334+leap, ndays];
        if (day < 1) {
            m=1; d=day;
        } else {
            for (let i=0; i<13; i++) {
                if (day-mday[i] < 1) {
                    m=i; d = day-mday[i-1];
                    break;
                }
            }
        }
    }
    
    let mm = "0"+m, dd = "0"+d;
    return mm.slice(-2)+'-'+dd.slice(-2);
}

// Determine if the new moon associated with month j in year y 
// is too close to midnight
function newMoonCloseToMidnight(y, j) {
    let warn = 0;
    if (y==2057) {
        warn = (j==9 ? 1:0);
    }
    if (y==2089) {
        warn = (j==8 ? 1:0);
    }
    if (y==2097) {
        warn = (j==7 ? 1:0);
    }
    if (y==2115) {
        warn = (j==2 ? 1:0);
    }
    if (y==2116) {
        warn = (j==4 ? 1:0);
    }
    if (y==2133) {
        warn = (j==9 ? 1:0);
    }
    if (y==2165) {
        warn = (j==11 ? 1:0);
    }
    if (y==2172) {
        warn = (j==9 ? 1:0);
    }
    
    return warn;
}

// Calendar notes at the bottom of Gregorian month m in year y.
function warningMessage(y, m, lang, langVars) {
    let warn = '';

    if (y < 618) {
        return calendarNotesBefore618(y, m, lang, langVars);
    }

    // Tang dynasty
    if (y > 617.5 && y < 908) {
        return calendarNotesTang(y, m, lang);
    }

    // Ming dynasty
    if (y > 1367.5 && y < 1644.5) {
        return calendarNotesMing(y, m, lang);
    }

    // Qing dynasty
    if (y > 1644.5 && y < 1911.5 && langVars.region=='default') {
        return calendarNotesQing(y, m, lang);
    }

    // Southern Ming and Zheng dynasty
    if (langVars.region=='SouthernMing') {
        return SouthernMingCalendarDateNotes(y, m, lang);
    }
    
    // 1912-1979
    if (y > 1911.5 && y < 1980) {
        return calendarNotes1912_1979(y, m, lang);
    }

    // After 2050
    if (y > 2050) {
        return calendarNotesAfter2050(y, m, lang, langVars);
    }
 
    return warn;
}

function calendarNotesBefore618(y, m, lang, langVars) {
    let warn = '';
    // Han calendar reform
    if (y==-103 && m==6) {
        if (lang==0) {
            warn = "New calendar is displayed starting from month 5. The lunar conjunction day was one day earlier than that of the old calendar, turning month 4 into a short month.";
        } else if (lang==1) {
            warn = "五月起的日曆依太初曆，朔日比舊曆早一日，使四月變成小月。";
        } else {
            warn = "五月起的日历依太初历，朔日比旧历早一日，使四月变成小月。";
        }
    } 
    
    // Xin dynasty
    if (y==9 && m==1) {
        if (lang==0) {
            warn = "The ch&#466;u month was supposed to be month 12. It became month 1 by edict. Hence, there was no month 12 in the Chinese year W&#249; ch&#233;n.";
        } else if (lang==1) {
            warn = "本來十二月是建丑，改正朔後建丑變成正月，所以戊辰年沒有十二月。";
        } else {
            warn = "本来十二月是建丑，改正朔后建丑变成正月，所以戊辰年没有十二月。";
        }
    }
    if (y==23 && m > 1) {
        let month_numChi = ["正","二","三","四","五","六","七","八","九","十", "十一","十二"];
        let cdates_eng = ['February 10th', 'March 11th', 'April 10th', 'May 9th', 'June 8th', 'July 7th', 'August 6th', 'September 4th', 'October 4th', 'November 2nd', 'December 2nd'];
        let cdates_chi = ['2月10日', '3月11日', '4月10日', '5月9日', '6月8日', '7月7日', '8月6日', '9月4日', '10月4日', '11月2日', '12月2日'];
        let msg = [cdates_eng[m-2]+' was the first day of month '+m+' in the Xin calendar and the first day of month '+(m-1)+' in the Gengshi calendar.', cdates_chi[m-2]+'是地皇四年'+month_numChi[m-1]+'月初一、更始元年'+month_numChi[m-2]+'月初一。', cdates_chi[m-2]+'是地皇四年'+month_numChi[m-1]+'月初一、更始元年'+month_numChi[m-2]+'月初一。'];
        if (m==12) {
            msg[0] += ' December 31st was the first day of month 12 in the Gengshi calendar.';
            msg[1] += '12月31日是更始元年十二月初一。';
            msg[2] += '12月31日是更始元年十二月初一。';
        }
        warn = msg[lang];
    }
    // if (y==23 && m==12) {
    //     if (lang==0) {
    //         warn = "Since month 1 was to switch back to be the y&#237;n month in the following year, there were two month 12s in this Chinese year. The first one was the z&#464; month and the second one was the ch&#466;u month. These two month 12s should not be confused as they can be distinguished by their sexagenary month cycles.";
    //     } else if (lang==1) {
    //         warn = "下一年的正月恢復為建寅，這一年的農曆有兩個十二月:建子和建丑。由於已註明了月干支，兩個十二月應不會被混淆。";
    //     } else {
    //         warn = "下一年的正月恢复为建寅，这一年的农历有两个十二月:建子和建丑。由于已注明了月干支，两个十二月应不会被混淆。";
    //     }
    // }
    
    // Wei dynasty
    if (y==237 && m==2 && langVars.region=='default') {
        if (lang==0) {
            warn = "Note that month 12 had only 28 days. This was due to the adoption of a new version of calendar in month 1. There are discrepancies between the data in the main text and Appendix 2 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The main text uses the new calendar in month 1, but Appendix 2 uses the new calendar in month 6. Here the data in the main text are used, in which the first days of each month before month 6 are one day earlier.";
        } else if (lang==1) {
            warn = "由於新曆法(景初曆)於正月初一開始使用，十二月只有二十八日。《三千五百年历日天象》的正文與其附表2的資料不合，正文在正月改用景初曆，附表2在六月才改曆。這裡用正文的數據，在六月前的朔日都比附表2早一日。";
        } else {
            warn = "由于新历法(景初历)于正月初一开始使用，十二月只有二十八日。。《三千五百年历日天象》的正文与其附表2的资料不合，正文在正月改用景初历，附表2在六月才改历。这里用正文的数据，在六月前的朔日都比附表2早一日。";
        }
    }
    if (y==237 && m==4 && langVars.region=='default') {
        if (lang==0) {
            warn = "The ch&#233;n month was supposed to be month 3. It became month 4 by edict. Hence, there was no month 3 in this Chinese year."; 
        } else if (lang==1) {
            warn = "本來三月是建辰，改正朔後變成四月，所以丁巳年沒有三月。"; 
        } else {
            warn = "本来三月是建辰，改正朔后变成四月，所以丁巳年没有三月。"; 
        }
    }
    if (y==240 && m==1 && langVars.region=='default') {
        if (lang==0) {
            warn = "Since month 1 was to switch back to be the y&#237;n month in the year G&#275;ng sh&#275;n, there were two month 12s in the year J&#464; w&#232;i. The first one was the z&#464; month and the second one was the ch&#466;u month. These two month 12s should not be confused as they can be distinguished by their sexagenary month cycles.";
        } else if (lang==1) {
            warn = "庚申年的正月恢復為建寅，己未年的農曆有兩個十二月:建子和建丑。由於已註明了月干支，兩個十二月應不會被混淆。";
        } else {
            warn = "庚申年的正月恢复为建寅，己未年的农历有两个十二月:建子和建丑。由于已注明了月干支，两个十二月应不会被混淆。";
        }
    }
    
    if (y==238 && m==11 && langVars.region=='Wu') {
        if (lang==0) {
            warn ='In Appendix 2 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i>, the sexagenary day of the leap month conjunction is listed as j&#464; ch&#466;u, corresponding to Nov. 25. This is at odds with my calculation. The result of my calculation is consistent with the data on the <a href="http://sinocal.sinica.edu.tw/" target="_blank">Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The preface of the book says that the calendar data in its appendices are based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by W&#257;ng Yu&#275;zh&#275;n (汪曰楨). I looked at the book and found that the date listed there was also the same as my calculation. I suspect that the date listed in <i>3500 Years of Calendars and Astronomical Phenomena</i> is wrong. The book also lists the sexagenary day of the month 11 conjunction as j&#464; ch&#466;u, which is certainly wrong since this date was far away from the new moon close to the beginning of month 11.'; 
        } else if (lang==1) {
            warn ='《三千五百年历日天象》附表2記閏十月己丑朔和十一月己丑朔。十一月己丑朔無疑是錯的，這裡列出的閏十月戊子朔是根據我的推步，結果與台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>一致，《三千五百年历日天象》前言說其附表參照清汪曰楨的《歷代長術輯要》，翻查此書發現亦記閏十月戊子。';
        } else {
            warn = '《三千五百年历日天象》附表2记闰十月己丑朔和十一月己丑朔。十一月己丑朔无疑是错的，这里列出的闰十月戊子朔是根据我的推步，结果与台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>一致，《三千五百年历日天象》前言说其附表参照清汪曰桢的《历代长术辑要》，翻查此书发现亦记闰十月戊子。';
        }
    }
    
    if (y==447 && m==12 && langVars.region=='WeiZhouSui') {
        if (lang==0) {
            warn = "According to <i>Index to Comprehensive Mirror to Aid in Governmance</i>, the month 11 conjunction occurred on a ji&#462; x&#363; day (Dec. 23). However, in <i>Compilation of Historical Calendars</i> by W&#257;ng Yu&#275;zh&#275;n, the month 12 conjunction was listed on a ji&#462; x&#363; day and is at odds with its statement that the winter solstice occurred on a ji&#462; x&#363; day in month 11. The month 12 conjunction on a ji&#462; x&#363; day is certainly a typo because a ji&#462; x&#363; day was 29 days (or 89 days) after a y&#464; s&#236; day, which was the leap month 10 conjunction date. So ji&#462; x&#363; day could only be the month 11 conjunction date. In <i>3500 Years of Calendars and Astronomical Phenomena</i> by Zh&#257;ng P&#233;iy&#250; and <i>Tables of Historical Lunar Conjunctions and Leap Months</i> by Ch&#233;n Yu&#225;n, the month 11 conjunction is mistakenly listed on Dec. 24. They were probably misled by W&#257;ng's typo. The book <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i> by Hsueh Chung-San and Ouyang Yi correctly places the month 11 conjunction on Dec. 23. Surprisingly, the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan, whose ancient calendar data are based on <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i>, does not follow the book and mistakenly places the month 11 conjunction on Dec. 24.";
        } else if (lang==1) {
            warn = '《通鑑目錄》記十一月甲戌朔，汪曰楨《歷代長術輯要》卻記「十乙亥、十二甲戌朔、閏十(十甲辰小雪、十一甲戌冬至)」，沒有記閏十月朔和十一月朔干支就是說兩朔日的天干和都是乙，但是「十二甲戌」是錯的，因為閏十朔是乙巳，而甲戌在乙巳後29日(或89日)，絕不可能是十二月朔，而且與其「十一甲戌冬至」相悖，可見「十二甲戌朔」應是「十一甲戌朔」之誤，「十二甲戌朔」是宋曆而非魏曆。張培瑜《三千五百年历日天象》和陳垣《二十史朔閏表》可能被《歷代長術輯要》誤導，記十一月乙亥朔及十二月甲辰朔。薛仲三、歐陽頤的《兩千年中西曆對照表》則沒有錯，奇怪的是臺灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換</a>卻不跟從《兩千年中西曆對照表》，也弄錯了十一月朔的日期。';
        } else {
            warn ='《通鉴目录》记十一月甲戌朔，汪曰桢《历代长术辑要》却记「十乙亥、十二甲戌朔、闰十(十甲辰小雪、十一甲戌冬至)」，没有记闰十月朔和十一月朔干支就是说两朔日的天干和都是乙，但是「十二甲戌」是错的，因为闰十朔是乙巳，而甲戌在乙巳后29日(或89日)，绝不可能是十二月朔，而且与其「十一甲戌冬至」相悖，可见「十二甲戌朔」应是「十一甲戌朔」之误，「十二甲戌朔」是宋历而非魏历。张培瑜《三千五百年历日天象》和陈垣《二十史朔闰表》可能被《历代长术辑要》误导，记十一月乙亥朔及十二月甲辰朔。薛仲三、欧阳颐的《两千年中西历对照表》则没有错，奇怪的是台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换</a>却不跟从《两千年中西历对照表》，也弄错了十一月朔的日期。';
        }
    }
    
    if (y==502 && m==6 && langVars.region=='default') {
        if (lang==0) {
            warn = "There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 5 in the main text but after month 4 in Appendix 3.";
        } else if (lang==1) {
            warn = "《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏五月，附表3則為閏四月。";
        } else {
            warn = "《三千五百年历日天象》的正文与其附表3的资料不一致，正文记這年闰五月，附表3则为闰四月。";
        } 
    }
    
    if (y==575 && m==9 && langVars.region=='default') {
        if (lang==0) {
            warn = "There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The leap month in this year is listed as after month 8 in the main text but after month 9 in Appendix 3.";
        } else if (lang==1) {
            warn = "《三千五百年历日天象》的正文與其附表3的資料不一致，正文記這年閏八月，附表3則為閏九月。";
        } else {
            warn = "《三千五百年历日天象》的正文与其附表3的资料不一致，正文记這年闰八月，附表3则为闰九月。";
        }
    }
    
    if (y==575 && m==9 && langVars.region=='WeiQi') {
        if (lang==0) {
            warn = "Appendix 3 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i> lists the leap month as after month 9. This is at odds with my calculation, which agrees with the data on the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The data in Appendix 3 are supposed to be based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by W&#257;ng Yu&#275;zh&#275;n (汪曰楨), but that book also lists the leap month as after month 8. That's why I use my calculation here.";
        } else if (lang==1) {
            warn = "《三千五百年历日天象》附表3記這年北齊閏九月，與我計算的閏八月不一致，台灣中央研究院的<a href='http://sinocal.sinica.edu.tw/' target='_blank'>兩千年中西曆轉換網站</a>和汪曰楨的《歷代長術輯要》也記這年閏八月，所以這裡不取《三千五百年历日天象》的數據。";
        } else {
            warn = '《三千五百年历日天象》附表3记这年北齐闰九月，与我计算的闰八月不一致，台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>和汪曰桢的《历代长术辑要》也记这年闰八月，所以这里不取《三千五百年历日天象》的数据。';
        }
    }

    return warn;
}

function calendarNotesTang(y, m, lang) {
    let warn = '';
    if (y==678 && (m==11 || m==12)) {
        if (lang==0) {
            warn = 'The <i>Old Book of Tang</i> mentions leap month 10 in this year. However, the <i>New Book of Tang</i> mentions leap month 11. Many scholars adopt the data in the <i>New Book of Tang</i>. However, Huang Yi-Long, Professor in the Institute of History at the National Tsing-Hua University in Taiwan, <a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">investigated the issue</a> and concludes that the record in the <i>Old Book of Tang</i> is more reliable. His analysis places leap month 10 beginning on Nov. 19 and month 11 beginning on Dec. 19.';
        } else if (lang==1) {
            warn = '《舊唐書》有閏十月的記載，《新唐書》卻有閏十一月記載，學者一般取《新唐書》的閏月。但台灣國立清華大學歷史研究所的黃一農教授經過<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考證</a>後認為《舊唐書》的記載比較可信。根據他的考證，閏十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。';
        } else {
            warn = '《旧唐书》有闰十月的记载，《新唐书》却有闰十一月记载，学者一般取《新唐书》的闰月。但台湾国立清华大学历史研究所的黄一农教授经过<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考证</a>后认为《旧唐书》的记载比较可信。根据他的考证，闰十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。';
        }
    }
    if (y==684 && m==1) {
        if (lang==0) {
            warn = 'The New Year day was supposed to be on Jan 22, but it was moved to Jan 23 by edict.';
        } else if (lang==1) {
            warn = '正月朔本在癸未(1月22日)，但唐高宗在弘道元年八月下旨，強將十二月改為大月，使正月朔移至甲申(1月23日)。';
        } else {
            warn = '正月朔本在癸未(1月22日)，但唐高宗在弘道元年八月下旨，强将十二月改为大月，使正月朔移至甲申(1月23日)。';
        }
    }
    if (y==697 && m==12) {
        if (lang==0) {
            warn = 'The calendrical winter solstice was originally on Dec. 18, but Empress Consort Wu changed several calendar dates by edict. It was claimed that several predicted conjunction dates in the previous years were incorrect, resulting in the Moon being visible on the last days of lunar months. The claim was in fact incorrect and was a pretense for the empress to change calendar dates so that the winter solstice would fall on the ji&#462; z&#464; day (Dec. 20) and coincide with the lunar conjunction. After an "investigation", it was decided that the winter solstice should be moved to the ji&#462; z&#464; day (Dec. 20), which "happened to coincide" with the lunar conjunction. Because of this change, the lunar month started on Nov. 20 became a leap month and the winter solstice became the New Year day. There was originally a leap month after month 12. It had to be changed to month 12. In order to do that, the middle solar term Z12 was moved from Jan 17, 698 to Jan 18, 698.';
        } else if (lang==1) {
            warn = '曆書冬至本在壬戌(12月18日)，閏十月本為正月，但武則天為了營造正月甲子合朔冬至之罕見曆象，七月下詔強行更改曆日。詔書偽稱曆官所推合朔時刻有不合天象，出現了「晦仍見月，有爽天經」之象，經「重更尋討」後「果差一日」，於是強將原本所推冬至移後二日為正月甲子合朔冬至，使原本的正月變為閏十月，為了除消原本所推的閏十二月，又強將大寒由壬辰(698年1月17日)推遲一日至癸巳(698年1月18日)。';
        } else {
            warn = '历书冬至本在壬戌(12月18日)，闰十月本为正月，但武则天为了营造正月甲子合朔冬至之罕见历象，七月下诏强行更改历日。诏书伪称历官所推合朔时刻有不合天象，出现了「晦仍见月，有爽天经」之象，经「重更寻讨」后「果差一日」，于是强将原本所推冬至移后二日为正月甲子合朔冬至，使原本的正月变为闰十月，为了除消原本所推的闰十二月，又强将大寒由壬辰(698年1月17日)推迟一日至癸巳(698年1月18日)。';
        }
    }
    if (y==698 && m==1) {
        if (lang==0) {
            warn = 'The calendrical Z12 was originally on Jan. 17, but was changed to Jan. 18 in order to cancel a leap month originally calculated but was moved to after the 10th month of the previous year.';
        } else if (lang==1) {
            warn = '曆書大寒本在壬辰(1月17日)，曆官強行移後一日以除消原本所推的閏月。';
        } else {
            warn = '历书大寒本在壬辰(1月17日)，历官强行移后一日以除消原本所推的闰月。';
        }
    }
    if (y==725 && m==1) {
        if (lang==0) {
            warn = 'The conjunction on Jan 19 was supposed to be the New Year day for the Chinese year in 725. However, in order to prevent a solar eclipse on the New Year day, the leap month was moved to a month earlier by edict and became the last month in the Chinese year in 724 and the New Year day was moved to Feb 18, 725.';
        } else if (lang==1) {
            warn = '丙辰朔本是開元十三年正月朔，為避正旦日食，當時強將閏月推前一月，使正月丙辰朔變閏十二月丙辰朔，閏正月丙戌朔(2月18日)變正月丙戌朔。';
        } else {
            warn = '丙辰朔本是开元十三年正月朔，为避正旦日食，当时强将闰月推前一月，使正月丙辰朔变闰十二月丙辰朔，闰正月丙戌朔(2月18日)变正月丙戌朔。';
        }
    }
    if (y==725 && m==2) {
        if (lang==0) {
            warn = 'The month associated with the conjunction on Feb 18 was supposed to be a leap month, but the leap month was moved to a month earlier in order to prevent a solar eclipse on the New Year day. As a result, the Feb 18 conjunction became the New Year day. The calendrical Z1 was also moved from Feb 16 to Feb 18 to be consistent with the change.';
        } else if (lang==1) {
            warn = '丙戌朔本是閏正月朔，為避正旦日食，當時強將閏月推前一月，故閏正月朔變為正月朔。曆書雨水(當時稱為啟蟄)本在甲申(2月16日)，亦強進為丙戌(2月18日)。';
        } else {
            warn = '丙戌朔本是闰正月朔，为避正旦日食，当时强将闰月推前一月，故闰正月朔变为正月朔。历书雨水(当时称为启蛰)本在甲申(2月16日)，亦强进为丙戌(2月18日)。';
        }
    }
    if (y==761 && m==12) {
        if (lang==0) {
            warn = "The z&#464; month was supposed to be month 11, but it became month 1 by edict. There were no months 11 and 12 in the year X&#299;n ch&#466;u";
        } else if (lang==1) {
            warn = "本來建子是十一月，改正朔後變成正月。農曆辛丑年沒有十一和十二月。";
        } else {
            warn = "本来建子是十一月，改正朔后变成正月。农历辛丑年没有十一和十二月。";
        }
    }
    if (y==762 && m==4) {
        if (lang==0) {
            warn = "Note that there was a second month 4 and second month 5 this year because it was decided that after the first month 5, the month numbers were switched back to the y&#237;n month being month 1, m&#462;o month being month 2, ch&#233;n being month 3, s&#236; month being month 4 and so on. As a result, there were two month 4s and two month 5s in this Chinese year. They can be distinguished by their sexagenary month cycles.";
        } else if (lang==1) {
            warn = "五月之後的那個月是四月。這是因為五月後正朔改回以建寅為正月、建卯為二月、建辰為三月、建巳為四月等。農曆壬寅年因此有兩個四月（建卯和建巳）和兩個五月（建辰和建午）。由於已註明月干支，這些重複的月份應不會被混潸。";
        } else {
            warn = "五月之后的那个月是四月。这是因为五月后正朔改回以建寅为正月、建卯为二月、建辰为三月、建巳为四月等。农历壬寅年因此有两个四月（建卯和建巳）和两个五月（建辰和建午）。由于已注明月干支，这些重复的月份应不会被混潸。";
        }
    }
    return warn;
}

function calendarNotesMing(y, m, lang) {
    let warn = '';

    // Gregorian calendar reform
    if (y==1582 && m==10) {
        if (lang==0) {
            warn = "Note that October 4 was followed by October 15 because of the Gregorian calendar reform.";
        } else if (lang==1) {
            warn = "由於格里高里曆改，10月4日的下一日是10月15日，跳了10日。";
        } else {
            warn = "由于格里高里历改，10月4日的下一日是10月15日，跳了10日。";
        }
    }
    
    // 1462
    if (y==1462 && m==11) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 11 on Nov. 22, which is inconsistent with the calendar issued by the Ming government (Nov. 21).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記十一月壬辰朔(11月22日)，不合當年的《大統曆》曆書(辛卯朔, 11月21日)，見<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中國史曆表朔閏訂正舉隅 &mdash; 以唐《麟德曆》行用時期為例」</a>緒言。';
        } else {
            warn = '《三千五百年历日天象》记十一月壬辰朔(11月22日)，不合当年的《大统历》历书(辛卯朔, 11月21日), 见<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中国史历表朔闰订正举隅 &mdash; 以唐《麟德历》行用时期为例」</a>绪言。';
        }
    }
    
    // 1581
    if (y==1581 && m==10) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 10 on Oct. 28, which is inconsistent with the calendar issued by the Ming government (Oct. 27).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記十月壬辰朔(10月28日)，不合當年的《大統曆》曆書(辛卯朔, 10月27日)，見《國家圖書館藏明代大統曆日彙編》第三冊第606頁。';
        } else {
            warn = '《三千五百年历日天象》记十月壬辰朔(10月28日)，不合当年的《大统历》历书(辛卯朔, 10月27日)，见《国家图书馆藏明代大统历日汇编》第三册第606页。';
        }
    }
    
    // 1588, 1589
    if (y==1588 && m==3) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 3 on Mar. 26, which is inconsistent with the calendar issued by the Ming government (Mar. 27).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記三月癸未朔(3月26日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">當年的《大統曆》曆書</a>(甲申朔, 3月27日)。';
        } else {
            warn = '《三千五百年历日天象》记三月癸未朔(3月26日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">当年的《大统历》历书</a>(甲申朔, 3月27日)。';
        }
    }
    if (y==1588 && m==4) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 4 on Apr. 25, which is inconsistent with the calendar issued by the Ming government (Apr. 26).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記四月癸丑朔(4月25日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">當年的《大統曆》曆書</a>(甲寅朔, 4月26日)。';
        } else {
            warn = '《三千五百年历日天象》记四月癸丑朔(4月25日)，不合<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">当年的《大统历》历书</a>(甲寅朔, 4月26日)。';
        }
    }
    if (y==1589 && m==1) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 12 on Jan. 17, which is inconsistent with the calendar issued by the Ming government (Jan. 16).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記十二月庚辰朔(1月17日)，不合當年的《大統曆》曆書(己卯朔, 1月16日)，見《國家圖書館藏明代大統曆日彙編》第四冊第175頁。';
        } else {
            warn = '《三千五百年历日天象》记十二月庚辰朔(1月17日)，不合当年的《大统历》历书(己卯朔, 1月16日)，见《国家图书馆藏明代大统历日汇编》第四册第175页。';
        }
    }
    
    // 1600
    if (y==1600 && m==2) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 14, which is inconsistent with the calendar issued by the Ming government (Feb. 15).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記正月乙巳朔(2月14日)，不合當年的《大統曆》曆書(丙午朔, 2月15日)，見《國家圖書館藏明代大統曆日彙編》第四冊第445頁。';
        } else {
            warn = '《三千五百年历日天象》记正月乙巳朔(2月14日)，不合当年的《大统历》历书(丙午朔, 2月15日)，见《国家图书馆藏明代大统历日汇编》第四册第445页。';
        }
    }
    
    // 1609
    if (y==1609 && m==2) {
        if (lang==0) {
            warn = '<i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day on Feb. 4, which is inconsistent with the calendar issued by the Ming government (Feb. 5).';
        } else if (lang==1) {
            warn = '《三千五百年历日天象》記正月癸未朔(2月4日)，不合當年的《大統曆》曆書(甲申朔, 2月5日)，見《國家圖書館藏明代大統曆日彙編》第五冊第67頁。';
        } else {
            warn = '《三千五百年历日天象》记正月癸未朔(2月4日)，不合当年的《大统历》历书(甲申朔, 2月5日)，见《国家图书馆藏明代大统历日汇编》第五册第67页。';
        }
    }

    return warn;
}

function calendarNotesQing(y, m, lang) {
    let warn = '';

    // 1645
    if (y==1645 && m==7) {
        if (lang==0) {
            warn = 'Note that leap month 6 contained the major solar term Z6, breaking the rule that a leap month must not contain a major solar term. W&#257;ng Yu&#275;zh&#275;n (&#27754;&#26352;&#26984;), a Chinese mathematician in the 19th century, explained that even though the solar term Z6 and the lunar conjunction associated with the month occurred on the same day, Z6 occurred earlier in the day than the lunar conjunction and was counted as a major solar term of the previous month. As a result, leap month 6 did not contain any major solar term. This "rule" was only used in this year. It was never used again after this year.';
        } else if (lang==1) {
            warn = '大暑這中氣出現在閏六月初一，違反了閏月不含中氣的規定。清朝曆算家汪曰楨解釋說雖然大暑與朔發生在同一日，大暑的時刻早於合朔時刻，屬於前月之中氣，所以閏六月不含中氣。這說法明顯不合傳統，屬於新的置閏法則，但是這新法則只在這一年用過，以後不再使用。';
        } else {
            warn = '大暑这中气出现在闰六月初一，违反了闰月不含中气的规定。清朝历算家汪曰桢解释说虽然大暑与朔发生在同一日，大暑的时刻早于合朔时刻，属于前月之中气，所以闰六月不含中气。这说法明显不合传统，属于新的置闰法则，但是这新法则只在这一年用过，以后不再使用。';
        }
        return warn;
    }

    // 1662
    if (y==1662 && m==2) {
        if (lang==0) {
            warn = 'The Chinese New Year in 1662 was originally on Feb. 19. There was a leap month after month 7 in 1661 and two major solar terms (Z11 and Z12) in month 11. The major solar term Z1 was originally placed on the last day of month 12 in 1661, leaving the first month in 1662 without a major solar term. To avoid controversy, the New Year Day was moved to Feb. 18 so that the first month would contain Z1, thus moving the month without major solar term to the last month of 1661.';
        } else if (lang==1) {
            warn = '康熙元年正月初一本在丙子日(2月19日)，事緣順治十八年閏七月，當年十一月含冬至和大寒兩中氣，雨水本來定在十二月晦，但這使康熙元年正月不含中氣。為免遭人非議，欽天監將正月初一提前一日至乙亥日(2月18日)，使正月含雨水，無中氣月便移到十二月。';
        } else {
            warn = '康熙元年正月初一本在丙子日(2月19日)，事缘顺治十八年闰七月，当年十一月含冬至和大寒两中气，雨水本来定在十二月晦，但这使康熙元年正月不含中气。为免遭人非议，钦天监将正月初一提前一日至乙亥日(2月18日)，使正月含雨水，无中气月便移到十二月。';
        }
        return warn;
    }
    
    // 1670
    if (y==1670 && m==1) {
        if (lang==0) {
            warn = 'The Chinese month that began on Jan 21 was a leap month according to the old calendar rule since it did not contain a major solar term. It was the first month of 1670 according to the new rule since it contained the major solar term Z1. In April 1669, the Kangxi Emperor abolished the old rule and ordered by decree to move the leap month from after the 12th month of 1669 to after the second month of 1670.';
        } else if (lang==1) {
            warn = '己丑朔(1月21日)對應的月份依舊法因不含中氣，為康熙八年閏十二月，依新法則含中氣雨水，為康熙九年正月。康熙帝在康熙八年三月下詔復用西洋新法，廢康熙八年閏十二月，改為康熙九年閏二月。';
        } else {
            warn = '己丑朔(1月21日)对应的月份依旧法因不含中气，为康熙八年闰十二月，依新法则含中气雨水，为康熙九年正月。康熙帝在康熙八年三月下诏复用西洋新法，废康熙八年闰十二月，改为康熙九年闰二月。';
        }
        return warn;
    }

    // 1679
    if (y==1679 && m==5) {
        if (lang==0) {
            warn = "In both <i>3500 Years of Calendars and Astronomical Phenomena</i> (by Zhang Peiyu) and <i>A Chinese calendar translated into the western calendar from 1516 to 1941</i> (by Zheng Hesheng), the calendrical solar term Z4 is listed on May 20. However, the Shixian Calendar for the 18th year of Emperor Kangxi's Reign (i.e. Feb. 11, 1679 - Jan. 30, 1680), a yearly calendar issued by the Imperial Astronomical Bureau in the Qing dynasty, lists Z4 on May 21 at 9:01am in Beijing's local apparent solar time. The calendarical solar term for Z4 is listed on May 21 here based on the Shixian Calendar.";
        } else if (lang==1) {
            warn = '張培瑜《三千五百年历日天象》和鄭鶴聲《近世中西史日對照表》皆記小滿為5月20日，但《大清康熙十八年歲次己未時憲曆》則載「(四月)十二日丙子巳初初刻一分小滿四月中」，即小滿在四月十二日(公曆5月21日)九時零一分(北京地方真太陽時)。這裡根據《大清時憲曆》記曆書小滿為公曆5月21日。';
        } else {
            warn = '张培瑜《三千五百年历日天象》和郑鹤声《近世中西史日对照表》皆记小满为5月20日，但《大清康熙十八年岁次己未时宪历》则载「(四月)十二日丙子巳初初刻一分小满四月中」，即小满在四月十二日(公历5月21日)九时零一分(北京地方真太阳时)。这里根据《大清时宪历》记历书小满为公历5月21日。';
        }
        return warn;
    }

    // 1848
    if (y==1848 && m==12) {
        if (lang==0) {
            warn = 'Z11 (December solstice) was on Dec 21 at 23:59:37 (UT1+8) according to the calculation using DE431. The calendrical Z11 was on Dec 22.';
        } else if (lang==1) {
            warn = 'DE431曆表算出的冬至時刻在12月21日23:59:57 (UT1+8)，曆書冬至在12月22日。';
        } else {
            warn = 'DE431历表算出的冬至时刻在12月21日23:59:57 (UT1+8)，历书冬至在12月22日。';
        }
        return warn;
    }

    // Deal with the calendrical solar terms after 1733 that didn't match solar terms 
    // computed by modern method
    let items = [{'y':1736, 'm':1, 's':'Z12', 'd':20},
              {'y':1739, 'm':1, 's':'J12', 'd':5},
              {'y':1744, 'm':7, 's':'Z6', 'd':22},
              {'y':1746, 'm':3, 's':'J2', 'd':5},
              {'y':1747, 'm':7, 's':'J6', 'd':7},
              {'y':1749, 'm':4, 's':'J3', 'd':4},
              {'y':1751, 'm':10, 's':'J9', 'd':9},
              {'y':1753, 'm':6, 's':'J5', 'd':5},
              {'y':1756, 'm':9, 's':'Z8', 'd':23},
              {'y':1760, 'm':4, 's':'Z3', 'd':19},
              {'y':1774, 'm':2, 's':'J1', 'd':3},
              {'y':1774, 'm':9, 's':'J8', 'd':8},
              {'y':1779, 'm':3, 's':'J2', 'd':5},
              {'y':1779, 'm':6, 's':'Z5', 'd':21},
              {'y':1781, 'm':12, 's':'J11', 'd':7},
              {'y':1782, 'm':4, 's':'J3', 'd':4},
              {'y':1784, 'm':10, 's':'J9', 'd':8},
              {'y':1787, 'm':2, 's':'Z1', 'd':18},
              {'y':1807, 'm':2, 's':'J1', 'd':4},
              {'y':1809, 'm':1, 's':'J12', 'd':5},
              {'y':1809, 'm':11, 's':'Z10', 'd':23},
              {'y':1812, 'm':3, 's':'J2', 'd':5},
              {'y':1815, 'm':4, 's':'J3', 'd':5},
              {'y':1817, 'm':10, 's':'J9', 'd':9},
              {'y':1820, 'm':2, 's':'Z1', 'd':19},
              {'y':1824, 'm':8, 's':'J7', 'd':8},
              {'y':1826, 'm':5, 's':'Z4', 'd':21},
              {'y':1829, 'm':11, 's':'J10', 'd':8},
              {'y':1836, 'm':9, 's':'J8', 'd':8},
              {'y':1844, 'm':6, 's':'J5', 'd':6},
              {'y':1846, 'm':11, 's':'Z10', 'd':23},
              {'y':1849, 'm':5, 's':'J4', 'd':5},
              {'y':1850, 'm':10, 's':'J9', 'd':9},
              {'y':1851, 'm':9, 's':'Z8', 'd':24},
              {'y':1851, 'm':12, 's':'J11', 'd':8},
              {'y':1855, 'm':4, 's':'Z3', 'd':20},
              {'y':1862, 'm':10, 's':'Z9', 'd':24},
              {'y':1862, 'm':11, 's':'J10', 'd':8},
              {'y':1864, 'm':7, 's':'Z6', 'd':23},
              {'y':1866, 'm':10, 's':'Z9', 'd':24},
              {'y':1867, 'm':7, 's':'J6', 'd':8},
              {'y':1867, 'm':8, 's':'Z7', 'd':24},
              {'y':1879, 'm':1, 's':'J12', 'd':6},
              {'y':1879, 'm':11, 's':'Z10', 'd':23},
              {'y':1883, 'm':10, 's':'J9', 'd':9},
              {'y':1884, 'm':9, 's':'Z8', 'd':23},
              {'y':1884, 'm':12, 's':'J11', 'd':7},
              {'y':1886, 'm':8, 's':'J7', 'd':8},
              {'y':1895, 'm':10, 's':'Z9', 'd':24},
              {'y':1895, 'm':11, 's':'J10', 'd':8},
              {'y':1898, 'm':9, 's':'J8', 'd':8},
              {'y':1899, 'm':6, 's':'Z5', 'd':22},
              {'y':1899, 'm':10, 's':'Z9', 'd':24}];
    let nitems = items.length;
    for (let i=0; i<nitems; i++) {
        if (y==items[i]['y'] && m==items[i]['m']) {
            let stName = langConstant(lang).soltermNames;
            let stLab = ["J12", "Z12", "J1", "Z1", "J2", "Z2", "J3","Z3", 
                         "J4", "Z4", "J5", "Z5", "J6", "Z6", "J7", "Z7", 
                        "J8", "Z8", "J9", "Z9", "J10", "Z10", "J11", "Z11"];
            // create a solar term dictionarys
            let sts = {};
            for (let j=0; j<24; j++) {
                sts[stLab[j]] = stName[j];
            }
            let sterm = sts[items[i]['s']]; // look up the name of the solar term
            if (lang==0) {
                let mon = ['January ', 'February ', 'March ', 'April ', 'May ', 'June ', 'July ', 'August ', 'September ', 'October ', 'November ', 'December ']
                warn = 'The calendrical ' + sterm + ' was on ' + mon[m-1] + items[i]['d'];
            } else {
                warn = (lang==1 ? '曆書':'历书') + sterm + '在' + items[i]['d'] + '日。'
            }
            return warn;
        }
    }

    return warn;
}

function SouthernMingCalendarDateNotes(y, m, lang) {
    let notes = [
        {y:1648, m:4, 
        w:['Several sources indicate that the leap month in this year was after the 6th month, which I find to be very unlikely.', 
        '王叔武"南明史料朔閏考異"引 《劫灰錄》、 《鹿樵紀聞》、 《明季南略》、 《爝火錄》說永曆二年閏六月，我認為閏六月很可能不對。', 
        '王叔武"南明史料朔闰考异"引 《劫灰录》、 《鹿樵纪闻》、 《明季南略》、 《爝火录》说永历二年闰六月，我认为闰六月很可能不对。']}, 

        {y:1649, m:2, 
        w:['Two dfferent versions of calendar in the Southern Ming dynasty were produced in the Chinese year in 1649. One of them was produced by the officials of the Yongli emperor, in which the New Year day was on February 11th, 1649. Another version was produced by the officials of the Prince of Lu, who named himself regent. The New Year day of the Lu calendar was on February 12th, 1649. According to the calculation of the Datong system, the New Year day was on February 11th, 1649.', 
        '永曆三年和魯王監國四年正月朔有異:永曆三年正月庚申朔(公曆2月11日);《魯監國大統曆》則有魯監國四年正月辛酉朔(2月12日)。依明大統曆推算此年正月朔為庚申。', 
        '永历三年和鲁王监国四年正月朔有异:永历三年正月庚申朔(公历2月11日);《鲁监国大统历》则有鲁监国四年正月辛酉朔(2月12日)。依明大统历推算此年正月朔为庚申。']},

        {y:1650, m:12, 
         w:["According to <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Y&#225;n P&#237;ng W&#225;ng H&#249; Gu&#257;n Y&#225;ng Y&#299;ng C&#243;ng Zh&#275;ng Sh&#237; L&#249;</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in 1650 was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a>, <a href='N1676_Zheng.html'>1676</a> and <a href='N1677_Zheng.html'>1677</a> recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.", 
         '傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>、<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。', 
         '傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>、<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。']}, 
        {y:1651, m:1, 
         w:["According to <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Y&#225;n P&#237;ng W&#225;ng H&#249; Gu&#257;n Y&#225;ng Y&#299;ng C&#243;ng Zh&#275;ng Sh&#237; L&#249;</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in 1650 was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a>, <a href='N1676_Zheng.html'>1676</a> and <a href='N1677_Zheng.html'>1677</a> recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.", 
         '傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>、<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。', 
         '傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>、<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。']},

        {y:1652, m:2, 
         w:["Two dfferent versions of calendar were produced in the Chinese year in 1652: emperor Yongli's and Prince Lu's version. The New Year day of the Yongli calendar was on February 10th, 1652. The New Year day of the Lu calendar was on February 9th, 1652. According to the calculation of the Datong system, the New Year day was on February 10th, 1652.", 
         '永曆六年和魯王監國七年正月朔有異:永曆六年正月甲戌朔(公曆2月10日);《魯監國大統曆》則有魯監國七年正月癸酉朔(2月9日)。依明大統曆推算此年正月朔為甲戌。', 
         '永历六年和鲁王监国七年正月朔有异:永历六年正月甲戌朔(公历2月10日);《鲁监国大统历》则有鲁监国七年正月癸酉朔(2月9日)。依明大统历推算此年正月朔为甲戌。']},

        {y:1653, m:8, 
         w:["There are discrepancies in the leap month in this year among various sources. <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records the leap month to be after the 7th month, which is consistent with the caleculation of the Datong system. <i>Y&#225;n P&#237;ng W&#225;ng H&#249; Gu&#257;n Y&#225;ng Y&#299;ng C&#243;ng Zh&#275;ng Sh&#237; L&#249;</i> or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i> has the leap month after the 8th month. The chronicle <i>X&#237;ng Z&#224;i Y&#225;ng Qi&#363;</i> records the leap month to be after the 6th month. The Datong calendar produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a> also records leap month after the 6th month. However, in the Datong calendar for <a href='N1676_Zheng.html'>1676</a> and <a href='N1677_Zheng.html'>1677</a>, the leap month is changed to being after the 8th month. I think leap month 6 is unlikely. Both leap month 7 and 8 are possible. Here I follow <i>Datong Calendar of the Waning Ming Dynasty</i> and place the leap month after the 7th month.", 
         '此年的閏月有爭議，依大統曆推算閏七月，傅以禮《殘明大統曆》亦記閏七月，但是《延平王戶官楊英從征實錄》記閏八月，《行在陽秋》記閏六月，明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>也記閏六月，但是後來頒行的<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>卻改為閏八月。我認為閏六月不大可能，閏七月和閏八月機會較大，此處依《殘明大統曆》記閏七月。', 
         '此年的闰月有争议，依大统历推算闰七月，傅以礼《残明大统历》亦记闰七月，但是《延平王户官杨英从征实录》记闰八月，《行在阳秋》记闰六月，明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>也记闰六月，但是后来颁行的<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>却改为闰八月。我认为闰六月不大可能，闰七月和闰八月机会较大，此处依《残明大统历》记闰七月。']}, 

        {y:1663, m:9, 
         w:['Calendrical J8 should be on September 6th according to the calculation of the Datong system. However, <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records J8 on September 5th, which is the date listed here.', 
         '依大統曆推算白露在八月初五(公曆9月6日)，但傅以禮《殘明大統曆》記八月初四(9月5日)，此處曆書白露依《殘明大統曆》。', 
         '依大统历推算白露在八月初五(公历9月6日)，但傅以礼《残明大统历》记八月初四(9月5日)，此处历书白露依《残明大统历》。']}, 

        {y:1671, m:2, 
         w:["The Chinese Near Year in 1671 was on February 9th according to <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i>, which also agrees with the calculation of the Datong system. However, the Datong calendar produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a> indicates that the New Year day was on February 10th. Even though Zheng dynasty claimed that their calendars were produced expediently and should not to be taken as official, by this time the Yongli emperor had died and the Southern Ming dynasty had already ended. Zheng's calendar became the de facto official Datong calendar of the state. So I change the New Year day to February 10th in accord with Zheng's calendar.", 
         '依大統曆推算永曆二十五正月朔在癸丑(公曆2月9日)，傅以禮《殘明大統曆》亦記正月癸丑朔，但是明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>記正月甲寅朔(2月10日)。雖然鄭氏奉明正朔，聲稱其大統曆乃「權宜頒行」，但是當時永曆帝已死，南明也已亡，明鄭的大統曆變相成為正統的大統曆書，所以此處依明鄭大統曆記正月甲寅朔。', 
         '依大统历推算永历二十五正月朔在癸丑(公历2月9日)，傅以礼《残明大统历》亦记正月癸丑朔，但是明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>记正月甲寅朔(2月10日)。虽然郑氏奉明正朔，声称其大统历乃「权宜颁行」，但是当时永历帝已死，南明也已亡，明郑的大统历变相成为正统的大统历书，所以此处依明郑大统历记正月甲寅朔。']}, 

        {y:1674, m:7, 
         w:['According to the calculation of the Datong system, the month 6 conjunction was on July 4th, which is inconsistent with the record in <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> (July 3rd). July 3rd is used here.', 
         '依明大統曆推算六月朔在甲午(公曆7月4日)，此處依傅以禮《殘明大統曆》改為六月癸巳朔(7月3日)。', 
         '依明大统历推算六月朔在甲午(公历7月4日)，此处依傅以礼《残明大统历》改为六月癸巳朔(7月3日)。']}, 

        {y:1674, m:9, 
         w:['According to the calculation of the Datong system, the month 9 conjunction was on September 30th, which is inconsistent with the record in <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> (September 29th). September 29th is used here.', 
         '依明大統曆推算九月朔在壬戌(公曆9月30日)，此處依傅以禮《殘明大統曆》改為九月辛酉朔(9月29日)。', 
         '依明大统历推算九月朔在壬戌(公历9月30日)，此处依傅以礼《残明大统历》改为九月辛酉朔(9月29日)。']}, 

        {y:1675, m:7, 
         w:['According to the calculation of the Datong system, a conjunction occurred on July 22nd. <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records a conjunction on July 23rd. The one-day difference changed the leap month in this year. July 22nd conjunction resulted in a leap month after the 5th month. July 23rd conjunction resulted in a leap month after the 6th month. Leap month 6 is also recorded in the calendars produced by the Zheng dynasty for <a href="N1676_Zheng.html">1676</a> and <a href="N1677_Zheng.html">1677</a>. So I use the data in <i>Datong Calendar of the Waning Ming Dynasty</i>.', 
         '依明大統曆推算有朔日在丁巳(公曆7月22日)，對應的朔日在傅以禮《殘明大統曆》出現在下一日戊午(7月23日)。此一日之差造成閏月分歧:依大統曆推算閏五月，《殘明大統曆》則為閏六月。明鄭頒行的<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>都記永曆二十九年閏六月，所以此處朔閏依《殘明大統曆》。', 
         '依明大统历推算有朔日在丁巳(公历7月22日)，对应的朔日在傅以礼《残明大统历》出现在下一日戊午(7月23日)。此一日之差造成闰月分歧:依大统历推算闰五月，《残明大统历》则为闰六月。明郑颁行的<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>都记永历二十九年闰六月，所以此处朔闰依《残明大统历》。']}, 

         {y:1676, m:12,
          w:['<i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> records that Z11 (winter solstice) was on the 16th day in month 11 (Dec. 20), which is inconsistent with the calculation of the Datong system (Dec. 21). The official <a href="N1676_Zheng.html">Datong Calendar for 1676</a> records Z11 on the 17th day in month 11 (Dec. 21). So the Z11 date in <i>Datong Calendar of the Waning Ming Dynasty</i> is wrong.', 
          '《殘明大統曆》記冬至在十一月十六(公曆12月20日)，不合明大統曆的推步(十一月十七)。明鄭頒行的<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>記冬至在十一月十七(12月21日)，證實《殘明大統曆》的冬至日期錯了。', 
          '《残明大统历》记冬至在十一月十六(公历12月20日)，不合明大统历的推步(十一月十七)。明郑颁行的<a href="N1676_Zheng_simp.html">永历三十年大统历</a>记冬至在十一月十七(12月21日)，证实《残明大统历》的冬至日期错了。']},

         {y:1677, m:7, 
          w:['According to the calculation of the Datong system, month 7 conjunction was on July 29th, which is inconsistent with July 30th recorded in <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or  <i>Datong Calendar of the Waning Ming Dynasty</i> and the calendar produced by the Zheng dynasty for <a href="N1677_Zheng.html">1677</a>. The Zheng calendar date is used here.', 
         '依明大統曆推算七月朔在乙亥(公曆7月29日)，不合傅以禮《殘明大統曆》及明鄭<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>的丙子朔(7月30日)。此處依《殘明大統曆》及明鄭大統曆記七月丙子朔。', 
         '依明大统历推算七月朔在乙亥(公历7月29日)，不合傅以礼《残明大统历》及明郑<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>的丙子朔(7月30日)。此处依《残明大统历》及明郑大统历记七月丙子朔。']}, 

        {y:1678, m:7, 
         w:['According to the calculation of the Datong system, the month 6 conjunction was on July 18th, inconsistent with July 19th recorded in <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or  <i>Datong Calendar of the Waning Ming Dynasty</i>. July 19th is used here.', 
         '依明大統曆推算六月朔在己巳(公曆7月18日)，不合傅以禮《殘明大統曆》的庚午朔(7月19日)。此處依《殘明大統曆》記六月庚午朔。', 
         '依明大统历推算六月朔在己巳(公历7月18日)，不合傅以礼《残明大统历》的庚午朔(7月19日)。此处依《残明大统历》记六月庚午朔。']}, 

        {y:1682, m:2, 
         w:['According to the calculation of the Datong system, the Chinese New Year in 1682 was on February 8th, inconsistent with February 7th recorded in <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i>. February 7th is used here.', 
         '依明大統曆推算永曆三十六年正月朔在庚戌(公曆2月8日)，不合傅以禮《殘明大統曆》的己酉朔(2月7日)。此處依《殘明大統曆》記正月己酉朔。', 
         '依明大统历推算永历三十六年正月朔在庚戌(公历2月8日)，不合傅以礼《残明大统历》的己酉朔(2月7日)。此处依《残明大统历》记正月己酉朔。']}
    ];
    
    let n = notes.length;
    let warn = '';
    for (let i=0; i<n; i++) {
        if (y==notes[i].y && m==notes[i].m) {
            warn = notes[i].w[lang];
            break;
        }
    }
    return warn;
}

function calendarNotes1912_1979(y, m, lang) {
    let notes = [{'y':1912, 'm':11, 
         'n':['The calendrical Z10 was on Nov 23.', 
              '曆書小雪在23日。', '历书小雪在23日。']}, 
         {'y':1913, 'm':9,
          'n':['The calendrical Z8 (September equinox) was on Sep 24.',
               '曆書秋分在24日。', '历书秋分在24日。']},
        {'y':1917, 'm':12,
         'n':['The calendrical J11 was on Dec 7.',
              '曆書大雪在7日。', '历书大雪在7日。']},
        {'y':1927, 'm':9,
         'n':['The calendrical J8 was on Sep 8.',
              '曆書白露在8日。', '历书白露在8日。']},
        {'y':1928, 'm':6,
         'n':['The calendrical Z5 (June solstice) was on June 21.',
              '曆書夏至在21日。', '历书夏至在21日。']},
        {'y':1979, 'm':1,
         'n':['Z12 calculated by DE431 was at 23:59:54 (UTC+8) on Jan. 20. <i>Chinese Astronomical Almanac for the Year 1979</i> lists Z12 at 00:00 (UTC+8) on Jan 21, so the calendrical Z12 was on Jan 21.',
              'DE431曆表推算的大寒時刻是1月20日23:59:54 (UTC+8)，《一九七九年中国天文年历》載大寒時刻為1月21日00:00 (UTC+8)，故曆書大寒在1月21日。',
              'DE431历表推算的大寒时刻是1月20日23:59:54 (UTC+8)，《一九七九年中国天文年历》载大寒时刻为1月21日00:00 (UTC+8)，故历书大寒在1月21日。']}];
    let nnotes = notes.length;
    for (let i=0; i<nnotes; i++) {
        if (y==notes[i]['y'] && m==notes[i]['m']) {
            return notes[i]['n'][lang];
        }
    }

    return '';
}

function calendarNotesAfter2050(y, m, lang, langVars) {
    let suffix_eng = " is close to the midnight. The actual date may be off by one day.";
    let suffix_chi = "的時刻接近午夜零時，實際日期或會與所示日期有一日之差。";
    let suffix_sim = "的时刻接近午夜零时，实际日期或会与所示日期有一日之差。";
    let warn = '';

    if (y==2051) {
        if (m==3) {
            if (lang==0) {
                warn = "The time of Z2 (March equinox)"+suffix_eng;
            } else {
                warn = "春分"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2057) {
        if (m==9) warn = langVars.note_early;
    }
    
    if (y==2083) {
        if (m==2) {
            if (lang==0) {
                warn = "The time of J1"+suffix_eng;
            } else {
                warn = "&#31435;&#26149;"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2084) {
        if (m==3) {
            if (lang==0) {
                warn = "The time of Z2 (March equinox)"+suffix_eng;
            } else {
                warn = "&#26149;&#20998;"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2089) {
        if (m==9) warn = langVars.note_late;
    }
    
    if (y==2097) {
        if (m==8) warn = langVars.note_early;
    }
    
    if (y==2114) {
        if (m==11) {
            if (lang==0) {
                warn = "The time of Z10"+suffix_eng;
            } else {
                warn = "小雪"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2115) {
        if (m==2) warn = langVars.note_late;
    }
    
    if (y==2116) {
        if (m==5) warn = langVars.note_late;
    }
    
    if (y==2133) {
        if (m==9) warn = langVars.note_early;
    }
    
    if (y==2142) {
        if (m==9) {
            if (lang==0) {
                warn = "The time of J8"+suffix_eng;
            } else {
                warn = "白露"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2155) {
        if (m==10) {
            if (lang==0) {
                warn = "The time of Z9"+suffix_eng;
            } else {
                warn = "霜降"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2157) {
        if (m==12) {
            if (lang==0) {
                warn = "The time of Z11 (December solstice)"+suffix_eng;
            } else {
                warn = "冬至"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2165) {
        if (m==12) warn = langVars.note_early;
    }
    
    if (y==2172) {
        if (m==10) warn = langVars.note_early;
    }
    
    if (y==2183) {
        if (m==3) {
            if (lang==0) {
                warn = "The time of Z2 (March equinox)"+suffix_eng;
            } else {
                warn = "春分"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }
    
    if (y==2186) {
        if (m==2) {
            if (lang==0) {
                warn = "The time of J1"+suffix_eng;
            } else {
                warn = "立春"+(lang==1 ? suffix_chi:suffix_sim);
            }
        }
    }

    return warn;
}

// TEST
function calendarOut(lang, year, region, li=null) {
    let langVars = langConstant(lang);
    langVars.region = region;
    langVars.li_ancient = li;
    let calVars = calDataYear(year, langVars);
    let cal = '';
    
    // How many Chinese years does this Gregorian/Julian calendar span?
    let n = calVars.cmonthDate.length;
    let Ncyear = calVars.cmonthYear[n-1] - calVars.cmonthYear[0] + 1;
    
    // Determine the date(s) of the Chinese new year
    let i,j,k,mm,dd;
    let mm1 = [], dd1 = [];
    let firstMonth = [0,0,0];
    for (i=0; i<3; i++) {
       if (year > -110) {
           firstMonth[i] = firstMonthNum(year-1+i);
       } else {
           firstMonth[i] = calVars.firstMonthNum;
       }
    }
    for (i=1; i<Ncyear; i++) {
        let firstMon = firstMonth[calVars.cmonthYear[0] + i];
        for(j=1; j<n; j++) {
            if (calVars.cmonthYear[j]==calVars.cmonthYear[0]+i && 
                calVars.cmonthNum[j]==firstMon) {
                dd = calVars.cmonthDate[j];
                for (k=0; k<13; k++) {
                    if (dd <= calVars.mday[k]) {
                        mm = k;
                        break;
                    }
                }
                mm1.push(mm); dd1.push(dd - calVars.mday[mm-1]);
            }
        }
    }
    
    let ih0 = (year + 725) % 10;
    let ie0 = (year + 727) % 12;
    if (ih0 < 0) { ih0 += 10;}
    if (ie0 < 0) { ie0 += 12;}
    let cyear = [" ", " ", " "];
    cyear[0] = langVars.heaven[ih0]+' '+langVars.earth[ie0]+' ('+langVars.animal[ie0]+')';
    let ih = (year + 726) % 10;
    let ie = (year + 728) % 12;
    if (ih < 0) { ih += 10;}
    if (ie < 0) { ie += 12;}
    cyear[1] = langVars.heaven[ih]+' '+langVars.earth[ie]+' ('+langVars.animal[ie]+')';
    let ih2 = (year + 727) % 10;
    let ie2 = (year + 729) % 12;
    if (ih2 < 0) { ih2 += 10;}
    if (ie2 < 0) { ie2 += 12;}
    cyear[2] = langVars.heaven[ih2]+' '+langVars.earth[ie2]+' ('+langVars.animal[ie2]+')';
    let gcal = (year > 1582 ? "Gregorian":(year > 7 ? "Julian":"(Proleptic) Julian"));
    if (year==1582) { gcal = "Gregorian/Julian";}
    let yearc = year.toString();
    if (year < 1) {
        yearc += (lang==0 ? ' ('+(1-year)+' BCE)':' (前'+(1-year)+')');
    }
    let cy0 = calVars.cmonthYear[0];
    if (lang==0) {
        cal += '<h1>'+gcal+' Year: '+yearc+'</h1>\n';
        cal += '<h1>Chinese year:</h1>\n'
        if (Ncyear==1) {
            cal += '<h2>'+cyear[cy0]+'</h2> <br />\n';
        } else if (Ncyear==2) {
            cal += '<h2>'+cyear[cy0]+' before '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+',<br />'+cyear[cy0+1]+' on and after '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+'</h2> <br />\n';
        } else {
            cal += '<h2>'+cyear[cy0]+' before '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+',<br />'+cyear[cy0+1]+' between '+langVars.gMonth[mm1[0]-1]+' '+dd1[0]+' and '+langVars.gMonth[mm1[1]-1]+' '+(dd1[1]-1)+',<br />'+cyear[cy0+2]+' on and after '+langVars.gMonth[mm1[1]-1]+' '+dd1[1]+'</h2> <br />\n';
        }      
    } else {
        if (lang==1) {
            cyear[0] += eraName(year-1, langVars.region, li);
            cyear[1] += eraName(year, langVars.region, li);
            cyear[2] += eraName(year+1, langVars.region, li);
        } else {
            cyear[0] += eraNameSim(year-1, langVars.region, li);
            cyear[1] += eraNameSim(year, langVars.region, li);
            cyear[2] += eraNameSim(year+1, langVars.region, li);
        }
        if (lang==1) {
            cal += '<h1>公曆年: '+yearc+'</h1>\n';
            cal += '<h1>農曆年:</h1>\n';
        } else {
            cal += '<h1>公历年: '+yearc+'</h1>\n';
            cal += '<h1>农历年:</h1>\n';
        }
        let tmp;
        if (Ncyear==1) {
            cal += '<h2>'+cyear[cy0]+'</h2> <br />\n';
        } else if (Ncyear==2) {
            tmp = '<h2>'+mm1[0]+'月'+dd1[0]+'日前: '+cyear[cy0]+', ';
            if (year < 1912) {
                tmp += '<br />';
            }
            tmp += mm1[0]+'月'+dd1[0]+'日及以後: '+cyear[cy0+1]+'</h2><br />';
            cal += tmp+'\n';
        } else {
            cal += '<h2>'+mm1[0]+'月'+dd1[0]+'日前: '+cyear[cy0]+',<br /> '+mm1[0]+'月'+dd1[0]+'日至'+mm1[1]+'月'+(dd1[1]-1)+'日: '+cyear[cy0+1]+',<br />'+mm1[1]+'月'+dd1[1]+'日及以後: '+cyear[cy0+2]+'</h2><br />\n';
        }
    }
    
    if (lang==0) {
        cyear[0] = langVars.heaven[ih0]+' '+langVars.earth[ie0];
        cyear[1] = langVars.heaven[ih]+' '+langVars.earth[ie];
        cyear[2] = langVars.heaven[ih2]+' '+langVars.earth[ie2];
    } else {
        cyear[0] = langVars.heaven[ih0]+langVars.earth[ie0]+'年';
        cyear[1] = langVars.heaven[ih]+langVars.earth[ie]+'年';
        cyear[2] = langVars.heaven[ih2]+langVars.earth[ie2]+'年';
    }
    
    // Add additional information after the year info
    let info = addYearInfo(year, langVars, calVars);
    if (info != "") {
        let h3 = (lang==0 ? '<h3 style="color:brown;line-height:26px;">':'<h3 style="color:brown;letter-spacing:4px;line-height:30px;">');
        cal += h3+info+'</h3><br /><br />\n';
    }
    
    for (let m=0; m<12; m++) {
        cal += printMonth(m, lang, year, cyear, firstMonth, 
                                    langVars, calVars)+'\n';
    }
    
    return cal;
}

function outputContent_forTestingMed(lang, y1, y2, region, li=null) {
    let txt = calendarOut(lang,y1, region, li);
    for (let y=y1+1; y <= y2; y++) {
        txt += calendarOut(lang, y, region, li);
    }
    return txt;
}

function outputContent_forTesting_allYears_default(lang) {
    let sub = (lang==0 ? '_eng':(lang==1 ? '_chinese':'_simp'));
    let outfile = 'calendar_default_-721to2200'+sub+'.txt', region='default';
    let txt = calendarOut(lang, -721, region, 'Chunqiu');
    let y;
    for (y=-720; y<-479; y++) {
        txt += calendarOut(lang, y, region, 'Chunqiu');
    }
    for (y=-479; y<-220; y++) {
        txt += calendarOut(lang, y, region, 'Zhou');
    }
    txt += calendarOut(lang, -220, region, 'Zhuanxu');
    txt += calendarOut(lang, -219, region, 'Zhuanxu');
    for (y=-218; y<2201; y++) {
        txt += calendarOut(lang, y, region);
    }
    download_txt(txt, outfile);
}

function outputContent_forTesting_period(lang, period) {
    let txt ='';
    if (period=='SpringWarring') {
        let lis = ['Zhou', 'Yin', 'Xia2'];
        let lisid = ['zhouSpring', 'yinSpring', 'xiaSpring'];
        lis.forEach(function (li,i) {
            txt += lisid[i]+'\n';
            txt += outputContent_forTestingMed(lang, -721, -480, 'default', li);
        });
        lis = ['Lu', 'Huangdi', 'Yin', 'Xia1', 'Zhuanxu'];
        lisid = ['luWarring', 'huangdiWarring', 'yinWarring', 'xiaWarring', 'zhuanxuWarring'];
        lis.forEach(function (li,i) {
            txt += lisid[i]+'\n'
            txt += outputContent_forTestingMed(lang, -479, -221, 'default', li);
        });
    } else if (period=='ShuWu') {
        txt = 'Shu\n';
        txt += outputContent_forTestingMed(lang, 221, 263, 'Shu');
        txt += 'Wu\n';
        txt += outputContent_forTestingMed(lang, 222, 280, 'Wu');
    } else if (period=='SouthNorth') {
        txt = 'Later Qin\n';
        txt += outputContent_forTestingMed(lang, 384, 417, 'LaterQin');
        txt += 'Northern Liang\n';
        txt += outputContent_forTestingMed(lang, 412, 439, 'NorthernLiang');
        txt += 'Northern Wei, Western Wei, Northern Zhou, Sui\n';
        txt += outputContent_forTestingMed(lang, 398, 590, 'WeiZhouSui');
        txt += 'Eastern Wei, Northern Qi\n';
        txt += outputContent_forTestingMed(lang, 534, 577, 'WeiQi');
    } else if (period=='LiaoJinYuan') {
        txt = outputContent_forTestingMed(lang, 947, 1279, 'LiaoJinYuan');
    }
    let sub = (lang==0 ? '_eng':(lang==1 ? '_chinese':'_simp'));
    download_txt(txt, 'calendar_'+period+sub+'.txt');
}

// Create file for download
function download_txt(data, filename) {
    // create link to download data
    let hiddenElement = window.document.createElement('a');
    hiddenElement.href = window.URL.createObjectURL(new Blob([data], {type: 'text/csv'}));
    hiddenElement.download = filename;

    // Append anchor to body.
    document.body.appendChild(hiddenElement);
    hiddenElement.click();

    // Remove anchor from body
    document.body.removeChild(hiddenElement);
}
