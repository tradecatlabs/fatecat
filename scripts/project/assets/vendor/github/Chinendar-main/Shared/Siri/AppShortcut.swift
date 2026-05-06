//
//  AppShortcut.swift
//  Chinendar
//
//  Created by Leo Liu on 8/8/24.
//

import AppIntents

struct ChinendarShortcut: AppShortcutsProvider {
    static let shortcutTileColor = ShortcutTileColor.red

    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: OpenApp(),
            phrases: [
                "打開\(.applicationName)",
                "打开\(.applicationName)",
                "Open \(.applicationName)",
                "\(.applicationName)を開く",
                "\(.applicationName) 열기",
                "打開\(\.$calendarConfig)\(.applicationName)",
                "打开\(\.$calendarConfig)\(.applicationName)",
                "Open \(\.$calendarConfig) \(.applicationName)",
                "\(\.$calendarConfig)の\(.applicationName)を開く",
                "\(\.$calendarConfig) \(.applicationName) 열기"
            ],
            shortTitle: "LAUNCH_CHINENDAR",
            systemImageName: "watchface.applewatch.case"
        )

        AppShortcut(
            intent: ChinendarDate(),
            phrases: [
                "這是\(.applicationName)幾號？",
                "这是\(.applicationName)几号？",
                "What date is it in \(.applicationName)?",
                "この日付は\(.applicationName)で何ですか？",
                "이 날짜가 \(.applicationName) 몇 호인가요?",
                "\(.applicationName)日期",
                "\(.applicationName) date",
                "\(.applicationName)の日付",
                "\(.applicationName) 날짜"
            ],
            shortTitle: "CHINENDAR_DATE_LOOKUP",
            systemImageName: "calendar"
        )

        AppShortcut(
            intent: NextEvent(),
            phrases: [
                "\(.applicationName)下一個時間",
                "\(.applicationName)下一个时间",
                "\(.applicationName) next event",
                "\(.applicationName)の次の時間",
                "\(.applicationName) 다음 시간",
                "\(.applicationName)下一個\(\.$nextEventType)",
                "\(.applicationName)下一个\(\.$nextEventType)",
                "\(.applicationName) next \(\.$nextEventType)",
                "\(.applicationName)の次の\(\.$nextEventType)",
                "\(.applicationName) 다음 \(\.$nextEventType)",
                "\(.applicationName)下一個\(\.$nextEventType)時間",
                "\(.applicationName)下一个\(\.$nextEventType)时间",
                "\(.applicationName) next time of \(\.$nextEventType)",
                "\(.applicationName)の次の\(\.$nextEventType)の時間",
                "\(.applicationName) 다음 \(\.$nextEventType) 시간"
            ],
            shortTitle: "NEXT_EVENT",
            systemImageName: "gauge.with.needle"
        )
    }
}
