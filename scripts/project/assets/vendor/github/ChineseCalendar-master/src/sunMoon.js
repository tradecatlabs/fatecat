"use strict";

function init(lang) {
    if (window.location === window.parent.location) {
        document.getElementById('wrapper0').style.display = "block";
        header(lang, 'sunmoon','sunMoon');
        let input = document.getElementById("year");
        input.addEventListener("keyup", function(event) {
        if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById("myBtn").click();
        }
        });
        // Get input from url
        let year = 99999999;
        const p = new URLSearchParams(window.location.search);
        if (p.has('y')) {
            year = parseInt(p.get('y'), 10);
        }
        if (isNaN(year) || year < -3500 || year > 3500) {
        let d = new Date(); // current time from computer's clock
        year = d.getFullYear();
        }
        input.value = year;

        // Hide the years y-1 and y+1
        let acc = document.getElementsByClassName("accordion");
        let i;
        for (i = 0; i < acc.length; i++) {
        acc[i].onclick = function() {
            this.classList.toggle("active");
            let panel = this.nextElementSibling;
            if (panel.style.maxHeight){
            panel.style.maxHeight = null;
            } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
            } 
          }
        }
        submitYear(lang);
    } else {
        exception_handler();
    }
}

function submitYear(lang) {
    document.getElementById('err').innerHTML = "";
    let year = parseInt(document.getElementById('year').value, 10);
    if (isNaN(year) || year < -3500 || year > 3500) {
        let message = ['Invalid input! Please enter an integer between -3500 and 3500.', 
        '輸入錯誤﹗請輸入包括 -3500 和 3500 之間的整數。', 
        '输入错误！请输入包括 -3500 和 3500 之间的整数。'];
        document.getElementById('err').innerHTML = message[lang];
    } else {
        document.getElementById('year').value = year;
        let moon = mphases();
        let sun = sterms();
        addContent(lang, year-1, 'ym1', moon, sun);
        addContent(lang, year, 'y', moon, sun);
        addContent(lang, year+1, 'y1', moon, sun);
        moon = null;
        sun = null;
        // Hide the years y-1 and y+1
        let acc = document.getElementsByClassName("accordion");
        for (let i=0; i < acc.length; i++) {
            if (acc[i].classList.contains('active')) {
                acc[i].click();
            }
        }
    }
}

function addContent(lang, y, id, moon, sun) {
    let wyear = get_Western_calendar_name(y);
    let txt;
    if (lang==0) {
        txt = wyear[0]+' Year: '+y;
    } else {
        txt ='公元'+y+'年';
    }
    if (y <= 0) {
        let app = [' ('+(1-y)+' BCE)', '(前'+(1-y)+'年)', '(前'+(1-y)+'年)'];
        txt += app[lang];
    }
    if (lang != 0) { 
        txt += ' ('+wyear[lang]+')';
    }
    //if (addClickMesg) {
    //    txt += '&nbsp; <span style="font-size:80%;">(' + 
    //        (lang==0 ? 'Click to show/hide data':'點擊以顯示/隱藏數據')+')</span>';
    //}
    document.getElementById(id).innerHTML = txt;
    
    let mpName = ["New Moon", "First Quarter", "Full Moon", "Last Quarter"];
    let stermName = ["Z11 (Dec. solstice)", "J12", "Z12", "J1", "Z1", "J2", 
                     "Z2 (March equinox)", "J3","Z3", 
                     "J4", "Z4", "J5", "Z5 (June solstice)", "J6", "Z6", "J7", "Z7", 
                     "J8", "Z8 (Sep. equinox)", "J9", "Z9", "J10", "Z10", "J11"];
    if (lang != 0) {
        mpName = ["朔", "上弦", "望", "下弦"];
        if (lang==1) {
           stermName = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", 
                    "穀雨", "立夏", "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", 
                    "處暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"];
        } else {
           stermName = ["冬至", "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", 
                    "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", 
                    "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪"];
        }
    }
    let ind = y - yrange_sunMoon()[0];
    let i;
    let ndays = [NdaysGregJul(y-1), NdaysGregJul(y), NdaysGregJul(y+1)];
    
    // decompress data
    let offsets = offset_sunMoon();
    let moony = decompress_moonPhases(y, offsets.lunar, moon[ind], 0.25);
    moony.unshift(moon[ind][0]);
    let stermy = decompress_solarTerms(y, 0, offsets.solar, sun[ind]);
    let sun_temp = [sun[ind+1][0], sun[ind+1][1]];
    // add two more solar terms: Z11 and J12 following J11
    let st2 = decompress_solarTerms(y+1, 0, offsets.solar, sun_temp);
    stermy.push(st2[0]+1441*ndays[1], st2[1]+1441*ndays[1]);
    
    // Moon phases
    // Data structure:
    // moony is an array storing the moon phases data
    // moony[0] is an integer between 0 and 3:
    //         0 if moony[1] corresponds to a new moon
    //         1 if moony[1] corresponds to a first quarter
    //         2 if moony[1] corresponds to a full moon
    //         3 if moony[1] corresponds to a third quarter
    // moony[i] (i=1,2,... end of index): date and time of 
    //          moon phases represent by an integer 
    //          L so that floor(L/1441) is the number of days 
    //          from Jan 0 and L - 1441*floor(L/1441) is the 
    //          number of minutes from the midnight (UT1+8/UTC+8).
    txt = "<br />";
    let app = ['<h2>Phases of the Moon</h2>', 
              '<h2>月相</h2>', '<h2>月相</h2>'];
    txt += app[lang] + '<table>';
    txt += "<tr> <th>"+mpName[0]+"</th><th>"+mpName[1]+"</th><th>"+mpName[2]+"</th><th>"+mpName[3]+"</th></tr>";
    let ph = moony[0]; // First moon phase in the year
    if (ph != 0) {
        txt += '<tr> <td colspan="'+ph+'"></td>';
    }
    
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
    let no_eclipse = {solar:false, lunar:false};
    let sol_eclipse = {solar:true, lunar:false, 
                      eclipses:links[iec]};
    let extra_links = links[iec-1];
    extra_links.forEach(function(e) {
        if (ndays[0] - e[0] < 3) {
            // this is close to Jan 1, y; add it to be safe
            sol_eclipse.eclipses.push([e[0]-ndays[0], e[1], e[2]]);
        }
    });
    extra_links = links[iec+1];
    extra_links.forEach(function(e) {
        if (e[0] < 3) {
            // this is close to Dec 31, y; add it to be safe
            sol_eclipse.eclipses.push([e[0]+ndays[1], e[1], e[2]]);
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
    let lun_eclipse = {solar:false, lunar:true, 
                      eclipses:links[iec]};
    extra_links = links[iec-1];
    extra_links.forEach(function(e) {
        if (ndays[0] - e[0] < 3) {
            // this is close to Jan 1, y; add it to be safe
            lun_eclipse.eclipses.push([e[0]-ndays[0], e[1], e[2]]);
        }
    });
    extra_links = links[iec+1];
    extra_links.forEach(function(e) {
        if (e[0] < 3) {
            // this is close to Dec 31, y; add it to be safe
            lun_eclipse.eclipses.push([e[0]+ndays[1], e[1], e[2]]);
        }
    });
    links = null;
    for (i=1; i<moony.length; i++) {
        if (ph==0) { txt += "<tr>";}
        let eclipse = (ph==0 ? sol_eclipse:(ph==2 ? lun_eclipse:no_eclipse));
        txt += addDateTime(y, moony[i], ndays, lang, eclipse);
        if (ph==3) { txt += "</tr>";}
        if (i == moony.length-1 && ph != 3) {
            txt += '<td colspan="'+(3-ph)+'"></td></tr>';
        }
        ph = (ph + 1) % 4;
    }
    txt += "</table>";
    
    // 24 solar terms
    // Data structure:
    // stermy is an array storing the 24 solar term data
    // stermy[i] (i=0, 1, ... 26): dates and times of the solar terms 
    // starting from Z11 (usually in the previous year) to J12 
    // in the following year. 
    // Each of them is an integer calculated in the same way as in the 
    // dates and times of the moon phases.
    txt += "<br />";
    app = ['<h2>24 Solar Terms</h2>', '<h2>二十四節氣</h2>', '<h2>二十四节气</h2>'];
    txt += app[lang]+'<table>';
    app = ['<tr><th>Solar Term</th><th>Time</th> <td>&nbsp;</td> <th>Solar Term</th> <th>Time</th></tr>', 
          '<tr><th>節氣</th><th>時刻</th> <td>&nbsp;</td> <th>節氣</th><th>時刻</th></tr>', 
          '<tr><th>节气</th><th>时刻</th> <td>&nbsp;</td> <th>节气</th><th>时刻</th></tr>'];
    txt += app[lang];
    for (i=0; i < 24; i++) {
        if (i % 2 ==0) {
            txt += "<tr>";
        }
        txt += "<td>"+stermName[i]+"</td>";
        txt += addDateTime(y, stermy[i], ndays, lang, no_eclipse);
        if (i % 2 == 0) {
            txt += "<td></td>";
        } else {
            txt += "</tr>";
        }
    }
    // Two more solar terms: Z11 and J12 following J11
    txt += "<tr>";
    txt += "<td>"+stermName[0]+"</td>";
    txt += addDateTime(y, stermy[24], ndays, lang, no_eclipse);
    txt += "<td></td><td>"+stermName[1]+"</td>";
    txt += addDateTime(y, stermy[25], ndays, lang, no_eclipse) + "</tr>";
    txt += "</table>";
    document.getElementById(id+'content').innerHTML = txt;
}

// day from Dec 31, y-1 -> m, d (assume 1 <= day <= ndays )
function ymd2(dayIn, ndays, lang) {
    let leap = (ndays==366 ? 1:0);
    
    let day = dayIn;
    if (ndays < 360 && dayIn > 277) { day += 10;} // Gregorian reform
    let m,d;
    let mday = [0, 31, 59+leap, 90+leap, 120+leap, 151+leap, 181+leap, 212+leap,
           243+leap, 273+leap, 304+leap, 334+leap, 365+leap];
    if (day < 1) {
        m=0; d=day;
    } else {
        for (let i=1; i<13; i++) {
            if (day-mday[i] < 1) {
                m=i-1; d = day-mday[i-1];
                break;
            }
        }
    }
    
    let mmdd;
    if (lang==0) {
        let mname = ["Jan. ", "Feb. ", "Mar. ", "Apr. ", "May ", "June ", "July ", 
            "Aug. ", "Sep. ", "Oct. ", "Nov. ", "Dec. "];
        mmdd = mname[m] + d;
    } else {
        mmdd = (m+1)+"月"+d+"日";
    }
    return mmdd;
}

function addDateTime(y, m, ndays, lang, eclipse) {
    let txt = "<td>";
    let nday = ndays[1];
    let day = Math.floor(m/1441);
    let md = m - 1441*day;
    let hh = Math.floor(md/60);
    let mm = md - 60*hh;
    if (hh < 10) { hh = '0'+hh;}
    if (mm < 10) { mm = '0'+mm;}
    if (day < 1) {
        txt += "(" + (y-1) + ") ";
        day += ndays[0];
        nday = ndays[0];
    } else if (day > ndays[1]) {
        txt += "(" + (y+1) + ") ";
        day -= ndays[1];
        nday = ndays[2];
    }
    txt += ymd2(day, nday, lang)+", "+hh+":"+mm;
    txt += add_eclipse_link(y, m, eclipse, lang);
    return txt+"</td>";
}

function add_eclipse_link(y, m, eclipse, lang) {
    if (!eclipse.solar && !eclipse.lunar) { return '';}
    
    let ybeg = 1 + 100*Math.floor(0.01*(y - 0.5));
    let day = Math.floor(m/1441);
    day += (m - 1441*day)/1440;
    let txt = '';
    eclipse.eclipses.forEach(function(e) {
        if (Math.abs(day - e[0]) < 5) {
            if (y==ybeg && e[1] > 200) { 
                ybeg -= 100;
            } else if (y-ybeg==99 && e[1] < 200) {
                ybeg += 100;
            }
            let type;
            let linkg = 'http://ytliu.epizy.com/eclipse/';
            if (eclipse.solar) {
                if (lang==0) {
                    type = ['Partial solar eclipse', 'Annular solar eclipse', 'Total solar eclipse', 'Hybrid solar eclipse'];
                } else if (lang==1) {
                    type = ['日偏食', '日環食', '日全食', '日全環食'];
                } else {
                    type = ['日偏食', '日环食', '日全食', '日全环食'];
                }
                linkg += 'one_solar_eclipse_general.html?ybeg='+ybeg+'&ind='+e[1]+'&eph=DE431';
            } else {
                if (lang==0) {
                    type = ['Penumbral lunar eclipse', 'Partial lunar eclipse', 'Total lunar eclipse'];
                } else {
                    type = ['半影月食', '月偏食', '月全食'];
                }
                linkg += 'one_lunar_eclipse_general.html?ybeg='+ybeg+'&shrule=Danjon&ind='+e[1]+'&eph=DE431';
            }
            txt = '<br /><a href="'+linkg+'" target="_blank">'+type[e[2]]+'</a>';
        }
    });
    
    return txt;
}
