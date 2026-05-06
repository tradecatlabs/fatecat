"use strict";

function init(lang) {
    header(lang, 'table', ''); // print menu
    if (window.location === window.parent.location) {
        const p = new URLSearchParams(window.location.search);
        if (p.has('period')) {
            let valid_periods = ['Spring', 'Warring', 'qinhanxin', 'easternhan', 'weishuwu', 'jin', 
                                'snweiqizhou', 'snsouth', 'sui', 'tang5', 'song', 'liaojin', 'yuan', 
                                'ming', 'qing', 'recent'];
            let period = p.get('period');
            let match = valid_periods.map(x => x==period).reduce((a,b) => a || b, false);
            if (!match) {
                let table_url = ['table.html', 'table_chinese.html', 'table_simp.html'];
                window.location.replace(table_url[lang]);
            } else {
                let txt = '<h2 style="text-align:right;">';
                let link = 'table_period';
                let qs = '.html?period='+period;
                if (lang==0) {
                    txt += 'Chinese versions: <a href="'+link+'_chinese'+qs+'">傳統中文</a> &nbsp; <a href="'+link+'_simp'+qs+'">简体中文</a></h2>';
                } else if (lang==1) {
                    txt += '<a href="'+link+qs+'">English 英文</a> &nbsp; <a href="'+link+'_simp'+qs+'">简体中文</a></h2>';
                } else {
                    txt += '<a href="'+link+qs+'">English 英文</a> &nbsp; <a href="'+link+'_chinese'+qs+'">傳統中文</a></h2>';
                }
                document.getElementById('language').innerHTML = txt;
                setup_table(lang, period);
                }
        } else {
            let table_url = ['table.html', 'table_chinese.html', 'table_simp.html'];
            window.location.replace(table_url[lang]);
        }
    } else {
        exception_handler();
    }
    // *** TEST ***
    //output_multiple_periods(lang);
    // ************
}

function setup_table(lang, period) {
    document.getElementById('returnMainMenu').style.display = "block";
    document.getElementById('returnMainMenuEnd').style.display = "block";
    document.getElementById('menu').scrollIntoView();
    if (period == "Spring") {
        document.getElementById("Spring").style.display = "block";
    }
    if (period == "Warring") {
        document.getElementById("Warring").style.display = "block";
    } 
    
    switch(period) {
        case 'Spring':
            table_spring(lang);
            break;
        case 'Warring':
            table_warring(lang);
            break;
        case 'qinhanxin':
            table_qinhanxin(lang);
            break;
        case 'easternhan':
            table_easternhan(lang);
            break;
        case 'weishuwu':
            table_weishuwu(lang);
            break;
        case 'jin':
            table_jin(lang);
            break;
        case 'snweiqizhou':
            table_snweiqizhou(lang);
            break;
        case 'snsouth':
            table_snsouth(lang);
            break;
        case 'sui':
            table_sui(lang);
            break;
        case 'tang5':
            table_tang5(lang);
            break;
        case 'song':
            table_song(lang);
            break;
        case 'liaojin':
            table_liaojin(lang);
            break;
        case 'yuan':
            table_yuan(lang);
            break;
        case 'ming':
            table_ming(lang);
            break;
        case 'qing':
            table_qing(lang);
            break;
        case 'recent':
            table_recent(lang);
    }
}

// Language-specific constants
function langConstant(lang) {
    let heaven, earth, animal, Wyear, Cyear, Cmonth, month_num, 
        Ndays, note_early, note_late;
    if (lang==0) {
        // English
        heaven = ["Ji&#462;","Y&#464;","B&#464;ng","D&#299;ng","W&#249;", 
                  "J&#464;", "G&#275;ng","X&#299;n","R&#233;n", "Gu&#464;"]; // heavenly stems
        earth = ["z&#464;", "ch&#466;u", "y&#237;n", "m&#462;o", "ch&#233;n", 
                "s&#236;", "w&#468;", "w&#232;i", "sh&#275;n", "y&#466;u", 
                "x&#363;", "h&#224;i"]; // earthly branches
        animal = ["Rat","Ox","Tiger","Rabbit","Dragon","Snake","Horse","Goat",
                 "Monkey","Chicken","Dog","Pig"]; // 12 animals
        Wyear = "Western<br />year";
        Cyear = "Chinese<br />year";
        Cmonth = "Months in Chinese Calendar";
        month_num = ["1","2","3","4","5","6","7","8","9","10","11","12","leap<br />mon."];
        Ndays = "# days";
        note_early = "The lunar conjunction is close to the midnight. The start day of the month may be one day earlier.";
        note_late = "The lunar conjunction is close to the midnight. The start day of the month may be one day later.";
    } else {
        // Chinese
        heaven = ["甲","乙","丙","丁", "戊","己","庚","辛","壬","癸"];
        earth = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"];
       //heaven = ["&#x7532;","&#x4E59;","&#x4E19;","&#x4E01;","&#x620A;", "&#x5DF1;","&#x5E9A;","&#x8F9B;","&#x58EC;","&#x7678;"];
        //earth = ["&#x5B50;","&#x4E11;","&#x5BC5;","&#x536F;","&#x8FB0;",  "&#x5DF3;","&#x5348;","&#x672A;","&#x7533;","&#x9149;", "&#x620C;","&#x4EA5;"];
        if (lang==1) {
            animal = ["鼠","牛","虎","兔","龍", "蛇","馬","羊","猴","雞", "狗","豬"];
            Wyear = "公曆年";
            Cyear = "中曆年";
            Cmonth = "中曆月";
            month_num = ["正","二","三","四","五", "六","七","八","九","十", "十一","十二","閏月"];
            Ndays = "日數";
            note_early = "朔的時刻接近午夜零時，初一或會提早一天。";
            note_late = "朔的時刻接近午夜零時，初一或會推遲一天。";
        } else {
            animal = ["鼠","牛","虎","兔","龙", "蛇","马","羊","猴","鸡", "狗","猪"];
            Wyear = "公历年";
            Cyear = "中历年";
            Cmonth = "中历月";
            month_num = ["正","二","三","四","五", "六","七","八","九","十", "十一","十二","闰月"];
            Ndays = "日数";
            note_early = "朔的时刻接近午夜零时，初一或会提早一天。";
            note_late = "朔的时刻接近午夜零时，初一或会推迟一天。";
        }
    }
    return {lang:lang, heaven:heaven, earth:earth, animal:animal, 
            region:'default', Wyear:Wyear, Cyear:Cyear, Cmonth:Cmonth, 
            month_num:month_num, Ndays:Ndays, 
            note_early:note_early, note_late:note_late, li:null};
}

// day from Dec 31, y-1 -> mm-dd (assume day > 0)
function ymd(yIn, dayIn) {
    // 9999 means NA
    if (dayIn==9999) {
        return '&mdash;';
    }
    
    let y = yIn, day = dayIn;
    
    // no Zhongqi marker for ancient calendars
    let noZhong = false;
    if (day > 1000) {
        noZhong = true;
        day -= 5000;
    }
    
    let ndays, yPrevious;
    if (day < 1) {
        yPrevious = true;
        y--;
        ndays = NdaysGregJul(y);
        day += ndays;
    } else {
        yPrevious = false;
        ndays = NdaysGregJul(y);
    }
    
    let leap = (ndays==366 ? 1:0);
    let m,d;
    
    if (day > ndays) {
        m = 13; d = day-ndays;
        if (d > 31) {
            m = 14;
            d -= 31;
        }
    } else {
        let mday = [0, 31, 59+leap, 90+leap, 120+leap, 151+leap, 181+leap, 212+leap,
               243+leap, 273+leap, 304+leap, 334+leap, 365+leap];
        if (y==1582) {
            if (day > 277) { day += 10;}
        }
        for (let i=0; i<13; i++) {
            if (day-mday[i] < 1) {
                m=i; d = day-mday[i-1];
                break;
            }
        }
    }
    
    let mm = "0"+m, dd = "0"+d;
    let mmdd = mm.slice(-2)+'-'+dd.slice(-2);
    if (yPrevious) { mmdd = '-'+mmdd;}
    if (noZhong) { mmdd = '<u>'+mmdd+'</u>';}
    return mmdd;
}

// Create a single table spanning years from ystart to yend.
// date is an 2D array storing the calendar information from 
// years between -105 and 2200.
// Each row contains data for a Chinese year
// columns: year, first date of month yin, mao,... , chou2, 
//          leap month, month # that is leaped, 
//          # of days in the year
// leap month = month # = 0 if no leap month
function tableYears(ystart, yend, date, langCon) {
    let txt = '<table>';
    txt += '<tr><th rowspan="2">'+langCon.Wyear+'</th>';
    txt += '<th rowspan="2" style="min-width:70px;">'+langCon.Cyear+'</th>';
    txt += '<th colspan="13">'+langCon.Cmonth+'</th>';
    txt += '<th rowspan="2">'+langCon.Ndays+'</th></tr>';
    txt += '<tr>';
    let year, y, i, j;
    for (j=0; j<12; j++) {
        txt += '<th style="min-width:60px;">'+langCon.month_num[j]+'</th>';
    }
    txt += '<th style="min-width:60px;">'+langCon.month_num[12]+'</th> </tr>';
    let jd0, jd;
    for (year = ystart; year <= yend; year++) {
        y = date[year - date[0][0]];
        let ih = (year + 6) % 10;
        let ie = (year + 8) % 12;
        if (ih < 0) {ih += 10;}
        if (ie < 0) {ie += 12;}
        let cyear = "";
        if (year < 1912 && langCon.lang > 0) {
            // Use era/regime name
            if (langCon.lang==1) {
                cyear = eraName(year, langCon.region, langCon.li);
            } else {
                cyear = eraNameSim(year, langCon.region, langCon.li);
            }
            if (cyear.length > 2) {
                cyear = cyear.slice(1, cyear.length-1);
                if (langCon.region=='default' && year > 420.5 && year < 589.5) {
                    // remove [南北朝]
                    cyear = cyear.slice(5);
                }
                if (langCon.region=='default' && year > 907.5 && year < 960.5) {
                    // remove [五代]
                    cyear = cyear.slice(4);
                }
            }
        }
        if (cyear == "") {
            // Use sexagenary year cycle
            cyear = langCon.heaven[ih]+" "+langCon.earth[ie]+" ("+langCon.animal[ie]+")";
        }
        txt +='<tr><td>'+year+'</td><td>'+cyear+'</td>';

        // JD at noon on Dec 31, year-1
        jd0 = Math.floor(getJD(year-1, 12,31) + 0.501);
        let mmdd;
        for (j=1; j<13; j++) {
            mmdd = ymd(year,y[j]);
            // Indicate new moon too close to midnight
            let warn = newMoonCloseToMidnight(year, j);
            if (warn==1) {
                mmdd = '<span style="color:red;">'+mmdd+'<sup>*</sup></span>';
            }
            if (langCon.lang > 0 && mmdd != '&mdash;') {
                // add sexagenary day cycle
                jd = jd0 + (y[j] > 1000 ? y[j]-5000:y[j]);
                mmdd += '<br />'+langCon.heaven[(jd-1) % 10]+langCon.earth[(jd+1) % 12];
            }
            txt +='<td>'+mmdd+'</td>';
        }
        let lmon = '&mdash;';
        if (y[13] > 0) {
            // there is a leap month
            mmdd = ymd(year,y[13]);
            lmon = langCon.month_num[y[14]-1]+': '+mmdd;
            if (year < -103) {
                lmon = mmdd;
            }
            if (langCon.lang > 0) {
                // add sexagenary day cycle
                jd = jd0 + (y[13] > 1000 ? y[13]-5000:y[13]);
                lmon += '<br />'+langCon.heaven[(jd-1) % 10]+langCon.earth[(jd+1) % 12];
            }
        }
        txt += '<td>'+lmon+'</td><td>'+y[15]+'</td>';
        txt +='</tr>';
    }
    txt += '</table>';
    txt += printWarningMessage(yend, langCon) + '<br /><br /><br />';
    return txt;
}

// Table for the Spring and Autumn Period (-721 - -480)
function table_spring(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    let langCon = langConstant(lang);
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (722 BCE &ndash; 481 BCE)</h1>';
        tab.innerHTML = '<p>The following table lists the proleptic Julian dates MM-DD of the first day of each month in the Chinese calendar. Julian year 0 means 1 BCE, -1 means 2 BCE and so on. MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. When MM is negative, it means the month in the previous year. For example, -11-27 means November 27th in the previous year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. The last column lists the total number of days in the Chinese year.</p>';
        langCon.Wyear = "Julian<br />year";
    } else if (lang==1) {
        tit.innerHTML = '<h1>春 秋 時 代 朔 閏 表 (前722 &ndash; 前481)</h1>';
        tab.innerHTML = '<p>下表列出農曆每月初一的公曆日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、餘類推。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月，負數的MM表示上一個公曆年的月份，例如 -11-27 表示上一年的11月27日。閏月欄裡 &mdash; 表示該農曆年沒有閏月，MM-DD 表示閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
    } else {
        tit.innerHTML = '<h1>春 秋 时 代 朔 闰 表 (前722 &ndash; 前481)</h1>';
        tab.innerHTML = '<p>下表列出农历每月初一的公历日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、余类推。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月，负数的MM表示上一个公历年的月份，例如 -11-27 表示上一年的11月27日。闰月栏里 &mdash; 表示该农历年没有闰月，MM-DD 表示闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
    }
    
    let menu = ancient_calendar_menu('Spring');
    let i, j, li, y, liDisplay;
    for (i=0; i<menu.length; i++) {
      if (document.getElementById(menu[i].id).classList.contains('active')) {
         li = menu[i].li;
         liDisplay = (lang==0 ? menu[i].li:menu[i].lic);
         if (lang==2) { liDisplay = menu[i].lis;}
         if (liDisplay=="Xia1" || liDisplay=="Xia2") { liDisplay ="Xia";}
         document.getElementById("calshownSpring").innerHTML = liDisplay;
         document.getElementById("SpringliDescription").innerHTML = ancient_calendar_description("SpringTable", menu[i].li, menu[i].lic, menu[i].lis, lang);
         break;
      }
    }
    
    // set up 2D array
    let date = new Array(242);
    for (i=0; i<242; i++) {
        date[i] = new Array(16);
        y = i-721;
        // Julian date number at noon on Dec 31, y-1 
        let accleap = Math.floor(0.25*(y + 799) + 1e-5);
        let jdc = 1429223 + accleap + 365*(y+799);
        let cm;
        if (li=="Chunqiu") {
            cm = chunqiu_cmonth(y, jdc);
            cm.noZhong = -1;
        } else {
            cm = guliuli_calendar_cmonth(li, y, jdc);
        }
        let leap = (cm.cmonthDate.length==12 ? 0:1);
        
        date[i][0] = y;
        for (j=1; j<13+leap; j++) {
            date[i][j] = cm.cmonthDate[j-1];
            if (cm.noZhong==j-1) { date[i][j] += 5000;}
        }
        if (leap==0) { 
            date[i][13]=0; 
            date[i][14]=0;
        } else {
            date[i][14] = 12;
        }
        date[i][15] = cm.cndays;
    }
    
    let txt = tableYears(-721, -710, date, langCon);
    for (y=-709; y <= -489; y += 10) {
        txt += tableYears(y, y+9, date, langCon);
    }
    document.getElementById('table').innerHTML = txt;
    // *** TEST ***
    //let csv = generate_csv(-721, -480, date);
    //download_csv(csv, 'test.csv');
    date = null;
}

// Table for the Warring Sattes Period (-479 - -221)
function table_warring(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    let langCon = langConstant(lang);
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (480 BCE &ndash; 222 BCE)</h1>';
        tab.innerHTML = '<p>The following table lists the proleptic Julian dates MM-DD of the first day of each month in the Chinese calendar. Julian year 0 means 1 BCE, -1 means 2 BCE and so on. MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. When MM is negative, it means the month in the previous year. For example, -11-27 means November 27th in the previous year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. The last column lists the total number of days in the Chinese year.</p>';
        langCon.Wyear = "Julian<br />year";
    } else if (lang==1) {
        tit.innerHTML = '<h1>戰 國 時 代 朔 閏 表 (前480 &ndash; 前222)</h1>';
        tab.innerHTML = '<p>下表列出農曆每月初一的公曆日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、餘類推。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月，負數的MM表示上一個公曆年的月份，例如 -11-27 表示上一年的11月27日。閏月欄裡 &mdash; 表示該農曆年沒有閏月，MM-DD 表示閏月初一的公曆月日。公曆日期的下面是日干支。日數指該農曆年的總日數。</p>';
    } else {
        tit.innerHTML = '<h1>战 国 时 代 朔 闰 表 (前480 &ndash; 前222)</h1>';
        tab.innerHTML = '<p>下表列出农历每月初一的公历日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、余类推。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月，负数的MM表示上一个公历年的月份，例如 -11-27 表示上一年的11月27日。闰月栏里 &mdash; 表示该农历年没有闰月，MM-DD 表示闰月初一的公历月日。公历日期的下面是日干支。日数指该农历年的总日数。</p>';
    }
    
    let menu = ancient_calendar_menu('Warring');
    let i, j, li, y, liDisplay;
    for (i=0; i<menu.length; i++) {
      if (document.getElementById(menu[i].id).classList.contains('active')) {
         li = menu[i].li;
         liDisplay = (lang==0 ? menu[i].li:menu[i].lic);
         if (lang==2) { liDisplay = menu[i].lis;}
         if (liDisplay=="Xia1" || liDisplay=="Xia2") { liDisplay ="Xia";}
         document.getElementById("calshownWarring").innerHTML = liDisplay;
         document.getElementById("guliuliDescription").innerHTML = ancient_calendar_description("WarringTable", menu[i].li, menu[i].lic, menu[i].lis, lang);
         break;
      }
    }
    
    if (li=="Zhuanxu") {
        if (lang==0) {
           langCon.month_num = ["10","11","12","1","2","3","4","5","6","7","8","9","post<br />9"]; 
        } else if (lang==1) {
           langCon.month_num = ['十', '十一', '十二', '正', '二', '三', '四', '五', '六', '七', '八', '九', '後九'];
        } else {
           langCon.month_num = ['十', '十一', '十二', '正', '二', '三', '四', '五', '六', '七', '八', '九', '后九'];
        }
    }
    
    // set up 2D array
    let date = new Array(259);
    for (i=0; i<259; i++) {
        date[i] = new Array(16);
        y = i-479;
        // Julian date number at noon on Dec 31, y-1 
        let accleap = Math.floor(0.25*(y + 799) + 1e-5);
        let jdc = 1429223 + accleap + 365*(y+799);
        let cm = guliuli_calendar_cmonth(li, y, jdc);
        let leap = (cm.cmonthDate.length==12 ? 0:1);
        
        date[i][0] = y;
        for (j=1; j<13+leap; j++) {
            date[i][j] = cm.cmonthDate[j-1];
            if (cm.noZhong==j-1) { date[i][j] += 5000;}
        }
        if (leap==0) { 
            date[i][13]=0; 
            date[i][14]=0;
        } else {
            date[i][14] = (li=="Zhuanxu" ? 9:12);
        }
        date[i][15] = cm.cndays;
    }
    
    tab = '';
    for (y=-479; y <= -230; y += 10) {
        tab += tableYears(y, y+9, date, langCon);
    }
    tab += tableYears(-229, -221, date, langCon);
    document.getElementById('table').innerHTML = tab;
    // *** TEST ***
    //let csv = generate_csv(-479, -221, date);
    //download_csv(csv, 'test.csv');
    date = null;
}

// Table for Qin, Han and Xin (-220 - 24)
function table_qinhanxin(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (221 BCE &ndash; 24 CE)</h1>';
        tab.innerHTML = '<p>The following table lists the (proleptic before 8 CE) Julian dates MM-DD of the first day of each month in the Chinese calendar in the Qin, Western Han, and Xin dynasty (221 BCE &ndash; 24 CE). Julian year 0 means 1 BCE, -1 means 2 BCE and so on. MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. When MM is negative, it means the month in the previous year. For example, -11-27 means November 27th in the previous year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p><br />';
    } else if (lang==1) {
        tit.innerHTML = '<h1>秦、 西 漢 及 新 朝 朔 閏 表 (前221 &ndash; 24)</h1>';
        tab.innerHTML = '<p>下表列出秦、西漢、新朝時(前221年至24年)農曆每月初一的公曆日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、餘類推。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月，負數的MM表示上一個公曆年的月份，例如 -11-27 表示上一年的11月27日。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p><br />';
    } else {
        tit.innerHTML = '<h1>秦、 西 汉 及 新 朝 朔 闰 表 (前221 &ndash; 24)</h1>';
        tab.innerHTML = '<p>下表列出秦、西汉、新朝时(前221年至24年)农历每月初一的公历日期 MM-DD。公元0年即公元前1年、-1年即前2年、-2年即前3年、余类推。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月，负数的MM表示上一个公历年的月份，例如 -11-27 表示上一年的11月27日。公历日期的下面是日干支。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。 日数指该农历年的总日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p><br />';
    }
    
    let langCon = langConstant(lang);
    
    let info;
    if (lang==0) {
        info = '<p style="color:brown;">The calendar used between 221 BCE and 104 BCE largely followed the convention used by the Zhuanxu calendar, one of the old calendars used in the third century BCE in the state of Qin. The first month was the h&#224;i month (present day month 10). However, it was still called month 10 instead of month 1. The numerical order of the months in a year was 10, 11, 12, 1, 2, ..., 9. The intercalary month was placed at the end of a year, called post month 9. There was a major calendar reform in 104 BCE, where the first month of a year was changed to month 1 and the intercalary month was placed in the month that did not contain a major solar term. The Chinese year in 104 BCE had 15 Chinese months as a result of the change.</p> <p style="color:brown;">The calendars in this period are reconstructed according to the description in the article "Researches on Calendars from Qin to early Han (246 B.C. to 104 B.C.) &mdash; centering on excavated calendrical bamboo slips" (秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心), L&#464; Zh&#333;ngl&#237;n (李忠林), in <i>Studies in Chinese History</i> (《中国史研究》), issue no. 2, pp. 17&ndash;69 (2012). Our computation method is explained on <a href="QinHanCalendars.html">this page</a>.</p>';
        langCon.Wyear = "Julian<br />year";
        langCon.month_num = ["10","11","12","1","2","3","4","5","6","7","8","9","post<br />9"];
    } else if (lang==1) {
        info = '<p style="color:brown;">秦朝及漢初(公元前221年 &ndash; 前104年)的曆法沿用顓頊曆的月序。顓頊曆是古六曆之一，據說戰國後期在秦國使用。顓頊曆以建亥(即今天的十月)為年首，但仍稱建丑為十月。月的數序是十月、十一月、十二月、正月、二月……九月，閏月置於年終，稱為後九月。秦朝的曆法與顓頊曆稍有不同。漢朝建立後基本上沿用秦曆，一百年間只作了少許修改，直到漢武帝太初元年(公元前104年)才頒行新曆法，以建寅(正月)為年首，並把閏月置於無中氣的月份，這使公元前104年的農曆年有十五個農曆月。秦朝為了避秦始皇名諱(正、政同音)，把正月改稱「端月」，到漢朝又改回正月。這裡沒有跟從歷史，在秦朝仍稱建寅為正月。</p> <p style="color:brown;">本網頁這時期的復原日曆是根據李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，發表於《中国史研究》2012年第2期第17&ndash;69頁。具體計算方法在<a href="QinHanCalendars_chinese.html">秦與漢初曆法網頁</a>闡述。</p>';
        langCon.month_num = ['十', '十一', '十二', '正', '二', '三', '四', '五', '六', '七', '八', '九', '後九'];
    } else {
        info = '<p style="color:brown;">秦朝及汉初(公元前221年 &ndash; 前104年)的历法沿用颛顼历的月序。颛顼历是古六历之一，据说战国後期在秦国使用。颛顼历以建亥(即今天的十月)为年首，但仍称建丑为十月。月的数序是十月丶十一月丶十二月丶正月丶二月……九月，闰月置於年终，称为后九月。秦朝的历法与颛顼历稍有不同。汉朝建立後基本上沿用秦历，一百年间只作了少许修改，直到汉武帝太初元年(公元前104年)才颁行新历法，以建寅(正月)为年首，并把闰月置於无中气的月份，这使公元前104年的农历年有十五个农历月。秦朝为了避秦始皇名讳(正丶政同音)，把正月改称「端月」，到汉朝又改回正月。这里没有跟从历史，在秦朝仍称建寅为正月。</p> <p style="color:brown;">本网页这时期的复原日历是根据李忠林的文章「秦至汉初(前246至前104)历法研究&mdash;以出土历简为中心」，发表於《中国史研究》2012年第2期第17&ndash;69页。具体计算方法在<a href="QinHanCalendars_simp.html">秦与汉初历法网页</a>阐述。</p>';
        langCon.month_num = ['十', '十一', '十二', '正', '二', '三', '四', '五', '六', '七', '八', '九', '后九'];
    }
    tab = info;
    
    // setup 2D array for -220 - -104
    let date = new Array(117);
    let i, j, y, jdc;
    for (y=-220; y <= -104; y++) {
        i = y + 220;
        date[i] = new Array(16);
        // Julian date number at noon on Dec 31, y-1 
        let accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        let cm = HanZhuanXu(y,jdc);
        date[i][0] = y;
        for (j=1; j<14; j++) {
            date[i][j] = cm.cmonthDate[j-1];
            if (cm.noZhong==j-1) { date[i][j] += 5000;}
        }
        date[i][14] = (date[i][13]==0 ? 0:9);
        date[i][15] = cm.cndays;
    }
    
    tab += tableYears(-220, -210, date, langCon);
    for (y=-209; y<=-119; y += 10) {
        tab += tableYears(y, y+9, date, langCon);
    }
    tab += tableYears(-109, -104, date, langCon);
    // *** TEST ***
    //let csv = generate_csv(-220, -104, date);
    //download_csv(csv, 'test1.csv');
    date = null;
    
    // Manually create the table for -103
    if (lang==0) {
        info = '<p style="color:red;">The calendar reform in 104 BCE (-103) caused that year having 15 Chinese months.</p>'
        info += '<table>';
        info += '<tr> <th rowspan="2">Julian<br />year</th> <th rowspan="2">Chinese<br />year</th> <th colspan="8">Months in Chinese Calendar</th></tr>';
        info += '<tr> <th>10</th> <th>11</th> <th>12</th> <th>1</th> <th>2</th> <th>3</th> <th>4</th> <th>5</th></tr>';
        info += '<tr> <td rowspan="3">-103</td> <td rowspan="3">D&#299;ng ch&#466;u; (Ox)</td> <td>-11-26</td> <td>-12-25</td> <td>01-24</td> <td>02-22</td> <td>03-24</td> <td>04-23</td> <td>05-22</td> <td>06-20</td></tr>';
        info += '<tr> <th>6</th> <th>7</th> <th>8</th> <th>9</th> <th>10</th> <th>11</th> <th>12</th> <th># days</th></tr>';
        info += '<tr><td>07-19</td> <td>08-18</td> <td>09-16</td> <td>10-16</td> <td>11-14</td> <td>12-14</td> <td>13-12</td> <td>442</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["1","2","3","4","5","6","7","8","9","10","11","12","leap<br />mon."];
    } else if (lang==1) {
        info = '<p style="color:red;">太初元年(-103年)的曆改使該年有十五個農曆月。</p>';
        info += '<table>';
        info += '<tr> <th rowspan="2">公曆年</th> <th rowspan="2">中曆年</th> <th colspan="8">中曆月</th></tr>';
        info += '<tr> <th>十</th> <th>十一</th> <th>十二</th> <th>正</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th></tr>';
        info += '<tr> <td rowspan="3">-103</td> <td rowspan="3">漢武帝太初元年</td> <td>-11-26<br />乙未</td> <td>-12-25<br />甲子</td> <td>01-24<br />甲午</td> <td>02-22<br />癸亥</td> <td>03-24<br />癸巳</td> <td>04-23<br />癸亥</td> <td>05-22<br />壬辰</td> <td>06-20<br />辛酉</td></tr>';
        info += '<tr> <th>六</th> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>日數</th></tr>';
        info += '<tr><td>07-19<br />庚寅</td> <td>08-18<br />庚申</td> <td>09-16<br />己丑</td> <td>10-16<br />己未</td> <td>11-14<br />戊子</td> <td>12-14<br />戊午</td> <td>13-12<br />丁亥</td> <td>442</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "閏月"];
    } else {
        info = '<p style="color:red;">太初元年(-103年)的历改使该年有十五个农历月。</p>';
        info += '<table>';
        info += '<tr> <th rowspan="2">公历年</th> <th rowspan="2">中历年</th> <th colspan="8">中历月</th></tr>';
        info += '<tr> <th>十</th> <th>十一</th> <th>十二</th> <th>正</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th></tr>';
        info += '<tr> <td rowspan="3">-103</td> <td rowspan="3">汉武帝太初元年</td> <td>-11-26<br />乙未</td> <td>-12-25<br />甲子</td> <td>01-24<br />甲午</td> <td>02-22<br />癸亥</td> <td>03-24<br />癸巳</td> <td>04-23<br />癸亥</td> <td>05-22<br />壬辰</td> <td>06-20<br />辛酉</td></tr>';
        info += '<tr> <th>六</th> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>日数</th></tr>';
        info += '<tr><td>07-19<br />庚寅</td> <td>08-18<br />庚申</td> <td>09-16<br />己丑</td> <td>10-16<br />己未</td> <td>11-14<br />戊子</td> <td>12-14<br />戊午</td> <td>13-12<br />丁亥</td> <td>442</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "闰月"];
    }
    tab += info;        
    
    date = ChineseToGregorian();
    tab += tableYears(-102, -90, date, langCon);
    for (y=-89; y <= -9; y += 10) {
       tab += tableYears(y, y+9, date, langCon);
    }
    
    // Create 2D array for years 1 - 23
    let date2 = new Array(23);
    let y0 = date[0][0];
    for (y=1; y <=8; y++) {
        date2[y-1] = new Array(16);
        j = y - y0;
        for (i=0; i<16; i++) {
            date2[y-1][i] = date[j][i];
        }
    }
    // Remove month 12 in year 8 by setting it to 9999, 
    // which ymd() function will interpret as NA
    // The number of days in year 8 is 354
    date2[7][12] = 9999; date2[7][15] = 354;
    for (y = 9; y <= 23; y++) {
        date2[y-1] = new Array(16);
        j = y - y0;
        let ndays1 = NdaysGregJul(y-1);
        date2[y-1][0] = y;
        date2[y-1][1] = date[j-1][12] - ndays1;
        for (i=2; i<13; i++) {
            date2[y-1][i] = date[j][i-1];
        }
        date2[y-1][13] = date[j][13];
        date2[y-1][14] = (date[j][14] > 0 ? date[j][14] + 1:0);
        date2[y-1][15] = date[j][12] - date2[y-1][1];
        if (date2[y-2][14]==13) {
            // leap 12 -> leap 1
            date2[y-1][14] = 1;
            date2[y-1][13] = date2[y-2][13] - NdaysGregJul(y-1);
            date2[y-2][13] = 0;
            date2[y-2][14] = 0;
        }
    }
    if (date2[21][14]==13) {
        date2[21][14]=0; date2[21][13]=0; 
    }
    
    tab += tableYears(1, 8, date2, langCon);
    if (lang==0) {
        info = '<p style="color:red;">The Xin dynasty was established in 9 CE The ch&#466;u month (present day month 12) was desnigated as the first month of a year; the y&#237;n month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. As a result, the Chinese year in 8 CE (W&#249; ch&#233;n) had only 11 months. The Xin dynasty was overthrown in 23 CE and the Han dynasty was restored. The month numbers were then switched back with month 1 being the y&#237;n month again. As a result, the Chinese year in 23 CE had two sets of calendar: one for the Xin dynasty (ch&#466;u month being the first month) and the other for the Han dynasty (y&#237;n month being the first month).</p>';
    } else if (lang==1) {
        info = '<p style="color:red;">公元9年，王莽建立新朝，改正朔以殷正建丑(即現在的十二月)為年首，故公元8年的中曆年(戊辰年)只有十一個月。中曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。新朝於地皇四年(癸未年，公元23年)亡，綠林軍擁立漢淮南王劉玄为帝，改元更始元年，恢復以建寅(即現在的正月)為年首。</p>';
    } else {
        info = '<p style="color:red;">公元9年，王莽建立新朝，改正朔以殷正建丑(即现在的十二月)为年首，故公元8年的农历年(戊辰年)只有十一个月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。新朝于地皇四年(癸未年，公元23年)亡，绿林军拥立汉淮南王刘玄为帝，改元更始元年，恢复以建寅(即现在的正月)为年首。</p>';
    }
    tab += info;
    langCon.month_num[0] = (lang==0 ? "1 (ch&#466;u)":"正(丑)");
    let txt = tableYears(9, 23, date2, langCon);
    if (lang==1) {
        txt = txt.replace('/漢更始元年', '');
    } else if (lang==2) {
        txt = txt.replace('/汉更始元年', '');
    }
    tab += txt;

    if (lang==0) {
        info = '<h3>Gengshi (23 &ndash; 25)</h3>';
    } else {
        info = '<h3>更 始 (23 &ndash; 25)</h3>';
    }
    tab += info;

    langCon.month_num[0] = (lang==0 ? "1":"正");
    txt = tableYears(23, 25, date, langCon);
    if (lang != 0) {
        txt = txt.replace('新地皇四年/', '');
    }
    tab += txt;
    
    document.getElementById('table').innerHTML = tab;
    date = null;
    date2 = null;
}

// Table for Eastern Han (25 - 219)
function table_easternhan(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (25 &ndash; 219)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Eastern Han dynasty (25&ndash;219). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>東 漢 朔 閏 表 (25 &ndash; 219)</h1>';
        tab.innerHTML = '<p>下表列出東漢時(25年至219年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>东 汉 朔 闰 表 (25 &ndash; 219)</h1>';
        tab.innerHTML = '<p>下表列出东汉时(25年至219年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。 公历日期的下面是日干支。日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(25, 30, date, langCon);
    
    for (let ystart=31; ystart <= 201; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(211, 219, date, langCon);
    document.getElementById('table').innerHTML = tab;
    date = null;
}

// Table for Wei, Shu and Wu dynasties (220 - 280)
function table_weishuwu(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (220 &ndash; 280)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Wei, Shu and Wu dynasties (220&ndash;280). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. When MM is negative, it means the month in the previous year. For example, -11-27 means November 27th in the previous year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>魏 蜀 吳 朔 閏 表 (220 &ndash; 280)</h1>';
        tab.innerHTML = '<p>下表列出魏蜀吳(220年至280年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月，負數的MM表示上一個公曆年的月份，例如 -11-27 表示上一年的11月27日。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>魏 蜀 吴 朔 闰 表 (220 &ndash; 280)</h1>';
        tab.innerHTML = '<p>下表列出魏蜀吴(220年至280年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月，负数的MM表示上一个公历年的月份，例如 -11-27 表示上一年的11月27日。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。 公历日期的下面是日干支。日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    let info, txt = '<br />';
    if (lang==0) {
        txt += '<h2>Wei (220-265)</h2> <br />';
    } else {
        txt += '<h2>魏 (220-265)</h2> <br />';
    }
    tab = txt;
    tab += tableYears(220, 229, date, langCon);
    
    // Set up 2D array date2 for the years 230-238
    let y, date2 = new Array(9);
    let y0 = date[0][0];
    let i,j,k;
    for (y=230; y<=236; y++) {
        j = y-230;
        date2[j] = new Array(16);
        for (i=0; i<16; i++) {
            date2[j][i] = date[y-y0][i];
        }
    }
    j = 237 - y0;
    date2[7] = new Array(16); 
    date2[8] = new Array(16);
    for (i=0; i<15; i++) {
        if (i > 3 && i < 13) {
            date2[7][i] = date[j][i-1];
        } else {
            date2[7][i] = date[j][i];
        }
    }
    // remove month 3 from the year 237 by 
    // seting the to 9999, a number the function ymd() 
    // recongnizes as NA. 
    // Number of days in N_{237} is 325
    date2[7][3] = 9999;
    date2[7][15] = 325;
    
    j = 238 - y0;
    let ndays1 = NdaysGregJul(237);
    date2[8][0] = 238;
    date2[8][1] = date[j-1][12] - ndays1;
    for (i=2; i<13; i++) {
        date2[8][i] = date[j][i-1];
    }
    date2[8][13] = date[j][13];
    date2[8][14] = date[j][14] + 1;
    date2[8][15] = date[j][12] - date2[8][1];
    tab += tableYears(230, 236, date2, langCon);
    
    if (lang==0) {
        info = '<p style="color:red;">In 237 CE, emperor Mingdi of the Wei dynasty declared that the ch&#466;u month (present day month 12) would be the first month of a year; the y&#237;n month (present day month 1) became month 2 and so on. The Chinese month numbers were shifted by one. The new system was imposed after month 2 in the Chinese year in 237, in which month 4 was followed by month 2. When the emperor died in 239 CE, the month numbers were switched back with month 1 being the y&#237;n month again in the following year. As a result, the Chinese year in 239 had 13 months, where month 12 appeared twice (z&#464; month and ch&#466;u month). In addition, month 12 in the Chinese year in 236 CE had only 28 days as a new version of the Chinese calendar was adopted. There are discrepancies between the data in the main text and Appendix 2 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. The main text uses the new calendar in month 1, but Appendix 2 uses the new calendar in month 6. Here the data in the main text are used, in which the first days of each month before month 6 are one day earlier.</p>';
        langCon.month_num[0] = '1 (y&#237;n)';
        langCon.month_num[1] = '2 (m&#462;o)';
        langCon.month_num[3] = '4 (ch&#233;n)';
    } else  {
        if (lang==1) {
            info = '<p style="color:red;">魏青龍五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即現在的十二月)為年首，二月後實施，並改元景初元年。所以丁巳年沒有三月份，二月後的月份是四月。農曆月的數序是:建丑為正月、建寅為二月等等，與現在通用的月序相差一個月。景初三年（公元239年）明帝駕崩,次年恢復以建寅(即現在的正月)為年首。景初三年有兩個十二月(建子和建丑)。另外，青龍五年正月開始使用新曆法(景初曆)，使青龍四年十二月只有二十八日。《三千五百年历日天象》的正文與其附表2的資料不合，正文在正月改用景初曆，附表2在六月才改曆。這裡用正文的數據，在六月前的朔日都比附表2早一日。</p>';
        } else {
            info = '<p style="color:red;">魏青龙五年（丁巳年，公元237年），魏明帝改正朔，以殷正建丑(即现在的十二月)为年首，二月后实施，并改元景初元年。所以丁巳年没有三月份，二月后的月份是四月。农历月的数序是:建丑为正月、建寅为二月等等，与现在通用的月序相差一个月。景初三年（公元239年）明帝驾崩,次年恢复以建寅(即现在的正月)为年首。景初三年有两个十二月(建子和建丑)。另外，青龙五年正月开始使用新历法(景初历)，使青龙四年十二月只有二十八日。《三千五百年历日天象》的正文与其附表2的资料不合，正文在正月改用景初历，附表2在六月才改历。这里用正文的数据，在六月前的朔日都比附表2早一日。</p>';
        }
        langCon.month_num[0] = '正(寅)';
        langCon.month_num[1] = '二(卯)';
        langCon.month_num[3] = '四(辰)';
    }
    tab += info;
    tab += tableYears(237,237, date2, langCon);
    if (lang==0) {
        langCon.month_num[0] = '1 (ch&#466;u)';
        langCon.month_num[1] = '2';
        langCon.month_num[3] = '4';
        langCon.month_num[11] = '12';
    } else {
        langCon.month_num[0] = '正(丑)';
        langCon.month_num[1] = '二';
        langCon.month_num[3] = '四';
        langCon.month_num[11] = '十二';
    }
    tab += tableYears(238,238, date2, langCon);
    
    // Manually create the table for 239
    if (lang==0) {
        info = '<table>';
        info += '<tr> <th rowspan="2">Julian<br />year</th> <th rowspan="2">Chinese<br />year</th> <th colspan="7">Months in Chinese Calendar</th> <th rowspan="4"># days</th></tr>';
        info += '<tr> <th>1 (ch&#466;u)</th> <th>2</th> <th>3</th> <th>4</th> <th>5</th> <th>6</th> <th>7</th>';
        info += '<tr> <td rowspan="3">239</td> <td rowspan="3">J&#464; w&#232;i (Goat)</td> <td>01-22</td> <td>02-21</td> <td>03-22</td> <td>04-21</td> <td>05-20</td> <td>06-19</td> <td>07-18</td> </tr>';
        info += '<tr> <th>8</th> <th>9</th> <th>10</th> <th>11</th> <th>12 (z&#464;)</th> <th>12 (ch&#466;u)</th> <th>leap<br />mon.</th> </tr>';
        info += '<tr><td>08-17</td> <td>09-15</td> <td>10-15</td> <td>11-13</td> <td>12-13</td> <td>13-12</td> <td>&mdash;</td> <td>384</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num[0] = '1';
    } else if (lang==1) {
        info = '<table>';
        info += '<tr> <th rowspan="2">公曆年</th> <th rowspan="2">中曆年</th> <th colspan="7">中曆月</th> <th rowspan="4">日數</th></tr>';
        info += '<tr> <th>正(丑)</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th> <th>六</th> <th>七</th></tr>';
        info += '<tr> <td rowspan="3">239</td> <td rowspan="3">魏明帝景初三年</td> <td>01-22<br />丁亥</td> <td>02-21<br />丁巳</td> <td>03-22<br />丙戌</td> <td>04-21<br />丙辰</td> <td>05-20<br />乙酉</td> <td>06-19<br />乙卯</td> <td>07-18<br />甲申</td></tr>';
        info += '<tr> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二(子)</th> <th>十二(丑)</th> <th>閏月</th> </tr>';
        info += '<tr><td>08-17<br />甲寅</td> <td>09-15<br />癸未</td> <td>10-15<br />癸丑</td> <td>11-13<br />壬午</td> <td>12-13<br />壬子</td> <td>13-12<br />壬午</td> <td>&mdash;</td> <td>384</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num[0] = '正';
    } else {
        info = '<table>';
        info += '<tr> <th rowspan="2">公历年</th> <th rowspan="2">中历年</th> <th colspan="7">中历月</th> <th rowspan="4">日数</th></tr>';
        info += '<tr> <th>正(丑)</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th> <th>六</th> <th>七</th></tr>';
        info += '<tr> <td rowspan="3">239</td> <td rowspan="3">魏明帝景初三年</td> <td>01-22<br />丁亥</td> <td>02-21<br />丁巳</td> <td>03-22<br />丙戌</td> <td>04-21<br />丙辰</td> <td>05-20<br />乙酉</td> <td>06-19<br />乙卯</td> <td>07-18<br />甲申</td></tr>';
        info += '<tr> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二(子)</th> <th>十二(丑)</th> <th>闰月</th> </tr>';
        info += '<tr><td>08-17<br />甲寅</td> <td>09-15<br />癸未</td> <td>10-15<br />癸丑</td> <td>11-13<br />壬午</td> <td>12-13<br />壬子</td> <td>13-12<br />壬午</td> <td>&mdash;</td> <td>384</td></tr>';
        langCon.month_num[0] = '正';
    }
    tab += info;
    
    tab += tableYears(240, 250, date, langCon);
    tab += tableYears(251, 260, date, langCon);
    tab += tableYears(261, 265, date, langCon);
    date = null;
    date2 = null;
    
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Shu (221-263)</h2> <br />';
    } else {
        txt += '<h2>蜀 (221-263)</h2> <br />';
    }
    tab += txt;
    langCon.region ='Shu';
    
    let accleap, jdc, cm, ystart;
    // create 2D array to store the Shu calendar data
    let date3 = new Array(43);
    for (i=0; i<43; i++) {
        y = i + 221;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date3[i] = new Array(16);
        date3[i][0] = y;
        cm = cmonthDate_Shu(y, jdc, false);
        for (j=0; j<15; j++) {
            date3[i][j+1] = cm[j];
        }
    }
    for (ystart=221; ystart <= 251; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date3, langCon);
    }
    tab += tableYears(261, 263, date3, langCon);
    date3 = null;
    
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Wu (222-280)</h2> <br />';
    } else if (lang==1) {
        txt += '<h2>吳 (222-280)</h2> <br />';
    } else {
        txt += '<h2>吴 (222-280)</h2> <br />';
    }
    tab += txt;
    langCon.region ='Wu';
    
    // create 2D array to store the Shu calendar data
    let date4 = new Array(59);
    for (i=0; i<59; i++) {
        y = i + 222;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date4[i] = new Array(16);
        date4[i][0] = y;
        cm = cmonthDate_Wu(y, jdc, false);
        for (j=0; j<15; j++) {
            date4[i][j+1] = cm[j];
        }
    }
    tab += tableYears(222, 230, date4, langCon);
    for (ystart=231; ystart <= 271; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date4, langCon);
    }
    date4 = null;
    
    txt = '';
    if (lang==0) {
        txt +='<h2><a href="ThreeKingdoms_calendars.html">Calendar Differences in this period</a></h2>';
    } else if (lang==1) {
        txt +='<h2><a href="ThreeKingdoms_calendars_chinese.html">魏 蜀 吳 朔 閏 異 同 表</a></h2>';
    } else {
        txt +='<h2><a href="ThreeKingdoms_calendars_simp.html">魏 蜀 吴 朔 闰 异 同 表</a></h2>';
    }
    txt += '<br /><br />';
    tab += txt;
    document.getElementById('table').innerHTML = tab;
}

// Table for Jin dynasty (220 - 419)
function table_jin(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (265 &ndash; 419)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Jin dynasty (265&ndash;419). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>晉 朝 朔 閏 表 (265 &ndash; 419)</h1>';
        tab.innerHTML = '<p>下表列出晉朝時(265年至419年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>晋 朝 朔 闰 表 (265 &ndash; 419)</h1>';
        tab.innerHTML = '<p>下表列出晋朝时(265年至419年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。 公历日期的下面是日干支。日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(265, 270, date, langCon);
    
    for (let ystart=271; ystart <= 401; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(411, 419, date, langCon);
    date = null;
    document.getElementById('table').innerHTML = tab;
}

// Table for Later Qin, Northern Liang, Northern Wei, 
// Eastern Wei, Western Wei, Northern Qi and Northern Zhou (398-580)
function table_snweiqizhou(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (384 &ndash; 580)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the north states between 384 and 580.  MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>後 秦、 北 涼、北 魏、 東 魏、 西 魏、 北 齊、 北 周 朔 閏 表 (384 &ndash; 580)</h1>';
        tab.innerHTML = '<p>下表列出後秦、北涼和南北朝時北魏﹑東魏﹑西魏﹑北齊﹑北周(384年至580年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>后 秦、 北 凉、北 魏、 东 魏、 西 魏、 北 齐、 北 周 朔 闰 表 (398 &ndash; 580)</h1>';
        tab.innerHTML = '<p>下表列出后秦、北凉和南北朝时北魏、东魏、西魏、北齐、北周(398年至580年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    
    let info, txt = '<br />';
    langCon.region = 'LaterQin';
    if (lang==0) {
        txt += '<h2>Later Qin (384-417)</h2> <br />';
    } else if (lang==1) {
        txt += '<h2>後 秦 (384-417)</h2> <br />';
    } else {
        txt += '<h2>后 秦 (384-417)</h2> <br />';
    }
    tab = txt;
    let date4 = new Array(34);
    let i,j,y, ystart, accleap, jdc, cm;
    for(i=0; i<34; i++) {
        y = i+384;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date4[i] = new Array(16);
        date4[i][0] = y;
        cm = cmonthDate_LaterQin(y, jdc, false);
        for (j=0; j<15; j++) {
            date4[i][j+1] = cm[j];
        }
    }
    tab += tableYears(384, 390, date4, langCon);
    tab += tableYears(391, 400, date4, langCon);
    tab += tableYears(401, 410, date4, langCon);
    tab += tableYears(411, 417, date4, langCon);
    date4 = null;
    
    langCon.region = 'NorthernLiang';
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Northern Liang (412-439)</h2>';
        txt += "<p>Northern Liang was established in 397, but it didn't have its own calendar until 412.</p><br />";
    } else if (lang==1) {
        txt += '<h2>北 涼 (412-439)</h2>';
        txt += '<p>北涼在神璽元年(公元397年)立國，初時沒有自己的曆法，到玄始元年(412年)始用太史趙𢾺著的《玄始曆》。</p><br />';
    } else {
        txt += '<h2>北 凉 (412-439)</h2>';
        txt += '<p>北凉在神玺元年(公元397年)立国，初时没有自己的历法，到玄始元年(412年)始用太史赵𢾺著的《玄始历》。</p><br />';
    }
    tab += txt;
    
    let date5 = new Array(28);
    for (i=0; i<28; i++) {
        y = i + 412;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date5[i] = new Array(16);
        date5[i][0] = y;
        cm = cmonthDate_NorthernLiang(y, jdc, false);
        for (j=0; j<15; j++) {
            date5[i][j+1] = cm[j];
        }
    }
    tab += tableYears(412, 420, date5, langCon);
    tab += tableYears(421, 430, date5, langCon);
    tab += tableYears(431, 439, date5, langCon);
    date5 = null;
    
    langCon.region = 'WeiZhouSui';
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Northern Wei (398-534)</h2><br />';
    } else if (lang==1) {
        txt += '<h2>北 魏 (398-534)</h2><br />';
    } else {
        txt += '<h2>北 魏 (398-534)</h2><br />';
    }
    tab += txt;
    
    let date1 = new Array(137);
    for (i=0; i<137; i++) {
        y = i + 398;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date1[i] = new Array(16);
        date1[i][0] = y;
        cm = cmonthDate_WeiZhouSui(y, jdc, false);
        for (j=0; j<15; j++) {
            date1[i][j+1] = cm[j];
        }
    }
    tab += tableYears(398, 410, date1, langCon);
    for (let ystart=411; ystart <= 521; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date1, langCon);
    }
    tab += tableYears(531, 534, date1, langCon);
    date1 = null;
    
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Eastern Wei (534-550)</h2> <br />';
    } else if (lang==1) {
        txt += '<h2>東 魏 (534-550)</h2> <br />';
    } else {
        txt += '<h2>东 魏 (534-550)</h2> <br />';
    }
    tab += txt;
    langCon.region = 'WeiQi';
    let date2 = new Array(44);
    for (i=0; i<44; i++) {
        y = i + 534;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date2[i] = new Array(16);
        date2[i][0] = y;
        cm = cmonthDate_WeiQi(y, jdc, false);
        for (j=0; j<15; j++) {
            date2[i][j+1] = cm[j];
        }
    }
    tab += tableYears(534, 540, date2, langCon);
    tab += tableYears(541, 550, date2, langCon);
    
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Northern Qi (550-577)</h2> <br />';
    } else if (lang==1) {
        txt += '<h2>北 齊 (550-577)</h2> <br />';
    } else {
        txt += '<h2>北 齐 (550-577)</h2> <br />';
    }
    tab += txt;
    tab += tableYears(550, 560, date2, langCon);
    tab += tableYears(561, 570, date2, langCon);
    tab += tableYears(571, 577, date2, langCon);
    date2 = null;
    
    langCon.region = 'WeiZhouSui';
    let date3 = new Array(47);
    for (i=0; i<47; i++) {
        y = i + 535;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date3[i] = new Array(16);
        date3[i][0] = y;
        cm = cmonthDate_WeiZhouSui(y, jdc, false);
        for (j=0; j<15; j++) {
            date3[i][j+1] = cm[j];
        }
    }
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Western Wei (535-557)</h2> <br />';
    } else {
        txt += '<h2>西 魏 (535-557)</h2> <br />';
    }
    tab += txt;
    tab += tableYears(535, 540, date3, langCon);
    tab += tableYears(541, 550, date3, langCon);
    tab += tableYears(550, 557, date3, langCon);
    txt = '<br />';
    if (lang==0) {
        txt += '<h2>Northern Zhou (557-581)</h2> <br />';
    } else {
        txt += '<h2>北 周 (557-581)</h2> <br />';
    }
    tab += txt;
    tab += tableYears(557, 560, date3, langCon);
    tab += tableYears(561, 570, date3, langCon);
    tab += tableYears(571, 581, date3, langCon);
    date3 = null;
    
    txt = '';
    if (lang==0) {
        txt +='<h2><a href="NorthSouth_calendars.html">Calendar Differences in this period</a></h2>';
    } else if (lang==1) {
        txt +='<h2><a href="NorthSouth_calendars_chinese.html">南 北 朝 朔 閏 異 同 表</a></h2>';
    } else {
        txt +='<h2><a href="NorthSouth_calendars_simp.html">南 北 朝 朔 闰 异 同 表</a></h2>';
    }
    txt += '<br /><br />';
    tab += txt;
    document.getElementById('table').innerHTML = tab;
}

// Table for Song, Qi, Liang and Chen (420 - 589)
function table_snsouth(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (420 &ndash; 589)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in Song, Qi, Liang and Chen dynasties (420&ndash;589). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>南 北 朝: 宋、 齊、 梁、 陳 朔 閏 表 (420 &ndash; 589)</h1>';
        tab.innerHTML = '<p>下表列出宋、 齊、 梁、 陳時(420年至589年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>南 北 朝: 宋、 齐、 梁、 陈 朔 闰 表 (420 &ndash; 589)</h1>';
        tab.innerHTML = '<p>下表列出宋、齐、梁、陈时(420年至589年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(420, 430, date, langCon);
    
    for (let ystart=431; ystart <= 571; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(581, 589, date, langCon);
    date = null;
    
    let txt = '';
    if (lang==0) {
        txt +='<h2><a href="NorthSouth_calendars.html">Calendar Differences in this period</a></h2>';
    } else if (lang==1) {
        txt +='<h2><a href="NorthSouth_calendars_chinese.html">南 北 朝 朔 閏 異 同 表</a></h2>';
    } else {
        txt +='<h2><a href="NorthSouth_calendars_simp.html">南 北 朝 朔 闰 异 同 表</a></h2>';
    }
    txt += '<br /><br />';
    tab += txt;
    document.getElementById('table').innerHTML = tab;
}

// Table for Sui dynasty (581-617)
function table_sui(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (581 &ndash; 617)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Sui dynasty (581&ndash;617). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>隋 朝 朔 閏 表 (581 &ndash; 617)</h1>';
        tab.innerHTML = '<p>下表列出隋朝時(581年至617年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>隋 朝 朔 闰 表 (581 &ndash; 617)</h1>';
        tab.innerHTML = '<p>下表列出隋朝时(581年至617年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    langCon.region = 'WeiZhouSui';
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    
    let date1 = new Array(10);
    let i,j,y, ystart, accleap, jdc, cm;
    for (i=0; i<10; i++) {
        y = i + 581;
        // Julian date number at noon on Dec 31, y-1 
        accleap = Math.floor(0.25*(y + 799) + 1e-5);
        jdc = 1429223 + accleap + 365*(y+799);
        date1[i] = new Array(16);
        date1[i][0] = y;
        cm = cmonthDate_WeiZhouSui(y, jdc, false);
        for (j=0; j<15; j++) {
            date1[i][j+1] = cm[j];
        }
    }
    tab = tableYears(581, 590, date1, langCon);
    date1 = null;
    
    langCon.region = 'default';
    let date = ChineseToGregorian();
    tab += tableYears(591, 600, date, langCon);
    tab += tableYears(601, 610, date, langCon);
    tab += tableYears(611, 617, date, langCon);
    date = null;
    document.getElementById('table').innerHTML = tab;
}

// Table for Tang dynasty and Five dynasties (618-959)
function table_tang5(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (618 &ndash; 959)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Tang dynasty and Five dynasties (618&ndash;959). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. When MM is negative, it means the month in the previous year. For example, -11-27 means November 27th in the previous year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>唐 朝 和 五 代 (梁、 唐、 晉、 漢、 周) 朔 閏 表 (618 &ndash; 959)</h1>';
        tab.innerHTML = '<p>下表列出唐朝及五代時(618年至959年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月，負數的MM表示上一個公曆年的月份，例如 -11-27 表示上一年的11月27日。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>唐 朝 和 五 代 (梁、 唐、 晋、 汉、 周) 朔 闰 表 (618 &ndash; 959)</h1>';
        tab.innerHTML = '<p>下表列出唐朝及五代时(618年至959年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月，负数的MM表示上一个公历年的月份，例如 -11-27 表示上一年的11月27日。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(618, 630, date, langCon);
    let ystart;
    for (ystart=631; ystart <= 671; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    
    // Set up 2D array date2 for the years 681-689
    let y, date2 = new Array(9);
    let y0 = date[0][0];
    let i,j,k;
    for (y=681; y<=689; y++) {
        j = y-681;
        date2[j] = new Array(16);
        for (i=0; i<16; i++) {
            date2[j][i] = date[y-y0][i];
        }
    }
    // remove months 11 and 12 from the year 689 by 
    // seting the to 9999, a number the function ymd() 
    // recongnizes as NA. 
    // Number of days in N_{689} is 325
    date2[8][11] = 9999; date2[8][12] = 9999;
    date2[8][15] = 325;
    tab += tableYears(681, 689, date2, langCon);
    date2 = null;
    
    let info;
    if (lang==0) {
        info = '<p style="color:red;">In December 689, Empress Consort Wu designated the z&#464; month (month 11) as the first month of a year. However, the month numbers did not change. The z&#464; month was named Zheng, which is usually referred to month 1; ch&#466;u month was stilled called month 12; y&#237;n month was month 1 and so on. Here the Zheng month is still labelled as month 11. The first month of a year was changed back to month 1 in February 701. The Chinese year in 689 only had 11 months (one leap month), whereas the Chinese year in 700 had 15 months (one leap month).</p>';
        langCon.month_num = ["11","12","1","2","3","4","5","6","7","8","9","10","leap<br />mon."];
    } else if (lang==1) {
        info = '<p style="color:red;">公元689年12月，武則天改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月，建寅（即現在的正月）改稱一月，其他農曆月的數序不變（即正月、十二月、一月、二月⋯⋯十月）。公元701年2月又改回以建寅為年首。公元689年的農曆年（己丑年）只有十一個月（其中一個月是閏月），而公元700年的農曆年（庚子年）有十五個月（其中一個月是閏月）。</p>';
        langCon.month_num = ["正(子)", "十二", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "閏月"];
    } else {
        info = '<p style="color:red;">公元689年12月，武则天改正朔，以周正建子(即现在的十一月)为年首，建子改称正月，建寅（即现在的正月）改称一月，其他农历月的数序不变（即正月、十二月、一月、二月__十月）。公元701年2月又改回以建寅为年首。公元689年的农历年（己丑年）只有十一个月（其中一个月是闰月），而公元700年的农历年（庚子年）有十五个月（其中一个月是闰月）。</p>';
        langCon.month_num = ["正(子)", "十二", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "闰月"];
    }
    tab += info;
    
    // Set up 2D array date2 for the years 690-699
    date2 = new Array(10);
    for (y=690; y<=699; y++) {
        i = y-690; j = y-y0;
        date2[i] = new Array(16);
        let ndays1 = NdaysGregJul(y-1);
        date2[i][0] = date[j][0];
        date2[i][1] = date[j-1][11] - ndays1;
        date2[i][2] = date[j-1][12] - ndays1;
        for (k=3; k<13; k++) {
            date2[i][k] = date[j][k-2];
        }
        date2[i][13] = date[j][13];
        date2[i][14] = date[j][14]+2;
        if (date2[i][14] > 12) { date2[i][14] -= 12;}
        // Number of days in the Chinese year
        date2[i][15] = date[j][11] - date2[i][1];
    }
    tab += tableYears(690, 699, date2, langCon);
    date2 = null;
    
    // Manually create the table for year 700
    if (lang==0) {
        info = '<table>';
        info += '<tr> <th rowspan="2">Julian<br />year</th> <th rowspan="2">Chinese<br />year</th> <th colspan="8">Months in Chinese Calendar</th></tr>';
        info += '<tr> <th>11</th> <th>12</th> <th>1</th> <th>2</th> <th>3</th> <th>4</th> <th>5</th> <th>6</th></tr>';
        info += '<tr> <td rowspan="3">700</td> <td rowspan="3">G&#275;ng z&#464; (Rat)</td> <td>-11-27</td> <td>-12-27</td> <td>01-26</td> <td>02-25</td> <td>03-25</td> <td>04-24</td> <td>05-23</td> <td>06-21</td></tr>';
        info += '<tr> <th>7</th> <th>8</th> <th>9</th> <th>10</th> <th>11</th> <th>12</th> <th>leap<br />mon.</th> <th># days</th></tr>';
        info += '<tr><td>07-21</td> <td>09-17</td> <td>10-17</td> <td>11-15</td> <td>12-15</td> <td>13-14</td> <td>7: 08-19</td> <td>444</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["1","2","3","4","5","6","7","8","9","10","11","12","leap<br />mon."];
    } else if (lang==1) {
        info = '<table>';
        info += '<tr> <th rowspan="2">公曆年</th> <th rowspan="2">中曆年</th> <th colspan="8">中曆月</th></tr>';
        info += '<tr> <th>正(子)</th> <th>十二</th> <th>一</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th> <th>六</th></tr>';
        info += '<tr> <td rowspan="3">700</td> <td rowspan="3">武周聖曆三年/久視元年</td> <td>-11-27<br />辛亥</td> <td>-12-27<br />辛巳</td> <td>01-26<br />辛亥</td> <td>02-25<br />辛巳</td> <td>03-25<br />庚戌</td> <td>04-24<br />庚辰</td> <td>05-23<br />己酉</td> <td>06-21<br />戊寅</td></tr>';
        info += '<tr> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>閏月</th> <th>日數</th></tr>';
        info += '<tr><td>07-21<br />戊申</td> <td>09-17<br />丙午</td> <td>10-17<br />丙子</td> <td>11-15<br />乙巳</td> <td>12-15<br />乙亥</td> <td>13-14<br />乙巳</td> <td>七: 08-19<br />丁丑</td> <td>444</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "閏月"];
    } else {
        info = '<table>';
        info += '<tr> <th rowspan="2">公历年</th> <th rowspan="2">中历年</th> <th colspan="8">中历月</th></tr>';
        info += '<tr> <th>正(子)</th> <th>十二</th> <th>一</th> <th>二</th> <th>三</th> <th>四</th> <th>五</th> <th>六</th></tr>';
        info += '<tr> <td rowspan="3">700</td> <td rowspan="3">武周圣历三年/久视元年</td> <td>-11-27<br />辛亥</td> <td>-12-27<br />辛巳</td> <td>01-26<br />辛亥</td> <td>02-25<br />辛巳</td> <td>03-25<br />庚戌</td> <td>04-24<br />庚辰</td> <td>05-23<br />己酉</td> <td>06-21<br />戊寅</td></tr>';
        info += '<tr> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>闰月</th> <th>日数</th></tr>';
        info += '<tr><td>07-21<br />戊申</td> <td>09-17<br />丙午</td> <td>10-17<br />丙子</td> <td>11-15<br />乙巳</td> <td>12-15<br />乙亥</td> <td>13-14<br />乙巳</td> <td>七: 08-19<br />丁丑</td> <td>444</td></tr>';
        info += '</table> <br /><br />';
        langCon.month_num = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "闰月"];
    }
    tab += info;
    
    for (ystart=701; ystart <= 741; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    
    // Set up 2D array date2 for the years 751-760
    date2 = new Array(11);
    for (y=751; y<=761; y++) {
        j = y-751;
        date2[j] = new Array(16);
        for (i=0; i<16; i++) {
            date2[j][i] = date[y-y0][i];
        }
    }
    // remove months 11 and 12 from the year 761 by 
    // seting the to 9999, a number the function ymd() 
    // recongnizes as NA. 
    // Number of days in N_{761} is 295
    date2[10][11] = 9999; date2[10][12] = 9999;
    date2[10][15] = 295;
    tab += tableYears(751, 761, date2, langCon);
    if (lang==0) {
        info = '<p style="color:red;">In December 761, emperor Suzong of the Tang dynasty designated the z&#464; month (present day month 11) as the first month of a year; the ch&#466;u month (present day month 12) became month 2; the y&#237;n month (present day month 1) became month 3 and so on. The Chinese month numbers were shifted by two. As a result, the Chinese year in 761 (X&#299;n ch&#466;u) had only 10 months. The month numbers ware switched back to the old system in April 762. The Chinese year in 762 (R&#233;n y&#237;n) had 14 months, with two month 4s (m&#462;o month and s&#236; month) and two month 5s (ch&#233;n month and w&#468; month).</p>';
    } else if (lang==1) {
        info = '<p style="color:red;">公元761年12月，唐肅宗改正朔，以周正建子(即現在的十一月)為年首，建子改稱正月、建丑（即現在的十二月）改稱二月、建寅（即現在的正月）改稱三月等等，與現在通用的月序相差二個月。公元762年4月又把農曆月的數序改回以建寅為正月、建卯為二月等。公元761年的農曆年（辛丑年）只有十個月,而公元762年的農曆年（壬寅年）則有十四個月，其中有兩個四月(建卯和建巳)和兩個五月(建辰和建午)。</p>';
    } else {
        info = '<p style="color:red;">公元761年12月，唐肃宗改正朔，以周正建子(即现在的十一月)为年首，建子改称正月、建丑（即现在的十二月）改称二月、建寅（即现在的正月）改称三月等等，与现在通用的月序相差二个月。公元762年4月又把农历月的数序改回以建寅为正月、建卯为二月等。公元761年的农历年（辛丑年）只有十个月,而公元762年的农历年（壬寅年）则有十四个月，其中有两个四月(建卯和建巳)和两个五月(建辰和建午)。</p>';
    }
    tab += info;
    // Manually create the table for year 762
    if (lang==0) {
        info = '<table>';
        info += '<tr> <th rowspan="2">Julian<br />year</th> <th rowspan="2">Chinese<br />year</th> <th colspan="8">Months in Chinese Calendar</th></tr>';
        info += '<tr> <th>1 (z&#464;)</th> <th>2</th> <th>3</th> <th>4 (m&#462;o)</th> <th>5 (ch&#233;n)</th> <th>4 (s&#236;)</th> <th>5 (w&#468;)</th> <th>6</th></tr>';
        info += '<tr> <td rowspan="3">762</td> <td rowspan="3">R&#233;n y&#237;n (Tiger)</td> <td>-12-02</td> <td>-12-31</td> <td>01-30</td> <td>03-01</td> <td>03-30</td> <td>04-29</td> <td>05-28</td> <td>06-27</td></tr>';
        info += '<tr> <th>7</th> <th>8</th> <th>9</th> <th>10</th> <th>11</th> <th>12</th> <th>leap<br />mon.</th> <th># days</th></tr>';
        info += '<tr><td>07-26</td> <td>08-24</td> <td>09-23</td> <td>10-22</td> <td>11-21</td> <td>12-20</td> <td>&mdash;</td> <td>413</td></tr>';
        info += '</table> <br /><br />';
    } else if (lang==1) {
        info = '<table>';
        info += '<tr> <th rowspan="2">公曆年</th> <th rowspan="2">中曆年</th> <th colspan="8">中曆月</th></tr>';
        info += '<tr> <th>正(子)</th> <th>二</th> <th>三</th> <th>四 (卯)</th> <th>五 (辰)</th> <th>四 (巳)</th> <th>五 (午)</th> <th>六</th></tr>';
        info += '<tr> <td rowspan="3">762</td> <td rowspan="3">唐肅宗上元三年/寶應元年</td> <td>-12-02<br />壬午</td> <td>-12-31<br />辛亥</td> <td>01-30<br />辛巳</td> <td>03-01<br />辛亥</td> <td>03-30<br />庚辰</td> <td>04-29<br />庚戌</td> <td>05-28<br />己卯</td> <td>06-27<br />己酉</td></tr>';
        info += '<tr> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>閏月</th> <th>日數</th></tr>';
        info += '<tr><td>07-26<br />戊寅</td> <td>08-24<br />丁未</td> <td>09-23<br />丁丑</td> <td>10-22<br />丙午</td> <td>11-21<br />丙子</td> <td>12-20<br />乙巳</td> <td>&mdash;</td> <td>413</td></tr>';
        info += '</table> <br /><br />';
    } else {
        info = '<table>';
        info += '<tr> <th rowspan="2">公历年</th> <th rowspan="2">中历年</th> <th colspan="8">中历月</th></tr>';
        info += '<tr> <th>正(子)</th> <th>二</th> <th>三</th> <th>四 (卯)</th> <th>五 (辰)</th> <th>四 (巳)</th> <th>五 (午)</th> <th>六</th></tr>';
        info += '<tr> <td rowspan="3">762</td> <td rowspan="3">唐肃宗上元三年/宝应元年</td> <td>-12-02<br />壬午</td> <td>-12-31<br />辛亥</td> <td>01-30<br />辛巳</td> <td>03-01<br />辛亥</td> <td>03-30<br />庚辰</td> <td>04-29<br />庚戌</td> <td>05-28<br />己卯</td> <td>06-27<br />己酉</td></tr>';
        info += '<tr> <th>七</th> <th>八</th> <th>九</th> <th>十</th> <th>十一</th> <th>十二</th> <th>闰月</th> <th>日数</th></tr>';
        info += '<tr><td>07-26<br />戊寅</td> <td>08-24<br />丁未</td> <td>09-23<br />丁丑</td> <td>10-22<br />丙午</td> <td>11-21<br />丙子</td> <td>12-20<br />乙巳</td> <td>&mdash;</td> <td>413</td></tr>';
        info += '</table> <br /><br />';
    }
    tab += info;
    
    // Rest of the period
    tab += tableYears(763, 770, date, langCon);
    for (ystart=771; ystart <= 941; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(951, 959, date, langCon);
    date = null;
    date2 = null;
    document.getElementById('table').innerHTML = tab;
}

// Table for Song dynasty (960-1279)
function table_song(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (960 &ndash; 1279)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Song dynasty (960&ndash;1279). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>宋 朝 朔 閏 表 (960 &ndash; 1279)</h1>';
        tab.innerHTML = '<p>下表列出宋朝時(960年至1279年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>宋 朝 朔 闰 表 (960 &ndash; 1279)</h1>';
        tab.innerHTML = '<p>下表列出宋朝时(960年至1279年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(960, 970, date, langCon);
    for (let ystart=971; ystart <= 1261; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(1271, 1279, date, langCon);
    date = null;
    
    let txt = '';
    if (lang==0) {
        txt +='<h2><a href="LiaoJinYuan_calendars.html">Calendar Differences Between the Northern and Southern Dynasties in 947 – 1279</a></h2>';
    } else if (lang==1) {
        txt +='<h2><a href="LiaoJinYuan_calendars_chinese.html">宋 遼 金 元 朔 閏 異 同 表</a></h2>';
    } else {
        txt +='<h2><a href="LiaoJinYuan_calendars_simp.html">宋 辽 金 元 朔 闰 异 同 表</a></h2>';
    }
    txt += '<br /><br />';
    tab += txt;
    document.getElementById('table').innerHTML = tab;
}

// Table for Liao and Jin (947 - 1234)
function table_liaojin(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (947 &ndash; 1234)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Liao (a.k.a.Khitan) dynasty and Jin dynasty (947&ndash;1234). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>遼 金 朔 閏 表 (947 &ndash; 1234)</h1>';
        tab.innerHTML = '<p>下表列出遼金時(947年至1234年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>辽 金 朔 闰 表 (947 &ndash; 1234)</h1>';
        tab.innerHTML = '<p>下表列出辽金时(947年至1234年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    langCon.region = 'LiaoJinYuan';
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    let corr = LiaoJinYuanCorrection();
    let ystart = date[0][0];
    for (let y=947; y <= 1234; y++) {
        let prop = 'y'+y.toString();
        if (prop in corr) {
            // Correction for year y
            let corr_array = corr[prop];
            for (let i=0; i<corr_array.length; i += 2) {
                date[y-ystart][corr_array[i]] = corr_array[i+1];
            }
        }
    }
    tab = tableYears(947, 960, date, langCon);
    for (ystart=961; ystart <= 1221; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(1231, 1234, date, langCon);
    date = null;
    
    let txt = '';
    if (lang==0) {
        txt +='<h2><a href="LiaoJinYuan_calendars.html">Calendar Differences Between the Northern and Southern Dynasties in 947 – 1279</a></h2>';
    } else if (lang==1) {
        txt +='<h2><a href="LiaoJinYuan_calendars_chinese.html">宋 遼 金 元 朔 閏 異 同 表</a></h2>';
    } else {
        txt +='<h2><a href="LiaoJinYuan_calendars_simp.html">宋 辽 金 元 朔 闰 异 同 表</a></h2>';
    }
    txt += '<br /><br />';
    tab += txt;
    document.getElementById('table').innerHTML = tab;
}

// Table for Mongol/Yuan dynasty (1234-1367)
function table_yuan(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (1234 &ndash; 1367)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian dates MM-DD of the first day of each month in the Chinese calendar in the Mongol/Yuan dynasty (1234&ndash;1367). MM indicates the Julian month and DD indicates the Julian date. When MM is 13, it means January in the following Julian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>蒙 古 和 元 朝 朔 閏 表 (1234 &ndash; 1367)</h1>';
        tab.innerHTML = '<p>下表列出蒙古和元朝時(1234年至1367年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>蒙 古 和 元 朝 朔 闰 表 (1234 &ndash; 1367)</h1>';
        tab.innerHTML = '<p>下表列出蒙古和元朝时(1234年至1367年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    langCon.region = 'LiaoJinYuan';
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    let date = ChineseToGregorian();
    let corr = LiaoJinYuanCorrection();
    let ystart = date[0][0];
    for (let y=1234; y <= 1279; y++) {
        let prop = 'y'+y.toString();
        if (prop in corr) {
            // Correction for year y
            let corr_array = corr[prop];
            for (let i=0; i<corr_array.length; i += 2) {
                date[y-ystart][corr_array[i]] = corr_array[i+1];
            }
        }
    }
    tab = tableYears(1234, 1240, date, langCon);
    for (ystart=1241; ystart <= 1271; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    langCon.region = 'default';
    for (ystart=1281; ystart <= 1351; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(1361, 1367, date, langCon);
    date = null;
    document.getElementById('table').innerHTML = tab;
}

// Table for Ming dynasty (1368-1644)
function table_ming(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (1368 &ndash; 1644, 1645 &ndash; 1683)</h1>';
        tab.innerHTML = '<p>The following table lists the Julian/Gregorian dates MM-DD of the first day of each month in the Chinese calendar in the Ming dynasty (1368&ndash;1644), Southern Ming and Zheng dynasty (1645&ndash;1683). Julian calendar was used until October 4th, 1582, after which the Western calendar was switched to the Gregorian calendar. The date following October 4th, 1582 was October 15th, 1582 because of the Gregorian calendar reform. MM indicates the Julian/Gregorian month and DD indicates the Julian/Gregorian date. When MM is 13, it means January in the following Julian/Gregorian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Julian/Gregorian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>明 朝 (1368 &ndash; 1644)、南 明 及 明 鄭 (1645 &ndash; 1683) 朔 閏 表</h1>';
        tab.innerHTML = '<p>下表列出明朝(1368年至1644年)、南明及明鄭(1645&ndash;1683)時期農曆每月初一的公曆日期 MM-DD。公曆在1582年10月4日及以前用儒略曆，之後用格里高里曆。格里高里的曆改使1582年10月4日的下一日變成10月15日，跳了十日。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>明 朝 (1368 &ndash; 1644)、南 明 及 明 郑 (1645 &ndash; 1683) 朔 闰 表</h1>';
        tab.innerHTML = '<p>下表列出明朝(1368年至1644年)、南明及明郑(1645&ndash;1683)时期农历每月初一的公历日期 MM-DD。公历在1582年10月4日及以前用儒略历，之后用格里高里历。格里高里的历改使1582年10月4日的下一日变成10月15日，跳了十日。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Julian<br />year";
    }
    // Ming dynasty
    if (lang==0) {
        tab = '<br /><h2>Ming Dynasty (1368 &ndash; 1644)</h2><br />';
    } else if (lang==1) {
        tab = '<br /><h2>明 朝 (1368 &ndash; 1644)</h2><br />';
    } else {
        tab = '<br /><h2>明 朝 (1368 &ndash; 1644)</h2><br />';
    }
    let date = ChineseToGregorian();
    let ystart;
    tab += tableYears(1368, 1380, date, langCon);
    for (ystart=1381; ystart <= 1571; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    if (lang==0) {
        langCon.Wyear = "Jul./Greg.<br />year";
    }
    tab += tableYears(1581, 1590, date, langCon);
    
    if (lang==0) {
        langCon.Wyear = "Greg.<br />year";
    }
    for (ystart=1591; ystart <= 1631; ystart += 10) {
        tab += tableYears(ystart, ystart+9, 
                                    date, langCon);
    }
    tab += tableYears(1641, 1644, date, langCon);

    // Southern Ming and Zheng dynasty
    langCon.region = 'SouthernMing';
    date = southernMingCalendarData();
    if (lang==0) {
        tab += '<h2>Southern Ming and Zheng Dynasty (1645 &ndash; 1683)</h2><br />';
    } else if (lang==1) {
        tab += '<h2>南 明 及 明 鄭 (1645 &ndash; 1683)</h2><br />';
    } else {
        tab += '<h2>南 明 及 明 郑 (1645 &ndash; 1683)</h2><br />';
    }
    tab += tableYears(1645, 1650, date, langCon);
    for (ystart=1651; ystart <= 1671; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(1681, 1683, date, langCon);
    date = null;
    if (lang==0) {
        tab += '<h2><a href="QingSouthernMingZheng_calendars.html">Calendar Differences Between Qing, Southern Ming and Zheng Dynasties in 1645 - 1683</a></h2><br /><br />';
    } else if (lang==1) {
        tab += '<h2><a href="QingSouthernMingZheng_calendars_chinese.html">清 與 南 明 及 明 鄭 朔 閏 異 同 表</a></h2><br /><br />';
    } else {
        tab += '<h2><a href="QingSouthernMingZheng_calendars_simp.html">清 与 南 明 及 明 郑 朔 闰 异 同 表</a></h2><br /><br />';
    }

    document.getElementById('table').innerHTML = tab;
}

// Table for Qing dynasty (1645-1911)
function table_qing(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (1645 &ndash; 1911)</h1>';
        tab.innerHTML = '<p>The following table lists the Gregorian dates MM-DD of the first day of each month in the Chinese calendar in the Qing dynasty (1645&ndash;1911). MM indicates the Gregorian month and DD indicates the Gregorian date. When MM is 13, it means January in the following Gregorian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Gregorian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>清 朝 朔 閏 表 (1645 &ndash; 1911)</h1>';
        tab.innerHTML = '<p>下表列出清朝時(1645年至1911年)農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>清 朝 朔 闰 表 (1645 &ndash; 1911)</h1>';
        tab.innerHTML = '<p>下表列出清朝时(1645年至1911年)农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Greg.<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(1645, 1650, date, langCon);
    for (let ystart=1651; ystart <= 1891; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    tab += tableYears(1901, 1911, date, langCon);
    date = null;
    document.getElementById('table').innerHTML = tab;
}

// Table for 1912 - 2200
function table_recent(lang) {
    // title and description
    let tit = document.getElementById('title');
    let tab = document.getElementById('description');
    if (lang==0) {
        tit.innerHTML = '<h1>Chinese Calendar &ndash; Western Calendar Conversion Table (1912 &ndash; 2200)</h1>';
        tab.innerHTML = '<p>The following table lists the Gregorian dates MM-DD of the first day of each month in the Chinese calendar for the years 1912&ndash;2200. MM indicates the Gregorian month and DD indicates the Gregorian date. When MM is 13, it means January in the following Gregorian year. The &mdash; in the leap month column means that there is no leap month in that Chinese year. Otherwise, it has the form X: MM-DD. X indicates the month number before the leap month; MM-DD indicates the Gregorian date of the first day in the leap month. The last column lists the total number of days in the Chinese year.</p>';
        tab.innerHTML += '<p>The first day of a month in the Chinese calendar is determined by the day on which the lunar conjunction (i.e. new moon) falls. The exact time (in UTC+8) of a lunar conjunction cannot be determined accurately far in the future. If a lunar conjunction occurs near the midnight, the predicted first day of a month may be off by one day. These cases occur on September 29, 2057; September 4, 2089; August 7, 2097; September 28, 2133; October 17, 2172 and May 12, 2192. They are indicated by a star and in red color.</p>';
        tab.innerHTML += '<p>The Chinese calendar data on this website are computed using the method described <a href="computation.html">here</a>.</p>';
    } else if (lang==1) {
        tit.innerHTML = '<h1>1912年 &ndash; 2200年 朔 閏 表</h1>';
        tab.innerHTML = '<p>下表列出由1912年至2200年農曆每月初一的公曆日期 MM-DD。MM代表公曆月份，DD代表公曆日期。MM=13 表示下一個公曆年的1月。閏月欄裡 &mdash; 表示該農曆年沒有閏月; X: MM-DD 表示該農曆年有閏月，X 表示閏月的農曆月份，MM-DD 表示該閏月初一的公曆月日。公曆日期的下面是日干支。 日數指該農曆年的總日數，即由正月初一到下一個農曆年正月初一中間的日數。</p>';
        tab.innerHTML += '<p>農曆每月的初一定於朔(又稱新月)的日期，由於數十年後朔的UTC+8時刻難以準確推算，如果朔的時刻接近午夜零時，初一的確實日期或會與表列日期有一日之差。這些情況出現在公曆2057年9月29日、2089年9月4日、2097年8月7日、2133年9月28日、2172年10月17日和2192年5月12日. 下表把這些可能有一日誤差的初一日用紅色顯示並加上星號。</p>';
        tab.innerHTML += '<p><a href="computation_chinese.html">本網站的農曆編算方法</a></p>';
    } else {
        tit.innerHTML = '<h1>1912年 &ndash; 2200年 朔 闰 表</h1>';
        tab.innerHTML = '<p>下表列出由1912年至2200年农历每月初一的公历日期 MM-DD。MM代表公历月份，DD代表公历日期。MM=13 表示下一个公历年的1月。闰月栏里 &mdash; 表示该农历年没有闰月; X: MM-DD 表示该农历年有闰月，X 表示闰月的农历月份，MM-DD 表示该闰月初一的公历月日。公历日期的下面是日干支。 日数指该农历年的总日数，即由正月初一到下一个农历年正月初一中间的日数。</p>';
        tab.innerHTML += '<p>农历每月的初一定于朔(又称新月)的日期，由于数十年后朔的UTC+8时刻难以准确推算，如果朔的时刻接近午夜零时，初一的确实日期或会与表列日期有一日之差。这些情况出现在公历2057年9月29日、2089年9月4日、2097年8月7日、2133年9月28日、2172年10月17日和2192年5月12日. 下表把这些可能有一日误差的初一日用红色显示并加上星号。</p>';
        tab.innerHTML += '<p><a href="computation_simp.html">本网站的农历编算方法</a></p>';
    }
    
    let langCon = langConstant(lang);
    if (lang==0) {
        langCon.Wyear = "Greg.<br />year";
    }
    let date = ChineseToGregorian();
    tab = tableYears(1912, 1920, date, langCon);
    for (let ystart=1921; ystart <= 2191; ystart += 10) {
        tab += tableYears(ystart, ystart+9, date, langCon);
    }
    date = null;
    document.getElementById('table').innerHTML = tab;
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

// Print warning message
function printWarningMessage(y, langCon) {
    let lang = langCon.lang, warn = '';

    if (y==23) {
        if (lang==0) {
            warn = '<p style="color:red;">There were two sets of calendar for the Chinese year in 23 CE: one for the Xin dynasty and the other for the restored Han dynasty, also known as Gengshi. The two sets of calendar had 11 overlapping months: the second month in the Xin calendar was the same as the first month in the Gengshi calendar, the third month in the Xin calendar was the same as the second month in the Gengshi calendar, ..., and the last month in the Xin calendar was the same as the 11th month in the Gengshi calendar.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">地皇四年和更始元年有十一個月重疊。地皇四年用丑正、更始元年用寅正，所以地皇四年二月相當於更始元年正月、地皇四年三月相當於更始元年二月……地皇四年十二月相當於更始元年十一月。</p>';
        } else {
            warn = '<p style="color:red;">地皇四年和更始元年有十一个月重叠。地皇四年用丑正、更始元年用寅正，所以地皇四年二月相当于更始元年正月、地皇四年三月相当于更始元年二月……地皇四年十二月相当于更始元年十一月。</p>';
        }
    }
    
    if (y==240 && langCon.region=='Wu') {
        if (lang==0) {
           warn ='<p style="color:red;">In Appendix 2 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i>, the sexagenary day of the leap month conjunction in 238 is listed as j&#464; ch&#466;u, corresponding to Nov. 25. This is at odds with my calculation. The result of my calculation is consistent with the data on the <a href="http://sinocal.sinica.edu.tw/" target="_blank">Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The preface of the book says that the calendar data in its appendices are based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by W&#257;ng Yu&#275;zh&#275;n (汪曰楨). I looked at the book and found that the date listed there was also the same as my calculation. I suspect that the date listed in <i>3500 Years of Calendars and Astronomical Phenomena</i> is wrong. The book also lists the sexagenary day of the month 11 conjunction in the Wu state as j&#464; ch&#466;u, which is certainly wrong since this date was far away from the new moon close to the beginning of month 11.</p>'; 
        } else if (lang==1) {
            warn ='<p style="color:red;">《三千五百年历日天象》附表2記吳赤烏元年閏十月己丑朔和十一月己丑朔。十一月己丑朔無疑是錯的，這裡列出的閏十月戊子朔是根據我的推步，結果與台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>一致，《三千五百年历日天象》前言說其附表參照清汪曰楨的《歷代長術輯要》，翻查此書發現亦記吳閏十月戊子。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》附表2记吴赤乌元年闰十月己丑朔和十一月己丑朔。十一月己丑朔无疑是错的，这里列出的闰十月戊子朔是根据我的推步，结果与台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>一致，《三千五百年历日天象》前言说其附表参照清汪曰桢的《历代长术辑要》，翻查此书发现亦记吴闰十月戊子。</p>';
        }
    }
    
    if (y==450 && langCon.region=='WeiZhouSui') {
        if (lang==0) {
            warn = "<p style='color:red;'>According to <i>Index to Comprehensive Mirror to Aid in Governmance</i>, the month 11 conjunction in 447 occurred on a ji&#462; x&#363; day (Dec. 23). However, in <i>Compilation of Historical Calendars</i> by W&#257;ng Yu&#275;zh&#275;n, the month 12 conjunction was listed on a ji&#462; x&#363; day and is at odds with its statement that the winter solstice occurred on a ji&#462; x&#363; day in month 11. The month 12 conjunction on a ji&#462; x&#363; day is certainly a typo because a ji&#462; x&#363; day was 29 days (or 89 days) after a y&#464; s&#236; day, which was the leap month 10 conjunction date. So ji&#462; x&#363; day could only be the month 11 conjunction date. In <i>3500 Years of Calendars and Astronomical Phenomena</i> by Zh&#257;ng P&#233;iy&#250; and <i>Tables of Historical Lunar Conjunctions and Leap Months</i> by Ch&#233;n Yu&#225;n, the month 11 conjunction is mistakenly listed on Dec. 24. They were probably misled by W&#257;ng's typo. The book <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i> by Hsueh Chung-San and Ouyang Yi correctly places the month 11 conjunction on Dec. 23. Surprisingly, the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan, whose ancient calendar data are based on <i>A Sino-Western Calendar For Two Thousand Years (1-2000)</i>, does not follow the book and mistakenly places the month 11 conjunction on Dec. 24.</p>";
        } else if (lang==1) {
            warn = '<p style="color:red;">《通鑑目錄》記太武帝太平真君八年(447年)十一月甲戌朔，汪曰楨《歷代長術輯要》卻記「十乙亥、十二甲戌朔、閏十(十甲辰小雪、十一甲戌冬至)」，沒有記閏十月朔和十一月朔干支就是說兩朔日的天干和都是乙，但是「十二甲戌」是錯的，因為閏十朔是乙巳，而甲戌在乙巳後29日(或89日)，絕不可能是十二月朔，而且與其「十一甲戌冬至」相悖，可見「十二甲戌朔」應是「十一甲戌朔」之誤，「十二甲戌朔」是宋曆而非魏曆。張培瑜《三千五百年历日天象》和陳垣《二十史朔閏表》可能被《歷代長術輯要》誤導，記十一月乙亥朔及十二月甲辰朔。薛仲三、歐陽頤的《兩千年中西曆對照表》則沒有錯，奇怪的是臺灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換</a>卻不跟從《兩千年中西曆對照表》，也弄錯了十一月朔的日期。</p>';
        } else {
            warn ='<p style="color:red;">《通鉴目录》记太武帝太平真君八年(447年)十一月甲戌朔，汪曰桢《历代长术辑要》却记「十乙亥、十二甲戌朔、闰十(十甲辰小雪、十一甲戌冬至)」，没有记闰十月朔和十一月朔干支就是说两朔日的天干和都是乙，但是「十二甲戌」是错的，因为闰十朔是乙巳，而甲戌在乙巳后29日(或89日)，绝不可能是十二月朔，而且与其「十一甲戌冬至」相悖，可见「十二甲戌朔」应是「十一甲戌朔」之误，「十二甲戌朔」是宋历而非魏历。张培瑜《三千五百年历日天象》和陈垣《二十史朔闰表》可能被《历代长术辑要》误导，记十一月乙亥朔及十二月甲辰朔。薛仲三、欧阳颐的《两千年中西历对照表》则没有错，奇怪的是台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换</a>却不跟从《两千年中西历对照表》，也弄错了十一月朔的日期。</p>';
        }
    }
    
    if (y==510 && langCon.region=='default') {
        if (lang==0) {
           warn ='<p style="color:red;">There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. In 502, the leap month is listed as after month 5 in the main text but after month 4 in Appendix 3.</p>'; 
        } else if (lang==1) {
            warn ='<p style="color:red;">《三千五百年历日天象》的正文與其附表3的資料不一致，正文記502年閏五月，附表3則為閏四月。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》的正文与其附表3的资料不一致，正文记502年闰五月，附表3则为闰四月。</p>';
        }
    }
    
    if (y==580 && langCon.region=='default') {
        if (lang==0) {
            warn ='<p style="color:red;">There is a discrepancy between the main text and Appendix 3 in the book <i>3500 Years of Calendars and Astronomical Phenomena</i>. In 575, the leap month is listed as after month 8 in the main text but after month 9 in Appendix 3.</p>';
        } else if (lang==1) {
            warn ='<p style="color:red;">《三千五百年历日天象》的正文與其附表3的資料不一致，正文記575年閏八月，附表3則為閏九月。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》的正文与其附表3的资料不一致，正文记575年闰八月，附表3则为闰九月。</p>';
        }
    }
    
    if (y==577 && langCon.region=='WeiQi') {
        if (lang==0) {
            warn ="<p style='color:red;'>Appendix 3 of the book <i>3500 Years of Calendars and Astronomical Phenomena</i> lists the leap month in 575 as after month 9. This is at odds with my calculation, which agrees with the data on the <a href='http://sinocal.sinica.edu.tw/' target='_blank'>Chinese-Western calendar conversion website</a> created by Academia Sinica in Taiwan. The data in Appendix 3 are supposed to be based on the book 《歷代長術輯要》(<i>Compilation of Historical Calendars</i>) by W&#257;ng Yu&#275;zh&#275;n (汪曰楨), but that book also lists 575's leap month as after month 8. That's why I use my calculation here.</p>";
        } else if (lang==1) {
            warn ='<p style="color:red;">《三千五百年历日天象》附表3記北齊武平六年為閏九月，與我計算的閏八月不一致，台灣中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">兩千年中西曆轉換網站</a>和汪曰楨的《歷代長術輯要》也記北齊武平六年為閏八月，所以這裡不取《三千五百年历日天象》的數據。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》附表3记北齐武平六年为闰九月，与我计算的闰八月不一致，台湾中央研究院的<a href="http://sinocal.sinica.edu.tw/" target="_blank">两千年中西历转换网站</a>和汪曰桢的《历代长术辑要》也记北齐武平六年为闰八月，所以这里不取《三千五百年历日天象》的数据。</p>';
        }
    }
    
    if (y==680) {
        if (lang==0) {
            warn = '<p style="color:red;">The <i>Old Book of Tang</i> mentions leap month 10 in 678. However, the <i>New Book of Tang</i> mentions leap month 11. Many scholars adopt the data in the <i>New Book of Tang</i>. However, Huang Yi-Long, Professor in the Institute of History at the National Tsing-Hua University in Taiwan, <a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">investigated the issue</a> and concludes that the record in the <i>Old Book of Tang</i> is more reliable. His analysis places leap month 10 beginning on Nov. 19 and month 11 beginning on Dec. 19.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">《舊唐書》有儀鳳三年(678年)閏十月的記載，《新唐書》卻有閏十一月記載，學者一般取《新唐書》的閏月。但台灣國立清華大學歷史研究所的黃一農教授經過<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考證</a>後認為《舊唐書》的記載比較可信。根據他的考證，閏十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。</p>';
        } else {
            warn = '<p style="color:red;">《旧唐书》有仪凤三年(678年)闰十月的记载，《新唐书》却有闰十一月记载，学者一般取《新唐书》的闰月。但台湾国立清华大学历史研究所的黄一农教授经过<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">考证</a>后认为《旧唐书》的记载比较可信。根据他的考证，闰十月朔是癸丑(11月19日)，十一月朔是癸未(12月19日)。</p>';
        }
    }

    if (y==689) {
        if (lang==0) {
            warn = '<p style="color:red;">The New Year day in 684 was supposed to be on Jan 22, 684, but it was moved to Jan 23 by edict.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">嗣聖元年正月朔本在癸未(684年1月22日)，但唐高宗在弘道元年八月下旨，強將十二月改為大月，使正月朔移至甲申(1月23日)。</p>';
        } else {
            warn = '嗣圣元年正月朔本在癸未(684年1月22日)，但唐高宗在弘道元年八月下旨，强将十二月改为大月，使正月朔移至甲申(1月23日)。';
        }
    }

    if (y==699) {
        if (lang==0) {
            warn = '<p style="color:red;">In 697, Empress Consort Wu changed several calendar dates by edict in order to create a rare phenomenon that a winter solstice occurred on a ji&#462; z&#464; day and coincided with a lunar conjunction. It was claimed that several predicted conjunction dates in the previous years were incorrect, resulting in the Moon being visible on the last days of lunar months. The claim was in fact incorrect and was a pretense for the empress to change calendar dates. After an "investigation", it was decided that the winter solstice should be moved two days later to the ji&#462; z&#464; day (Dec. 20), which "happened to coincide" with the lunar conjunction. Because of this change, the lunar month started on Nov. 20, 697 became a leap month and the winter solstice became the New Year day. There was originally a leap month after month 12 in 698. In order to cancel the leap month, the middle solar term Z12 was moved from Jan 17, 698 to Jan 18, 698.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">萬歲通天二年，武則天為了營造正月甲子合朔冬至罕見曆象，偽稱曆官所推合朔時刻有不合天象，出現了「晦仍見月，有爽天經」之象，強將聖曆元年冬至移後兩日、大寒移後一日，使原本所推聖曆元年正月甲午朔變為通天二年閏十月甲午朔、聖曆元年十二月甲子朔變正月甲子朔，閏十二月癸巳朔變十二月癸巳朔。</p>';
        } else {
            warn = '<p style="color:red;">万岁通天二年，武则天为了营造正月甲子合朔冬至罕见历象，伪称历官所推合朔时刻有不合天象，出现了「晦仍见月，有爽天经」之象，强将圣历元年冬至移后两日、大寒移后一日，使原本所推圣历元年正月甲午朔变为通天二年闰十月甲午朔、圣历元年十二月甲子朔变正月甲子朔，闰十二月癸巳朔变十二月癸巳朔。</p>';
        }
    }

    if (y==730) {
        if (lang==0) {
            warn = '<p style="color:red;">The New Year day in 725 was supposed to be on Jan 19, 725 and there was a leap month after the first month. However, in order to prevent a solar eclipse on the New Year day, the leap month was moved to a month earlier by edict and became the last month in the Chinese year in 724 and the New Year day was moved to Feb 18, 725.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">開元十三年正月朔本在丙辰(725年1月19日)，為避正旦日食，當時強將閏月推前一月，使正月丙辰朔變閏十二月丙辰朔，閏正月丙戌朔(725年2月18日)變正月丙戌朔。</p>';
        } else {
            warn = '<p style="color:red;">开元十三年正月朔本在丙辰(725年1月19日)，为避正旦日食，当时强将闰月推前一月，使正月丙辰朔变闰十二月丙辰朔，闰正月丙戌朔(725年2月18日)变正月丙戌朔。</p>';
        }
    }
    
    if (y==1470) {
        if (lang==0) {
            warn = '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the first day of month 11 on Nov. 22 in 1462, which is inconsistent with the calendar issued by the Ming government (Nov. 21).</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">《三千五百年历日天象》記明英宗天順六年(1462年)十一月壬辰朔(11月22日)，不合當年的《大統曆》曆書(辛卯朔, 11月21日)，見<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中國史曆表朔閏訂正舉隅 &mdash; 以唐《麟德曆》行用時期為例」</a>緒言。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》记明英宗天顺六年(1462年)十一月壬辰朔(11月22日)，不合当年的《大统历》历书(辛卯朔, 11月21日)，见<a href="http://ccsdb.ncl.edu.tw/ccs/image/01_010_002_01_11.pdf" target="_blank">「中国史历表朔闰订正举隅 &mdash; 以唐《麟德历》行用时期为例」</a>绪言。</p>';
        }
    } 
    
    if (y==1590) {
        if (lang==0) {
            warn = '<p style="color:red;">1. Note that the year 1582 had only 355 days because of the Gregorian calendar reform: the day following Oct. 4 was Oct. 15. The Chinese year in 1582 also had 355 days. As a result, the Chinese new years in 1582 and 1583 fell on the same date in the Western calendar.</p>';
            warn += '<p style="color:red;">2. There are several mistakes in <i>3500 Years of Calendars and Astronomical Phenomena</i> in 1581 (month 10) and 1588 (months 3, 4, 12), which have been corrected here.</p>'
        } else if (lang==1) {
            warn = '<p style="color:red;">1. 格里高里的曆改使1582年只有355日:1582年10月4日的下一日是10月15日，跳了10日。1582年的農曆年(明神宗萬曆十年、壬午年)也剛好有355日，所以1582年和1583年的農曆新年的公曆日期在同一日。</p>';
            warn += '<p style="color:red;">2. 《三千五百年历日天象》在萬曆九年(十月朔)和十六年(三、四、十二月朔)有四個朔日錯誤，現已按《國家圖書館藏明代大統曆日彙編》第三冊第606頁、《國家圖書館藏明代大統曆日彙編》第四冊第135、139、175頁，及<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">典藏臺灣</a>的資料更正。</p>';
        } else {
            warn = '<p style="color:red;">1. 格里高里的历改使1582年只有355日:1582年10月4日的下一日是10月15日，跳了10日。1582年的农历年(明神宗万历十年、壬午年)也刚好有355日，所以1582年和1583年的农历新年的公历日期在同一日。</p>';
            warn += '<p style="color:red;">2. 《三千五百年历日天象》在万历九年(十月朔)和十六年(三、四、十二月朔)有四个朔日错误，现已按《国家图书馆藏明代大统历日汇编》第三册第606页、《国家图书馆藏明代大统历日汇编》第四册第135、139、175页，及<a href="http://catalog.digitalarchives.tw/item/00/07/ec/c9.html" target="_blank">典藏台湾</a>的资料更正。</p>';
        }
    }
    
    if (y==1600) {
        if (lang==0) {
            warn = '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day of 1600 on Feb. 14, which is inconsistent with the calendar issued by the Ming government (Feb. 15).</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">《三千五百年历日天象》記萬曆二十八年(1600年)正月乙巳朔(2月14日)，不合當年的《大統曆》曆書(丙午朔, 2月15日)，見《國家圖書館藏明代大統曆日彙編》第四冊第445頁。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》记万历二十八年(1600年)正月乙巳朔(2月14日)，不合当年的《大统历》历书(丙午朔, 2月15日)，见《国家图书馆藏明代大统历日汇编》第四册第445页。</p>';
        }
    }
    
    if (y==1610) {
        if (lang==0) {
            warn = '<p style="color:red;"><i>3500 Years of Calendars and Astronomical Phenomena</i> lists the New Year day of 1609 on Feb. 4, which is inconsistent with the calendar issued by the Ming government (Feb. 5).</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">《三千五百年历日天象》記萬曆三十七年(1609年)正月癸未朔(2月4日)，不合當年的《大統曆》曆書(甲申朔, 2月5日)，見《國家圖書館藏明代大統曆日彙編》第五冊第67頁。</p>';
        } else {
            warn = '<p style="color:red;">《三千五百年历日天象》记万历三十七年(1609年)正月癸未朔(2月4日)，不合当年的《大统历》历书(甲申朔, 2月5日)，见《国家图书馆藏明代大统历日汇编》第五册第67页。</p>';
        }
    }

    if (y==1670 && langCon.region != 'SouthernMing') {
        if (lang==0) {
            warn = '<p style="color:red;">The Chinese New Year in 1662 was originally on Feb. 19. There was a leap month after month 7 in 1661 and two major solar terms (Z11 and Z12) in month 11. The major solar term Z1 was originally placed on the last day of month 12 in 1661, leaving the first month in 1662 without a major solar term. To avoid controversy, the New Year Day was moved to Feb. 18 so that the first month would contain Z1, thus moving the month without major solar term to the last month of 1661.</p>';
        } else if (lang==1) {
            warn = '<p style="color:red;">康熙元年正月初一本在丙子日(2月19日)，事緣順治十八年閏七月，當年十一月含冬至和大寒兩中氣，雨水本來定在十二月晦，但這使康熙元年正月不含中氣。為免遭人非議，欽天監將正月初一提前一日至乙亥日(2月18日)，使正月含雨水，無中氣月便移到十二月。</p>';
        } else {
            warn = '<p style="color:red;">康熙元年正月初一本在丙子日(2月19日)，事缘顺治十八年闰七月，当年十一月含冬至和大寒两中气，雨水本来定在十二月晦，但这使康熙元年正月不含中气。为免遭人非议，钦天监将正月初一提前一日至乙亥日(2月18日)，使正月含雨水，无中气月便移到十二月。</p>';
        }
    }

    if (langCon.region=='SouthernMing') {
        if (y==1650) {
            warn = '<ol style="color:red;">';
            if (lang==0) {
                warn += '<li><p>Several sources indicate that the leap month in 1648 was after the 6th month, which I find to be very unlikely.</p></li>';
                warn += '<li><p>Two dfferent versions of calendar in the Southern Ming dynasty were produced in 1649. One of them was produced by the officials of the Yongli emperor, in which the New Year day was on February 11th, 1649. Another version was produced by the officials of the Prince of Lu, who named himself regent. The New Year day of the Lu calendar was on February 12th, 1649. According to the calculation of the Datong system, the New Year day was on February 11th, 1649.</p></li>';
                warn += "<li><p>According to <i>C&#225;n M&#237;ng D&#224; T&#466;ng L&#236;</i> or <i>Datong Calendar of the Waning Ming Dynasty</i> by Fu Yili and <i>Y&#225;n P&#237;ng W&#225;ng H&#249; Gu&#257;n Y&#225;ng Y&#299;ng C&#243;ng Zh&#275;ng Sh&#237; L&#249;</i> (or <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i>), the leap month in 1650 was after the 11th month in the Southern Ming calendar. This is consistent with the calculation by the Datong system. However, the Datong calendars produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a>, <a href='N1676_Zheng.html'>1676</a> and <a href='N1677_Zheng.html'>1677</a> recorded the leap month to be after the 12th month. Leap month 12 was probably based on an unofficial calendar expediently produced by the Zheng officials in 1649 since the official emperor calendar had not arrived in time because of war.</p></li>";
            } else if (lang==1) {
                warn += '<li><p>王叔武"南明史料朔閏考異"引 《劫灰錄》、 《鹿樵紀聞》、 《明季南略》、 《爝火錄》說永曆二年閏六月，我認為閏六月很可能不對。</p></li>';
                warn += '<li><p>永曆三年和魯王監國四年正月朔有異:永曆三年正月庚申朔;《魯監國大統曆》則有魯監國四年正月辛酉朔。依明大統曆推算此年正月為庚申朔。</p></li>';
                warn += '<li><p>傅以禮《殘明大統曆》和《延平王戶官楊英從征實錄》記永曆四年閏十一月，符合大統曆的推算，但明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>、<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>都記永曆四年閏十二月。閏十二月或許是當年鄭氏命官員權宜頒行的大統曆推算出的。</p></li>';
            } else {
                warn += '<li><p>王叔武"南明史料朔闰考异"引 《劫灰录》、 《鹿樵纪闻》、 《明季南略》、 《爝火录》说永历二年闰六月，我认为闰六月很可能不对。</p></li>';
                warn += '<li><p>永历三年和鲁王监国四年正月朔有异:永历三年正月庚申朔;《鲁监国大统历》则有鲁监国四年正月辛酉朔。依明大统历推算此年正月为庚申朔。</p></li>';
                warn += '<li><p>傅以礼《残明大统历》和《延平王户官杨英从征实录》记永历四年闰十一月，符合大统历的推算，但明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>、<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>都记永历四年闰十二月。闰十二月或许是当年郑氏命官员权宜颁行的大统历推算出的。</p></li>';
            }
            warn += '</ol>';
        }
        if (y==1660) {
            warn = '<ol style="color:red;">';
            if (lang==0) {
                warn += "<li><p>Two dfferent versions of calendar were produced in 1652: emperor Yongli's and Lu's version. The New Year day of the Yongli calendar was on February 10th, 1652. The New Year day of the Lu calendar was on February 9th, 1652. According to the calculation of the Datong system, the New Year day was on February 10th, 1652.</p></li>";
                warn += "<li><p>There are discrepancies in the leap month in 1653 among various sources. <i>Datong Calendar of the Waning Ming Dynasty</i> records the leap month to be after the 7th month, which is consistent with the caleculation of the Datong system. <i>Account of the quartermaster Yang Ying's campaign with Prince Yanping</i> has the leap month after the 8th month. The chronicle <i>X&#237;ng Z&#224;i Y&#225;ng Qi&#363;</i> records the leap month to be after the 6th month. The Datong calendar produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a> also records leap month after the 6th month. However, in the Datong calendar for <a href='N1676_Zheng.html'>1676</a> and <a href='N1677_Zheng.html'>1677</a>, the leap month is changed to being after the 8th month. I think leap month 6 is unlikely. Both leap month 7 and 8 are possible. Here I follow <i>Datong Calendar of the Waning Ming Dynasty</i> and place the leap month after the 7th month.</p></li>";
            } else if (lang==1) {
                warn += '<li><p>永曆六年和魯王監國七年正月朔有異:永曆六年正月甲戌朔;《魯監國大統曆》則有魯監國七年正月癸酉朔。依明大統曆推算此年正月為甲戌朔。</p></li>';
                warn += '<li><p>永曆七年的閏月有爭議，依大統曆推算閏七月，傅以禮《殘明大統曆》亦記閏七月，但是《延平王戶官楊英從征實錄》記閏八月，《行在陽秋》記閏六月，明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>也記閏六月，但是後來頒行的<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>卻改為閏八月。我認為閏六月不大可能，閏七月和閏八月機會較大，此處依《殘明大統曆》記閏七月。</p></li>';
            } else {
                warn += '<li><p>永历六年和鲁王监国七年正月朔有异:永历六年正月甲戌朔;《鲁监国大统历》则有鲁监国七年正月癸酉朔。依明大统历推算此年正月为甲戌朔。</p></li>';
                warn += '<li><p>永历七年的闰月有争议，依大统历推算闰七月，傅以礼《残明大统历》亦记闰七月，但是《延平王户官杨英从征实录》记闰八月，《行在阳秋》记闰六月，明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>也记闰六月，但是后来颁行的<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>却改为闰八月。我认为闰六月不大可能，闰七月和闰八月机会较大，此处依《残明大统历》记闰七月。</p></li>';
            }
            warn += '</ol>';
        }
        if (y==1680) {
            warn = '<ol style="color:red;">';
            if (lang==0) {
                warn += "<li><p>The New Year day in 1671 was on February 9th, 1671 according to <i>Datong Calendar of the Waning Ming Dynasty</i>, which also agrees with the calculation of the Datong system. However, the Datong calendar produced by the Zheng dynasty for <a href='N1671_Zheng.html'>1671</a> indicates that the New Year day was on February 10th, 1671. Even though Zheng dynasty claimed that their calendars were produced expediently and should not to be taken as official, by this time the Yongli emperor had died and the Southern Ming dynasty had already ended. Zheng's calendar became the de facto official Datong calendar of the state. So I change the New Year day to February 10th, 1671 in accord with Zheng's calendar.</p></li>";
                warn += '<li><p>According to the calculation of the Datong system, in 1674 the month 6 conjunction was on July 4th and month 9 conjunction was on September 30th. These dates are inconsistent with the records in <i>Datong Calendar of the Waning Ming Dynasty</i> (July 3rd and September 29th). The dates here are based on the records in <i>Datong Calendar of the Waning Ming Dynasty</i>.</p></li>';
                warn += '<li><p>According to the calculation of the Datong system, in 1675 a conjunction occurred on July 22nd. <i>Datong Calendar of the Waning Ming Dynasty</i> records a conjunction on July 23rd. The one-day difference changed the leap month in this year. July 22nd conjunction resulted in a leap month after the 5th month. July 23rd conjunction resulted in a leap month after the 6th month. Leap month 6 is also recorded in the calendars produced by the Zheng dynasty for <a href="N1676_Zheng.html">1676</a> and <a href="N1677_Zheng.html">1677</a>. So I use the data in <i>Datong Calendar of the Waning Ming Dynasty</i>.</p></li>';
                warn += '<li><p>According to the calculation of the Datong system, in 1677 the month 7 conjunction was on July 29th, which is inconsistent with July 30th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i> and the calendar produced by the Zheng dynasty for <a href="N1677_Zheng.html">1677</a>. The Zheng calendar date is used here.</p></li>';
                warn += '<li><p>According to the calculation of the Datong system, in 1678 the month 6 conjunction was on July 18th, inconsistent with July 19th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i>. July 19th is used here.</p></li>';
            } else if (lang==1) {
                warn += '<li><p>依大統曆推算永曆二十五正月癸丑朔，傅以禮《殘明大統曆》亦記正月癸丑朔，但是明鄭頒行的<a href="N1671_Zheng_chinese.html">永曆二十五年大統曆</a>記正月甲寅朔。雖然鄭氏奉明正朔，聲稱其大統曆乃「權宜頒行」，但是當時永曆帝已死，南明也已亡，明鄭的大統曆變相成為正統的大統曆書，所以此處依明鄭大統曆記正月甲寅朔。</p></li>';
                warn += '<li><p>依明大統曆推算永曆二十八年六月甲午朔及九月壬戌朔，此處依傅以禮《殘明大統曆》改為六月癸巳朔和九月辛酉朔。</p></li>';
                warn += '<li><p>依明大統曆推算永曆二十九年有朔日在丁巳(公曆7月22日)，對應的朔日在傅以禮《殘明大統曆》出現在下一日戊午(7月23日)。此一日之差造成閏月分歧:依大統曆推算閏五月，《殘明大統曆》則為閏六月。明鄭頒行的<a href="N1676_Zheng_chinese.html">永曆三十年大統曆</a>及<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>都記永曆二十九年閏六月，所以此處永曆二十九年朔閏依《殘明大統曆》。</p></li>';
                warn += '<li><p>依明大統曆推算永曆三十一年七月乙亥朔，不合傅以禮《殘明大統曆》及明鄭<a href="N1677_Zheng_chinese.html">永曆三十一年大統曆</a>的丙子朔。此處依《殘明大統曆》及明鄭大統曆記七月丙子朔。</p></li>';
                warn += '<li><p>依明大統曆推算永曆三十二年六月己巳朔，不合傅以禮《殘明大統曆》的庚午朔。此處依《殘明大統曆》記六月庚午朔。</p></li>';
            } else {
                warn += '<li><p>依大统历推算永历二十五正月癸丑朔，傅以礼《残明大统历》亦记正月癸丑朔，但是明郑颁行的<a href="N1671_Zheng_simp.html">永历二十五年大统历</a>记正月甲寅朔。虽然郑氏奉明正朔，声称其大统历乃「权宜颁行」，但是当时永历帝已死，南明也已亡，明郑的大统历变相成为正统的大统历书，所以此处依明郑大统历记正月甲寅朔。</p></li>';
                warn += '<li><p>依明大统历推算永历二十八年六月甲午朔及九月壬戌朔，此处依傅以礼《残明大统历》改为六月癸巳朔和九月辛酉朔。</p></li>';
                warn += '<li><p>依明大统历推算永历二十九年有朔日在丁巳(公历7月22日)，对应的朔日在傅以礼《残明大统历》出现在下一日戊午(7月23日)。此一日之差造成闰月分歧:依大统历推算闰五月，《残明大统历》则为闰六月。明郑颁行的<a href="N1676_Zheng_simp.html">永历三十年大统历</a>及<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>都记永历二十九年闰六月，所以此处永历二十九年朔闰依《残明大统历》。</p></li>';
                warn += '<li><p>依明大统历推算永历三十一年七月乙亥朔，不合傅以礼《残明大统历》及明郑<a href="N1677_Zheng_simp.html">永历三十一年大统历</a>的丙子朔。此处依《残明大统历》及明郑大统历记七月丙子朔。</p></li>';
                warn += '<li><p>依明大统历推算永历三十二年六月己巳朔，不合傅以礼《残明大统历》的庚午朔。此处依《残明大统历》记六月庚午朔。</p></li>';
            }
            warn += '</ol>';
        }
        if (y==1683) {
            if (lang==0) {
                warn = '<p style="color:red;">According to the calculation of the Datong system, the New Year day in 1682 was on February 8th, inconsistent with February 7th recorded in <i>Datong Calendar of the Waning Ming Dynasty</i>. February 7th is used here.</p>';
            } else if (lang==1) {
                warn = '<p style="color:red;">依明大統曆推算永曆三十六年正月庚戌朔，不合傅以禮《殘明大統曆》的己酉朔。此處依《殘明大統曆》記正月己酉朔。</p>';
            } else {
                warn = '<p style="color:red;">依明大统历推算永历三十六年正月庚戌朔，不合傅以礼《残明大统历》的己酉朔。此处依《残明大统历》记正月己酉朔。</p>';
            }
        }
    }

    if (y==2060) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 9 conjunction in 2057 is close to the midnight. The start day of the month may be one day earlier.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2057年九月'+langCon.note_early+'</p>';
        }
    }
    if (y==2090) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 8 conjunction in 2089 is close to the midnight. The start day of the month may be one day later.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2089年八月'+langCon.note_late+'</p>';
        }
    }
    if (y==2100) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 7 conjunction in 2097 is close to the midnight. The start day of the month may be one day earlier.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2097年七月'+langCon.note_early+'</p>';
        }
    }
    if (y==2120) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 2 conjunction in 2115 and month 4 conjunction in 2116 are close to the midnight. The start days of the months may be one day later.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2115年二月朔和2116年四月'+langCon.note_late+'</p>';
        }
    }
    if (y==2140) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 9 conjunction in 2133 is close to the midnight. The start day of the month may be one day earlier.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2133年九月'+langCon.note_early+'</p>';
        }
    }
    if (y==2170) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 11 conjunction in 2165 is close to the midnight. The start day of the month may be one day earlier.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2165年十一月'+langCon.note_early+'</p>';
        }
    }
    if (y==2180) {
        if (lang==0) {
            warn = '<p style="color:red;"><sup>*</sup>The month 9 conjunction in 2172 is close to the midnight. The start day of the month may be one day earlier.</p>';
        } else {
            warn = '<p style="color:red;"><sup>*</sup>2172年九月'+langCon.note_early+'</p>';
        }
    }
    return warn;
}

// *** TESTING ***
function generate_csv(ystart, yend, date) {
    let csv = 'year, M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11, M12, Mleap, leap\n';
    let y0 = date[0][0];
    let n;
    for (let y=ystart; y<=yend; y++) {
        let i = y-y0;
        csv += y+', ';
        for (let j=1; j<=12; j++) {
            let mmdd = ymd(y, date[i][j]);
            n = mmdd.length;
            if (mmdd.substring(0,3)=='<u>') {
                mmdd = mmdd.substring(3,n-4);
            }
            mmdd = parseInt(mmdd.substring(0,n-3)).toString() + mmdd.slice(-2);
            csv += mmdd+', '
        }
        if (date[i][14]==0) {
            csv += '0, 0\n';
        } else {
            mmdd = ymd(y, date[i][13]);
            n = mmdd.length;
            if (mmdd.substring(0,3)=='<u>') {
                mmdd = mmdd.substring(3,n-4);
            }
            mmdd = parseInt(mmdd.substring(0,n-3)).toString() + mmdd.slice(-2);
            csv += mmdd+', '+date[i][14].toString()+'\n';
        }
    }
    return csv;
}

function download_csv(data, filename) {
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
