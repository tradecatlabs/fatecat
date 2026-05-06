const minify = require('terser').minify;
const ht = require('html-minifier-terser');
const fs = require('fs');
const html_minifier_option = {collapseWhitespace:true, removeComments:true, minifyCSS:true,
                              minifyJS:true};

let src = './src/';
let narg = process.argv.length;
let clean = (narg < 3 ? false:process.argv[2]=='clean');
let all = (narg < 3 ? false:process.argv[2]=='all');
let config_json = 'build_config.json';
if (!all && !clean && narg >=3) {
  config_json = process.argv[2];
}
let opt = JSON.parse(fs.readFileSync(config_json, 'utf8'));
let tg = opt.target_directory;
 
// remove trailing slash and white space
tg = tg.replace(/(\s*)$/, '').replace(/(\/?)$/, '').replace(/(\s*)$/, '');

// Check the existence of protect_this_dir.txt in the target directory
if (fs.existsSync(tg+'/protect_this_dir.txt')) {
   // protect_this_dir.txt exists in the target directory. Abort script
   let err = 'Cannot write files to the target directory '+tg +'\n';
   err += 'Because the file "protect_this_dir.txt" is there.\n';
   err += 'If you want to use this target directory,\n';
   err += 'either remove that file from the directory or rename it.\n';
   console.error(err);
   process.exit(1);
}

if (clean) {
  if (fs.existsSync(tg+'/src/protect_this_dir.txt')) {
     let err = 'Cannot remove directory '+tg+'...\n';
     err += 'because it contains the source directory.\n';
     console.error(err);
     process.exit(1);
  }

  // remove target directory
  let success = true;
  try {
    fs.rmdirSync(tg, {recursive: true});
  } catch(err) {
    success = false;
    console.error(err.message);
  }
  if (success) {
    console.log(tg+' is removed!');
  }
  process.exit();
}

// create target directory if it doesn't exist
if (!fs.existsSync(tg)){
    fs.mkdirSync(tg);
}

tg += '/';

async function build() {
  // Copy docs files
  if (all || opt.copy_docs) {
    console.log('Copying doc files...');
    let docs_dir_tg = tg + 'docs/';
    let docs_dir = src+'docs/'
    if (docs_dir_tg != docs_dir) {
      if (!fs.existsSync(docs_dir_tg)) {
         fs.mkdirSync(docs_dir_tg);
      }
      fs.copyFile(docs_dir+'sunMoon.pdf', docs_dir_tg+'sunMoon.pdf', 
         err => {if (err) throw err;});
      fs.copyFile(docs_dir+'sunMoon_chinese.pdf', docs_dir_tg+'sunMoon_chinese.pdf', 
         err => { if (err) throw err;});
      fs.copyFile(docs_dir+'sunMoon_simp.pdf', docs_dir_tg+'sunMoon_simp.pdf', 
         err => { if (err) throw err;});
    }
  }
  
  // Copy image files
  if (all || opt.copy_img) {
    console.log('Copying image files...');
    fs.readdir(src, (err, files) => {
      if (err) { throw err;}
      files.forEach(file => {
         if (file.match(/(\.jpg|\.png)$/)) {
           fs.copyFile(src+file, tg+file, err => {if (err) throw err;});
         }
      });
    });
  }
  
  // calendar_min.css 
  if (all || opt.calendar_min) {
    console.log('Minifying calendar.css...');
    let css = fs.readFileSync(src+'calendar.css', 'utf8');
    let css_min = await ht.minify(css, html_minifier_option); 
    fs.writeFileSync(tg+'calendar_min.css', css_min, 'utf8');
  }
  
  // calendar_chinese_min.css
  if (all || opt.calendar_chinese_min) {
    console.log('Minifying calendar_chinese.css...');
    let css = fs.readFileSync(src+'calendar_chinese.css', 'utf8');
    let css_min = await ht.minify(css, html_minifier_option);
    fs.writeFileSync(tg+'calendar_chinese_min.css', css_min, 'utf8');
  }
  
  // header_min.js
  if (all || opt.header_min) {
    console.log('Minifying header.js...');
    let code = {'header.js': fs.readFileSync(src+'header.js', 'utf8')};
    let mini = await minify(code);
    fs.writeFileSync(tg+'header_min.js', mini.code, 'utf8');
  }
  
  // index_c.js
  if (all || opt.index_c) {
    console.log('Building index_c.js...');
    let code = {
     'header.js': fs.readFileSync(src+'header.js', 'utf8'),
     'utilities.js': fs.readFileSync(src+'utilities.js', 'utf8'),
     'calendar.js': fs.readFileSync(src+'calendar.js', 'utf8'),
     'calendarData.js': fs.readFileSync(src+'calendarData.js', 'utf8'),
     'eclipse_linksM722-2202.js': fs.readFileSync(src+'eclipse_linksM722-2202.js', 'utf8'),
     'decompressSunMoonData.js': fs.readFileSync(src+'decompressSunMoonData.js', 'utf8'),
     'ancientCalendars.js': fs.readFileSync(src+'ancientCalendars.js', 'utf8'),
     'eras.js': fs.readFileSync(src+'eras.js', 'utf8'),
     'split.js': fs.readFileSync(src+'split.js', 'utf8')
     };
    let combined = await minify(code);
    fs.writeFileSync(tg+'index_c.js', combined.code, 'utf8');
  }
  
  // table_c.js
  if (all || opt.table_c) {
    console.log('Building table_c.js...');
    let code = {
     'header.js': fs.readFileSync(src+'header.js', 'utf8'),
     'utilities.js': fs.readFileSync(src+'utilities.js', 'utf8'),
     'calendarData.js': fs.readFileSync(src+'calendarData.js', 'utf8'),
     'ancientCalendars.js': fs.readFileSync(src+'ancientCalendars.js', 'utf8'),
     'eras.js': fs.readFileSync(src+'eras.js', 'utf8'),
     'split.js': fs.readFileSync(src+'split.js', 'utf8'),
     //'table_output.js': fs.readFileSync(src+'table_output.js', 'utf8'),
     'table.js': fs.readFileSync(src+'table.js', 'utf8')
     };
    let combined = await minify(code);
    fs.writeFileSync(tg+'table_c.js', combined.code, 'utf8');
  }
  
  // sunMoon_c.js
  if (all || opt.sunMoon_c) {
    console.log('Building sunMoon_c.js...');
    let code = {
     'header.js': fs.readFileSync(src+'header.js', 'utf8'),
     'decompressSunMoonData.js': fs.readFileSync(src+'decompressSunMoonData.js', 'utf8'),
     'sunMoon.js': fs.readFileSync(src+'sunMoon.js', 'utf8'),
     'sunMoonData.js': fs.readFileSync(src+'sunMoonData.js', 'utf8'),
     'eclipse_linksM3502-3502.js': fs.readFileSync(src+'eclipse_linksM3502-3502.js', 'utf8'),
     'utilities.js': fs.readFileSync(src+'utilities.js', 'utf8')
     };
    let combined = await minify(code);
    fs.writeFileSync(tg+'sunMoon_c.js', combined.code, 'utf8');  
  }
  
  // Julian_c.js
  if (all || opt.Julian_c) {
    console.log('Building Julian_c.js...');
    let code = {
     'header.js': fs.readFileSync(src+'header.js', 'utf8'),
     'Julian.js': fs.readFileSync(src+'Julian.js', 'utf8')
     };
    let combined = await minify(code);
    fs.writeFileSync(tg+'Julian_c.js', combined.code, 'utf8');
  }
  
  // 12 html files
  let files = ['index', 'index_chinese', 'index_simp', 
               'table_period', 'table_period_chinese', 'table_period_simp',
               'sunMoon', 'sunMoon_chinese', 'sunMoon_simp',
               'Julian', 'Julian_chinese', 'Julian_simp'];
  files.forEach(async function(f, ind) {
    if (!all && !opt[f]) {
      return;
    }
    console.log('Building '+f+'.html...');
    let css = (f.match(/(_chinese|_simp)$/) ? 'calendar_chinese':'calendar');
    let js; 
    if (f.substring(0,5)=='index') {
      js = '"index_c.js"';
    } else if (f.substring(0,5)=='table') {
      js = '"table_c.js"';
    } else if (f.substring(0,7)=='sunMoon') {
      js = '"sunMoon_c.js"';
    } else {
      js = '"Julian_c.js"';
    }
    let html = fs.readFileSync(src+f+'.html', 'utf8');
    html = html.replace(/<script src.*<\/script>/g,'');
    html = html.replace(css+'.css',css+'_min.css');
    html = html.replace('</head>', '<script src='+js+'></script></head>');
    let html_min = await ht.minify(html, html_minifier_option);
    fs.writeFileSync(tg+f+'.html', html_min, 'utf8');
   });
  
  // Other html files
  files = ['era_names', 'era_names_simp', 'solarTerms', 'solarTerms_chinese', 
           'table', 'table_chinese', 'table_simp',
           'solarTerms_simp', 'sexagenary', 'sexagenary_chinese', 'sexagenary_simp',
           'rules', 'rules_chinese', 'rules_simp', 'examples', 'examples_chinese',
           'examples_simp', 'rules_demysterified', 'rules_demysterified_chinese',
           'rules_demysterified_simp', 'computation', 'computation_chinese', 
           'computation_simp', '3500Calendars_errors', '3500Calendars_errors_simp',
           'chunqiu', 'chunqiu_chinese', 'chunqiu_simp',
           'guliuli', 'guliuli_chinese', 'guliuli_simp', 'QinHanCalendars',
           'QinHanCalendars_chinese', 'QinHanCalendars_simp', 'QinHanSolarTerms', 
           'QinHanSolarTerms_chinese', 'QinHanSolarTerms_simp', 'Shangyuan', 
           'Shangyuan_chinese', 'Shangyuan_simp', 'MingCalendar', 'MingCalendar_chinese',
           'MingCalendar_simp', 'MingCalendar_index', 
           'ThreeKingdoms_calendars', 'ThreeKingdoms_calendars_chinese',
           'ThreeKingdoms_calendars_simp', 'LiaoJinYuan_calendars', 
           'LiaoJinYuan_calendars_chinese', 'LiaoJinYuan_calendars_simp', 'others', 
           'others_chinese', 'others_simp', 'NorthSouth_calendars', 
           'NorthSouth_calendars_chinese', 'NorthSouth_calendars_simp', 
           'SouthernMingCalendar', 'SouthernMingCalendar_chinese', 'SouthernMingCalendar_simp',
           'QingSouthernMingZheng_calendars', 'QingSouthernMingZheng_calendars_chinese', 
           'QingSouthernMingZheng_calendars_simp', 'N1676_Zheng', 'N1676_Zheng_chinese', 
           'N1676_Zheng_simp', 'N1677_Zheng', 'N1677_Zheng_chinese', 'N1677_Zheng_simp', 
           'N1671_Zheng', 'N1671_Zheng_chinese', 'N1671_Zheng_simp', 'faq', 'faq_chinese',
           'faq_simp'];
  files.forEach(async function(f, ind) {
    if (!all && !opt[f]) {
      return;
    }
    console.log('Building '+f+'.html...');
    let css = (f.match(/(_chinese|_simp)$/) ? 'calendar_chinese':'calendar');
    if (f=='era_names' || f=='3500Calendars_errors' || f=='MingCalendar_index') { 
       css = 'calendar_chinese';
    }
    let html = fs.readFileSync(src+f+'.html', 'utf8');
    html = html.replace(css+'.css',css+'_min.css').replace('header.js','header_min.js');
    let html_min = await ht.minify(html, html_minifier_option);
    fs.writeFileSync(tg+f+'.html', html_min, 'utf8');
   });

  // Calendar quiz
  if (all || opt.simpleQuiz_js) {
    fs.copyFile(src+'simpleQuiz.js', tg+'simpleQuiz.js', err => {if (err) throw err;});
  }
  files = ['simpleQuiz', 'simpleQuiz_chinese', 'simpleQuiz_simp'];
  files.forEach(async function(f, ind) {
    if (!all && !opt[f]) {
      return;
    }
    console.log('Building '+f+'.html...');
    let css = (f.match(/(_chinese|_simp)$/) ? 'calendar_chinese':'calendar');
    let html = fs.readFileSync(src+f+'.html', 'utf8');
    html = html.replace(css+'.css',css+'_min.css').replace('<script type="module" src="simpleQuiz.mjs"></script>', '<script src="simpleQuiz.js"></script>');
    let html_min = await ht.minify(html, html_minifier_option);
    fs.writeFileSync(tg+f+'.html', html_min, 'utf8');
  });
}

async function run_build() {
  await build();
  console.log('Done.\nOutput directory: '+tg);
}

run_build();

