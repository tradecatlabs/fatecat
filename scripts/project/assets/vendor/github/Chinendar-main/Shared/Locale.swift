//
//  Locale.swift
//  Chinendar
//
//  Created by Leo Liu on 8/18/23.
//

import Foundation

extension Locale {
    static var isEastAsian: Bool {
        let languages = Locale.preferredLanguages
        var isEastAsian = true
        for language in languages {
            let flag = language[language.startIndex..<language.index(language.startIndex, offsetBy: 2)]
            if flag == "en" {
                isEastAsian = false
                break
            } else if ["zh", "ko", "ja"].contains(flag) {
                isEastAsian = true
                break
            }
        }
        return isEastAsian
    }

    private static let translation: [String: LocalizedStringResource] = [
        "夜中": "MID_NIGHT", "日出": "SUNRISE", "日中": "NOON", "日入": "SUNSET",
        "月出": "MOONRISE", "月中": "LUNAR_NOON", "月入": "MOONSET",
        "朔": "NEW_MOON", "望": "FULL_MOON",
        "冬至": "ST0", "大寒": "ST2", "雨水": "ST4", "春分": "ST6", "穀雨": "ST8", "小滿": "ST10", "夏至": "ST12", "大暑": "ST14", "處暑": "ST16", "秋分": "ST18", "霜降": "ST20", "小雪": "ST22",
        "小寒": "ST1", "立春": "ST3", "驚蟄": "ST5", "清明": "ST7", "立夏": "ST9", "芒種": "ST11", "小暑": "ST13", "立秋": "ST15", "白露": "ST17", "寒露": "ST19", "立冬": "ST21", "大雪": "ST23",
        "辰星": "MERCURY", "太白": "VENUS", "熒惑": "MARS", "歲星": "JUPYTER", "填星": "SATURN", "太陰": "MOON",
        "元旦": "CH_1_1", "上元": "CH_1_15", "春社": "CH_2_2", "上巳": "CH_3_3", "端午": "CH_5_5", "七夕": "CH_7_7", "中元": "CH_7_15", "中秋": "CH_8_15", "重陽": "CH_9_9", "下元": "CH_10_15", "臘祭": "CH_12_8", "除夕": "CH_12_30"
    ]

    static func translate(_ original: String) -> String {
        var processed = original
        if ChineseCalendar.oddSolarTermChinese.contains(processed) || ChineseCalendar.evenSolarTermChinese.contains(processed) {
            processed = processed.replacingOccurrences(of: "　", with: "")
        }
        return if let translated = translation[processed] {
            String(localized: translated)
        } else {
            processed
        }
    }
}
