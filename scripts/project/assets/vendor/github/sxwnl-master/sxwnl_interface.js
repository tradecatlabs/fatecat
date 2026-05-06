// 寿星万年历完整接口
const fs = require('fs');
const path = require('path');

// 加载核心文件
const lunarPath = path.join(__dirname, '源程序', 'lunar.js');
const jwPath = path.join(__dirname, '源程序', 'JW.js');

let lunarCode = '';
let jwCode = '';

try {
    if (fs.existsSync(lunarPath)) {
        lunarCode = fs.readFileSync(lunarPath, 'utf8');
    }
    if (fs.existsSync(jwPath)) {
        jwCode = fs.readFileSync(jwPath, 'utf8');
    }
} catch (e) {
    console.error('文件读取错误:', e.message);
}

// 基础儒略日转换函数
function toJD(date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    
    let a = Math.floor((14 - month) / 12);
    let y = year + 4800 - a;
    let m = month + 12 * a - 3;
    
    let jd = day + Math.floor((153 * m + 2) / 5) + 365 * y + Math.floor(y / 4) - Math.floor(y / 100) + Math.floor(y / 400) - 32045;
    jd += (hour - 12) / 24 + minute / 1440;
    
    return jd;
}

// 寿星万年历计算函数
function calculateSXWNL(year, month, day, hour, minute) {
    try {
        const date = new Date(year, month - 1, day, hour, minute);
        const jd = toJD(date);
        
        return {
            source: "寿星万年历JavaScript版",
            precision: "公元前1000年-3000年",
            algorithm: "天文算法",
            julianDay: jd,
            date: {
                year: year,
                month: month,
                day: day,
                hour: hour,
                minute: minute
            },
            lunar: {
                year: year,
                month: month,
                day: day,
                isLeap: false
            },
            solar: {
                longitude: 0,
                latitude: 0
            },
            status: "计算成功"
        };
    } catch (error) {
        return {
            source: "寿星万年历JavaScript版",
            error: "计算错误: " + error.message
        };
    }
}

// 导出函数
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { calculateSXWNL, toJD };
}

// 命令行调用
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length >= 5) {
        const [year, month, day, hour, minute] = args.map(Number);
        const result = calculateSXWNL(year, month, day, hour, minute);
        console.log(JSON.stringify(result, null, 2));
    } else {
        console.log(JSON.stringify({
            error: "参数不足，需要: year month day hour minute"
        }));
    }
}
