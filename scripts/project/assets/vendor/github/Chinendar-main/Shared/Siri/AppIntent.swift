//
//  AppIntent.swift
//  Chinendar
//
//  Created by Leo Liu on 8/6/24.
//

import AppIntents
import SwiftUI
import Foundation

struct ChinendarDate: AppIntent {
    static let title = LocalizedStringResource("CHINENDAR_DATE_LOOKUP")
    static let description = IntentDescription("CHINENDAR_DATE_LOOKUP_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent
    @Parameter(title: "DATE_TO_LOOKUP")
    var queryDate: Date

    static var parameterSummary: some ParameterSummary {
        Summary("LOOKUP\(\.$queryDate)") {
            \.$calendarConfig
            \.$queryDate
        }
    }

    func perform() async throws -> some IntentResult & ReturnsValue<String> & ProvidesDialog & ShowsSnippetView {
        let asyncModels = await AsyncConfigModels(configIntent: calendarConfig)
        var chineseCalendar = asyncModels.chineseCalendar
        chineseCalendar.update(time: queryDate)
        let calendarString = if chineseCalendar.holidays.count > 0 {
            "\(chineseCalendar.dateString) \(chineseCalendar.holidays.joined(separator: " ")) \(chineseCalendar.timeString)"
        } else {
            "\(chineseCalendar.dateString) \(chineseCalendar.timeString)"
        }

        return .result(value: calendarString, dialog: IntentDialog(full: "MONTH\(chineseCalendar.monthStringLocalized)DAY\(chineseCalendar.dayStringLocalized)HOLIDAY\(Locale.translate(chineseCalendar.holidays.first ?? ""))HOUR\(chineseCalendar.hourStringLocalized)QUARTER\(chineseCalendar.quarterStringLocalized)", supporting: "LOOKUP_RESULT_PROMPT", systemImageName: "calendar.badge.clock")) {
            Text(String(calendarString.reversed()))
                .font(.system(size: 21, weight: .bold, design: .rounded))
                .foregroundStyle(.primary)
                .minimumScaleFactor(0.5)
                .padding()
        }
    }
}

struct ChinendarDateLookup: AppIntent {
    static let title = LocalizedStringResource("CHINENDAR_DATE_REVERSE_LOOKUP")
    static let description = IntentDescription("CHINENDAR_DATE_REVERSE_LOOKUP_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent
    @Parameter(title: "YEAR_OFFSET", default: 0, inclusiveRange: (-5, 5))
    var yearOffset: Int
    @Parameter(title: "MONTH", inclusiveRange: (1, 12))
    var month: Int
    @Parameter(title: "DAY", inclusiveRange: (1, 30))
    var day: Int
    @Parameter(title: "PREFER_LEAP_MONTH", default: false)
    var preferLeapMonth: Bool

    static var parameterSummary: some ParameterSummary {
        Summary("FIND_MONTH\(\.$month)DAY\(\.$day)") {
            \.$calendarConfig
            \.$yearOffset
            \.$month
            \.$day
            \.$preferLeapMonth
        }
    }

    func perform() async throws -> some IntentResult & ReturnsValue<Date?> & ProvidesDialog & ShowsSnippetView {
        let asyncModels = await AsyncConfigModels(configIntent: calendarConfig)
        var chineseCalendar = asyncModels.chineseCalendar
        if yearOffset > 0 {
            for _ in 0..<yearOffset {
                if let newDate = chineseCalendar.nextYear() {
                    chineseCalendar.update(time: newDate)
                }
            }
        } else if yearOffset < 0 {
            for _ in 0..<(-yearOffset) {
                if let newDate = chineseCalendar.previousYear() {
                    chineseCalendar.update(time: newDate)
                }
            }
        }

        if let date = chineseCalendar.find(chineseDate: .init(month: month, day: day, leap: preferLeapMonth))?.startOfDay {
            let dateFormatter = DateFormatter()
            dateFormatter.timeStyle = .none
            return .result(value: date, dialog: IntentDialog(full: "DATE_FOUND_IS\(dateFormatter.string(from: date))", supporting: "REVERSE_LOOKUP_RESULT_PROMPT", systemImageName: "calendar.badge.clock")) {
                Text(date, style: .date)
                    .font(.system(size: 21, weight: .bold, design: .rounded))
                    .foregroundStyle(.primary)
                    .minimumScaleFactor(0.5)
                    .padding()
            }
        } else {
            return .result(value: nil, dialog: IntentDialog(full: "DATE_NOT_FOUND", supporting: "REVERSE_LOOKUP_RESULT_PROMPT", systemImageName: "calendar.badge.exclamationmark")) {
                Text("DATE_NOT_FOUND")
                    .font(.system(size: 21, weight: .bold, design: .rounded))
                    .foregroundStyle(.secondary)
                    .minimumScaleFactor(0.5)
                    .padding()
            }
        }
    }
}

struct NextEvent: AppIntent {
    static let title = LocalizedStringResource("NEXT_EVENT")
    static let description = IntentDescription("NEXT_EVENT_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent
    @Parameter(title: "EVENT_TYPE")
    var nextEventType: NextEventType

    static var parameterSummary: some ParameterSummary {
        Summary("NEXT\(\.$nextEventType)") {
            \.$calendarConfig
            \.$nextEventType
        }
    }

    func perform() async throws -> some IntentResult & ReturnsValue<Date?> & ProvidesDialog & ShowsSnippetView {
        let asyncModels = await AsyncConfigModels(configIntent: calendarConfig)
        let (_, nextDate) = next(nextEventType, in: asyncModels.chineseCalendar)

        let dialog = if let nextDate {
            IntentDialog(full: "NEXT_EVENT\(Locale.translate(nextDate.name))IS_ON:\(nextDate.date.description(with: .current))", supporting: "NEXT_EVENT_RESULT_FOR:\(nextEventType.localizedStringResource)", systemImageName: "clock")
        } else {
            IntentDialog(full: "NEXT_EVENT\(nextEventType.localizedStringResource)UNAVAILABLE", supporting: "NEXT_EVENT_RESULT_FOR:\(nextEventType.localizedStringResource)", systemImageName: "clock")
        }

        return .result(value: nextDate?.date, dialog: dialog) {
            if let nextDate {
                NextEventView(nextDate: nextDate)
                    .padding()
            } else {
                Text("NEXT_EVENT\(nextEventType.localizedStringResource)UNAVAILABLE")
                    .font(.title)
                    .padding()
            }
        }
    }
}

struct NextEventView: View {
    let nextDate: ChineseCalendar.NamedDate

    var body: some View {
        VStack(spacing: 5) {
            Text(Locale.translate(nextDate.name))
                .lineLimit(1)
                .font(.system(size: 18, weight: .bold, design: .rounded))
                .minimumScaleFactor(0.5)
            Text(nextDate.date.formatted(date: .abbreviated, time: .shortened))
                .lineLimit(1)
                .font(.system(size: 24, weight: .bold, design: .rounded))
                .minimumScaleFactor(0.5)
        }
        .foregroundStyle(.primary)
    }
}

#Preview {
    let nextDate = ChineseCalendar.NamedDate(name: "大暑", date: Date.now + 23048)
    NextEventView(nextDate: nextDate)
}
