//
//  WidgetModels.swift
//  Chinendar
//
//  Created by Leo Liu on 9/3/23.
//

import WidgetKit
import AppIntents

protocol ChinendarWidgetConfigIntent: AppIntent, WidgetConfigurationIntent {
    var calendarConfig: ConfigIntent? { get set }
}

protocol ChinendarEntry: Sendable {
    associatedtype Intent: ChinendarWidgetConfigIntent
    var chineseCalendar: ChineseCalendar { get }
    init(configuration: Intent, chineseCalendar: ChineseCalendar, watchLayout: WatchLayout)
}

func generateEntries<Entry: TimelineEntry & ChinendarEntry, Intent: WidgetConfigurationIntent>(baseChineseCalendar: ChineseCalendar, timeline: [Date], watchLayout: WatchLayout, calendarConfig: CalendarConfigure, configuration: Intent) async -> [Entry] where Entry.Intent == Intent {
    var entries: [Entry] = [Entry(configuration: configuration, chineseCalendar: baseChineseCalendar, watchLayout: watchLayout)]
    await withTaskGroup { group in
        for date in timeline {
            group.addTask {
                var newCalendar = baseChineseCalendar
                await newCalendar.update(time: date, location: calendarConfig.location())
                return Entry(configuration: configuration, chineseCalendar: newCalendar, watchLayout: watchLayout)
            }
        }
        for await result in group {
            entries.append(result)
        }
    }
    entries.sort { $0.date < $1.date }
    return entries
}
