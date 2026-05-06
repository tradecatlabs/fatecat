"use strict";

function header(lang, page, link) {
    let menulist = [], menu;
    if (lang==0) {
        // English
        menu = {id:'menuconversion', title:'Calendar<br />Conversion'};
        menu.sub = [{title:'Yearly Calendar', url:'index.html'},
                    {title:'Conversion Table', url:'table.html'},
                    {title:'Sun &amp; Moon Phenomena', url:'sunMoon.html'},
                    {title:'Julian &amp; Sexagenary Date Calculator', url:'Julian.html'}];
        menulist.push(menu);
            
        menu = {id:'menuCalendarBasics', title:'Chinese Calendar<br />Basics'};
        menu.sub = [{title:'24 Solar Terms', url:'solarTerms.html'},
                    {title:'Sexagenary Cycle', url:'sexagenary.html'},
                    {title:'Chinese Calendar Rules', url:'rules.html'},
                    {title:'Calendar Quiz', url:'simpleQuiz.html'}];
        menulist.push(menu);
        
        menu = {id:'menuCalendarComputation', title:'Calendar<br />Computation'};
        menu.sub = [{title:'Chinese Calendar Generation', url:'computation.html'}, 
                    {title:'Moon Phases and Solar Terms', url:'docs/sunMoon.pdf'},
                    {title:'Chunqiu Calendar', url:'chunqiu.html'},
                    {title:'Ancient Six Calendars', url:'guliuli.html'},
                    {title:'Qin &amp; Early Han Calendars', url:'QinHanCalendars.html'}];
        menulist.push(menu);
        
        menu = {id:'menuMisc', title:'Other<br />Links'};
        menu.sub = [{title:'Miscellaneous', url:'others.html'},
                    {title:'FAQ', url:'faq.html'}];
        menulist.push(menu);
    } else if (lang==1) {
        // traditional Chinese
        menu = {id:'menuconversion', title:'中 西 曆 對 照'};
        menu.sub = [{title:'年曆', url:'index_chinese.html'},
                    {title:'朔閏表', url:'table_chinese.html'},
                    {title:'氣朔時刻', url:'sunMoon_chinese.html'},
                    {title:'中國歷史年表', url:'era_names.html'},
                    {title:'儒略日數和日干支計算器', url:'Julian_chinese.html'}];
        menulist.push(menu);
        
        menu = {id:'menuCalendarBasics', title:'農 曆 知 識'};
        menu.sub = [{title:'二十四節氣', url:'solarTerms_chinese.html'},
                    {title:'六十干支', url:'sexagenary_chinese.html'},
                    {title:'農曆編算法則', url:'rules_chinese.html'}, 
                    {title:'曆法測驗', url:'simpleQuiz_chinese.html'}];
        menulist.push(menu);
        
        menu = {id:'menuCalendarComputation', title:'曆 法 計 算'};
        menu.sub = [{title:'編算農曆', url:'computation_chinese.html'},
                    {title:'月相和二十四節氣算法', url:'docs/sunMoon_chinese.pdf'},
                    {title:'春秋曆復原法', url:'chunqiu_chinese.html'},
                    {title:'古六曆計算法', url:'guliuli_chinese.html'},
                    {title:'秦至漢初的曆法復原', url:'QinHanCalendars_chinese.html'}];
        menulist.push(menu);
        
        menu = {id:'menuMisc', title:'其 他'};
        menu.sub = [{title:'雜 項', url:'others_chinese.html'},
                    {title:'常見問題', url:'faq_chinese.html'}];
        menulist.push(menu);
    } else {
        // simplified Chinese
                menu = {id:'menuconversion', title:'中 西 历 对 照'};
        menu.sub = [{title:'年历', url:'index_simp.html'},
                    {title:'朔闰表', url:'table_simp.html'},
                    {title:'气朔时刻', url:'sunMoon_simp.html'},
                    {title:'中国历史年表', url:'era_names_simp.html'},
                    {title:'儒略日数和日干支计算器', url:'Julian_simp.html'}];
        menulist.push(menu);
        
        menu = {id:'menuCalendarBasics', title:'农 历 知 识'};
        menu.sub = [{title:'二十四节气', url:'solarTerms_simp.html'},
                    {title:'六十干支', url:'sexagenary_simp.html'},
                    {title:'农历编算法则', url:'rules_simp.html'}, 
                    {title:'历法测验', url:'simpleQuiz_simp.html'}];
        menulist.push(menu);
        
        menu = {id:'menuCalendarComputation', title:'历 法 计 算'};
        menu.sub = [{title:'编算农历', url:'computation_simp.html'},
                    {title:'月相和二十四节气算法', url:'docs/sunMoon_simp.pdf'},
                    {title:'春秋历复原法', url:'chunqiu_simp.html'},
                    {title:'古六历计算法', url:'guliuli_simp.html'},
                    {title:'秦至汉初的历法复原', url:'QinHanCalendars_simp.html'}];
        menulist.push(menu);
        
        //menu = {id:'menuMisc', title:'其 他', url:'others_simp.html', sub:[]};
        menu = {id:'menuMisc', title:'其 他'};
        menu.sub = [{title:'杂项', url:'others_simp.html'},
                    {title:'常见问题', url:'faq_simp.html'}];
        menulist.push(menu);
    }
    
    let txt = '<div class="menu">';
    menulist.forEach(add_menu);
    
    function add_menu(x) {
        txt += '<div class="dropdown" id="'+x.id+'">';
        let n = x.sub.length;
        if (n==0) {
            txt += '<button class="dropbtn" style="cursor:pointer;"  onclick="myloadurl('+"'"+x.url+"'"+')">'+x.title+'</button></div>';
        } else {
            txt += '<button class="dropbtn" onclick="display_dropdown_menu('+"'"+x.id+"'"+')">'+x.title+'</button>';
            txt += '<div class="dropdown-content">';
            for (let i=0; i<n; i++) {
                txt += '<p onclick="myloadurl('+"'"+x.sub[i].url+"'"+')">'+x.sub[i].title+'</p>';
            }
            txt += '</div></div>';
        }
    }
    
    txt += '</div>';
    document.getElementById('menu').innerHTML = txt;
    
    if (link != "") {
        txt = '<h2 style="text-align:right;">';
        if (lang==0) {
            txt += 'Chinese versions: <a href="'+link+'_chinese.html">傳統中文</a> &nbsp; <a href="'+link+'_simp.html">简体中文</a></h2>';
        } else if (lang==1) {
            txt += '<a href="'+link+'.html">English 英文</a> &nbsp; <a href="'+link+'_simp.html">简体中文</a></h2>';
        } else {
            txt += '<a href="'+link+'.html">English 英文</a> &nbsp; <a href="'+link+'_chinese.html">傳統中文</a></h2>';
        }
        document.getElementById('language').innerHTML = txt;
    }
    if (window.location !== window.parent.location) {
        if (page=='table') {
            if (link=='') {
                document.getElementById('table').style.display = none;
            } else {
                document.getElementById('mainMenu').style.display = none;
            }
        } else {
            document.getElementById('wrapper0').style.display = none;
        }
    }
    add_footer();
}

// The click event is created to handle devices with touch screen
function display_dropdown_menu(id) {
    document.getElementById(id).classList.toggle('showdropdown');
    let x = document.getElementsByClassName('showdropdown');
    let n = x.length;
    for (let i=0; i<n; i++) {
        if (x[i].id != id) {
            x[i].classList.remove('showdropdown');
            break;
        }
    }
}

// remove showdropdown class and load url
function myloadurl(url) {
    let x = document.getElementsByClassName('showdropdown');
    let n = x.length;
    if (n==1) {
        x[0].classList.remove('showdropdown');
    }
    location.href = url;
}

function add_footer() {
    let foot = document.createElement('FOOTER');
    let txt = '<hr /><p style="text-align:center;font-size:90%;">&copy; 2018&ndash;2025 Yuk Tung Liu</p>';
    foot.innerHTML = txt;
    document.body.appendChild(foot);
}
