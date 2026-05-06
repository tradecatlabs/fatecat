//
//  Card.swift
//  Chinendar
//
//  Created by Leo Liu on 1/21/24.
//

import AppIntents
import SwiftUI
import WidgetKit

struct CardConfiguration: ChinendarWidgetConfigIntent {
    static let title: LocalizedStringResource = "WGT_CARD"
    static let description = IntentDescription("WGT_CARD_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent?

    static var parameterSummary: some ParameterSummary {
        Summary {
            \.$calendarConfig
        }
    }
}

struct CardProvider: ChinendarAppIntentTimelineProvider {
    typealias Intent = CardConfiguration
    typealias Entry = CardEntry

    func nextEntryDates(chineseCalendar: ChineseCalendar, config: CardConfiguration, context: Context) -> [Date] {
        return chineseCalendar.nextQuarters(count: 12)
    }

    func recommendations() -> [AppIntentRecommendation<Intent>] {
        return [
            AppIntentRecommendation(intent: Intent(), description: "CHINENDAR")
        ]
    }

    func relevances() async -> WidgetRelevance<Intent> {
        let asyncModels = await AsyncLocalModels()

        var relevantIntents = [WidgetRelevanceAttribute<Entry.Intent>]()

        for date in asyncModels.chineseCalendar.nextHours(count: 6) {
            let config = Intent()
            let relevantContext = RelevantContext.date(range: (date - 900)...(date + 600), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        return WidgetRelevance(relevantIntents)
    }
}

struct CardEntry: TimelineEntry, ChinendarEntry {
    let date: Date
    let chineseCalendar: ChineseCalendar
    let watchLayout: WatchLayout
    var baseLayout: BaseLayout {
        watchLayout.baseLayout
    }

    init(configuration: CardProvider.Intent, chineseCalendar: ChineseCalendar, watchLayout: WatchLayout) {
        self.date = chineseCalendar.time
        self.chineseCalendar = chineseCalendar
        self.watchLayout = watchLayout
    }
}

struct CardEntryView: View {
    var entry: CardProvider.Entry

    var body: some View {
        let chineseCalendar = entry.chineseCalendar
        CalendarBadge(dateString: chineseCalendar.dateString, timeString: chineseCalendar.hourString + chineseCalendar.shortQuarterString, color: entry.baseLayout.colors.centerFontColor.apply(startingAngle: 0), centerFont: WatchFont(entry.watchLayout.centerFont))
            .containerBackground(Color(cgColor: entry.baseLayout.colors.innerColor.light.cgColor), for: .widget)
    }
}

struct DateCardWidget: Widget {
    static let kind: String = "Date Card"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: Self.kind, intent: CardProvider.Intent.self, provider: CardProvider()) { entry in
            CardEntryView(entry: entry)
        }
        .contentMarginsDisabled()
        .containerBackgroundRemovable()
        .configurationDisplayName("WGT_CARD")
        .description("WGT_CARD_MSG")
        .supportedFamilies([.accessoryRectangular])
    }
}

#Preview("Card", as: .accessoryRectangular, using: {
    let intent = CardProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    return intent
}()) {
    DateCardWidget()
} timelineProvider: {
    CardProvider()
}
