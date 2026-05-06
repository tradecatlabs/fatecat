//
//  WatchWidget.swift
//  WatchWidget
//
//  Created by Leo Liu on 5/10/23.
//

import AppIntents
import SwiftUI
import WidgetKit

enum TextWidgetSeparator: String, AppEnum {
    static let typeDisplayRepresentation: TypeDisplayRepresentation = .init(name: "SEPARATOR")
    case space = " ", dot = "・", none = ""
    static let caseDisplayRepresentations: [TextWidgetSeparator: DisplayRepresentation] = [
        .none: .init(title: "NONE"),
        .dot: .init(title: "・"),
        .space: .init(title: "SPACE")
    ]
}

enum TextWidgetTime: String, AppEnum {
    static let typeDisplayRepresentation: TypeDisplayRepresentation = .init(name: "TIME_STRING_LEVEL")
    case none, hour, hourAndQuarter
    static let caseDisplayRepresentations: [TextWidgetTime: DisplayRepresentation] = [
        .none: .init(title: "NONE"),
        .hour: .init(title: "HOUR_ONLY"),
        .hourAndQuarter: .init(title: "HOUR_QUARTER")
    ]
    var displayHour: Bool {
        self == .hour || self == .hourAndQuarter
    }
    var displayQuarter: Bool {
        self == .hourAndQuarter
    }
}

struct TextConfiguration: ChinendarWidgetConfigIntent {
    static let title: LocalizedStringResource = "WGT_TEXT"
    static let description = IntentDescription("WGT_TEXT_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent?
    @Parameter(title: "DATE", default: true)
    var date: Bool
    @Parameter(title: "TIME_STRING_LEVEL", default: .hour)
    var time: TextWidgetTime
    @Parameter(title: "NUMBER_OF_HOLIDAY", default: 1, controlStyle: .stepper, inclusiveRange: (0, 2))
    var holidays: Int
    @Parameter(title: "SEPARATOR", default: .space)
    var separator: TextWidgetSeparator

    static var parameterSummary: some ParameterSummary {
        Summary {
            \.$calendarConfig
            \.$date
            \.$time
            \.$holidays
            \.$separator
        }
    }
}

struct TextProvider: ChinendarAppIntentTimelineProvider {
    typealias Intent = TextConfiguration
    typealias Entry = TextEntry

    func nextEntryDates(chineseCalendar: ChineseCalendar, config: TextConfiguration, context: Context) -> [Date] {
        switch config.time {
        case .hour, .none:
            return chineseCalendar.nextHours(count: 12)
        case .hourAndQuarter:
            return chineseCalendar.nextQuarters(count: 12)
        }
    }

    func recommendations() -> [AppIntentRecommendation<Intent>] {
        let datetimeHoliday = Intent()
        let datetime = Intent()
        datetime.holidays = 0
        datetime.time = .hourAndQuarter
        let dateholiday = Intent()
        dateholiday.time = .none
        return [
            AppIntentRecommendation(intent: datetimeHoliday, description: "DATE_HOLIDAY_TIME"),
            AppIntentRecommendation(intent: datetime, description: "DATE_TIME"),
            AppIntentRecommendation(intent: dateholiday, description: "DATE_HOLIDAY")
        ]
    }

    func relevances() async -> WidgetRelevance<Intent> {
        let asyncModels = await AsyncLocalModels()

        var relevantIntents = [WidgetRelevanceAttribute<Entry.Intent>]()

        for date in asyncModels.chineseCalendar.nextHours(count: 6) {
            let config = Intent()
            config.time = .hour
            let relevantContext = RelevantContext.date(range: (date - 900)...(date + 600), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        for date in [asyncModels.chineseCalendar.startOfNextDay] {
            let config = Intent()
            config.time = .none
            let relevantContext = RelevantContext.date(range: (date - 3600)...(date + 900), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        return WidgetRelevance(relevantIntents)
    }
}

struct TextEntry: TimelineEntry, ChinendarEntry {
    let date: Date
    let displayDate: Bool
    let displayTime: TextWidgetTime
    let DisplayHolidays: Int
    let separator: String
    let chineseCalendar: ChineseCalendar

    init(configuration: TextProvider.Intent, chineseCalendar: ChineseCalendar, watchLayout: WatchLayout) {
        self.date = chineseCalendar.time
        self.displayDate = configuration.date
        self.displayTime = configuration.time
        self.DisplayHolidays = configuration.holidays
        self.separator = configuration.separator.rawValue
        self.chineseCalendar = chineseCalendar
    }
}

struct TextEntryView: View {
    var entry: TextProvider.Entry

    var body: some View {
        LineDescription(chineseCalendar: entry.chineseCalendar, displayDate: entry.displayDate, displayHour: entry.displayTime.displayHour, displayQuarter: entry.displayTime.displayQuarter, displayHolidays: entry.DisplayHolidays, separator: entry.separator)
            .containerBackground(Color.clear, for: .widget)
    }
}

struct LineWidget: Widget {
    static let kind: String = "Date String"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: Self.kind, intent: TextProvider.Intent.self, provider: TextProvider()) { entry in
            TextEntryView(entry: entry)
        }
        .containerBackgroundRemovable()
        .configurationDisplayName("WGT_TEXT")
        .description("WGT_TEXT_MSG")
        .supportedFamilies([.accessoryInline])
    }
}

#Preview("Inline", as: .accessoryInline, using: {
    let intent = TextProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    return intent
}()) {
    LineWidget()
} timelineProvider: {
    TextProvider()
}
