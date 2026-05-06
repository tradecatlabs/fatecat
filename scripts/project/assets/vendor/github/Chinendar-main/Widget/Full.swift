//
//  Full.swift
//  iOSWidgetExtension
//
//  Created by Leo Liu on 5/9/23.
//

import AppIntents
import SwiftUI
import WidgetKit

struct FullWatchConfiguration: ChinendarWidgetConfigIntent {
    static let title: LocalizedStringResource = "WGT_FULL_WATCH"
    static let description = IntentDescription("WGT_FULL_WATCH_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent?

    @Parameter(title: "BACK_GREYNESS", default: 0, controlStyle: .slider, inclusiveRange: (0, 1))
    var backAlpha: Double

    static var parameterSummary: some ParameterSummary {
        Summary {
            \.$calendarConfig
            \.$backAlpha
        }
    }
}

struct FullWatchProvider: ChinendarAppIntentTimelineProvider {
    typealias Entry = FullWatchEntry
    typealias Intent = FullWatchConfiguration

    func compactCalendar(context: Context) -> Bool {
#if os(visionOS)
        return true
#else
        return context.family != .systemLarge
#endif
    }

    func nextEntryDates(chineseCalendar: ChineseCalendar, config: FullWatchConfiguration, context: Context) -> [Date] {
        return chineseCalendar.nextQuarters(count: 10)
    }

    func relevances() async -> WidgetRelevance<Intent> {
        let asyncModels = await AsyncLocalModels()

        var relevantIntents = [WidgetRelevanceAttribute<Entry.Intent>]()

        for date in asyncModels.chineseCalendar.nextHours(count: 5) {
            let config = Intent()
            let relevantContext = RelevantContext.date(range: (date - 900)...(date + 600), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        return WidgetRelevance(relevantIntents)
    }
}

struct FullWatchEntry: TimelineEntry, ChinendarEntry {
    let date: Date
    let configuration: FullWatchProvider.Intent
    let chineseCalendar: ChineseCalendar
    let watchLayout: WatchLayout

    init(configuration: FullWatchProvider.Intent, chineseCalendar: ChineseCalendar, watchLayout: WatchLayout) {
        date = chineseCalendar.time
        self.configuration = configuration
        self.chineseCalendar = chineseCalendar
        self.watchLayout = watchLayout
    }
}

struct FullWidgetEntryView: View {
    @Environment(\.widgetFamily) var widgetFamily
    var entry: FullWatchProvider.Entry
    var backColor: Color {
        Color.gray.opacity(entry.configuration.backAlpha)
    }

    var body: some View {
#if os(visionOS)
        let isLarge = false
#else
        let isLarge = widgetFamily == .systemLarge
#endif
        Watch(displaySubquarter: false, displaySolarTerms: isLarge, compact: !isLarge, watchLayout: entry.watchLayout, markSize: 1.0, chineseCalendar: entry.chineseCalendar, highlightType: .alwaysOn, widthScale: isLarge ? 0.8 : 1.0)
            .containerBackground(backColor, for: .widget)
            .padding(5)
    }
}

struct FullWatchWidget: Widget {
    static let kind: String = "Large"
    static let supportedFamilies: [WidgetFamily] = [.systemSmall, .systemLarge]

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: Self.kind, intent: FullWatchProvider.Intent.self, provider: FullWatchProvider()) { entry in
            FullWidgetEntryView(entry: entry)
        }
        .contentMarginsDisabled()
        .containerBackgroundRemovable()
        .configurationDisplayName("WGT_FULL_WATCH")
        .description("WGT_FULL_WATCH_MSG")
        .supportedFamilies(Self.supportedFamilies)
#if os(visionOS) || os(iOS)
        .supportedMountingStyles([.elevated, .recessed])
#endif
    }
}

#Preview("Small", as: .systemSmall, using: {
    let intent = FullWatchProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.backAlpha = 0.2
    return intent
}(), widget: {
    FullWatchWidget()
}, timelineProvider: {
    FullWatchProvider()
})

#if os(macOS) || os(iOS)
#Preview("Large", as: .systemLarge, using: {
    let intent = FullWatchProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.backAlpha = 0.2
    return intent
}(), widget: {
    FullWatchWidget()
}, timelineProvider: {
    FullWatchProvider()
})
#endif
