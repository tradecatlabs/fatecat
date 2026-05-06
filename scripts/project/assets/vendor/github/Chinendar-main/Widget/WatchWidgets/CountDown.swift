//
//  CountDown.swift
//  Chinendar
//
//  Created by Leo Liu on 6/28/23.
//

import AppIntents
import SwiftUI
import WidgetKit

struct CountDownConfiguration: ChinendarWidgetConfigIntent {
    static let title: LocalizedStringResource = "WGT_COUNTDOWN"
    static let description = IntentDescription("WGT_COUNTDOWN_MSG")

    @Parameter(title: "SELECT_CALENDAR")
    var calendarConfig: ConfigIntent?
    @Parameter(title: "EVENT_TYPE", default: .solarTerms)
    var target: NextEventType

    static var parameterSummary: some ParameterSummary {
        Summary {
            \.$calendarConfig
            \.$target
        }
    }
}

struct CountDownProvider: ChinendarAppIntentTimelineProvider {
    typealias Entry = CountDownEntry
    typealias Intent = CountDownConfiguration

    func nextEntryDates(chineseCalendar: ChineseCalendar, config: CountDownConfiguration, context: Context) -> [Date] {
        let allTimes = switch config.target {
        case .moonriseSet:
            nextMoonTimes(chineseCalendar: chineseCalendar)
        case .sunriseSet:
            nextSunTimes(chineseCalendar: chineseCalendar)
        case .lunarPhases:
            nextMoonPhase(chineseCalendar: chineseCalendar)
        case .solarTerms:
            nextSolarTerm(chineseCalendar: chineseCalendar)
        case .chineseHoliday:
            nextChineseHoliday(chineseCalendar: chineseCalendar)
        }
        return if allTimes.count > 0 {
            allTimes
        } else {
            [chineseCalendar.startOfNextDay]
        }
    }

    func recommendations() -> [AppIntentRecommendation<Intent>] {
        let solarTerms = { let intent = Intent(); intent.target = .solarTerms; return intent }()
        let lunarPhases = { let intent = Intent(); intent.target = .lunarPhases; return intent }()
        let chineseHoliday = { let intent = Intent(); intent.target = .chineseHoliday; return intent }()
        let sunriseSet = { let intent = Intent(); intent.target = .sunriseSet; return intent }()
        let moonriseSet = { let intent = Intent(); intent.target = .moonriseSet; return intent }()

        return [
            AppIntentRecommendation(intent: solarTerms, description: "ET_ST"),
            AppIntentRecommendation(intent: lunarPhases, description: "ET_MP"),
            AppIntentRecommendation(intent: chineseHoliday, description: "ET_HOLIDAY"),
            AppIntentRecommendation(intent: sunriseSet, description: "SUNRISE_SET"),
            AppIntentRecommendation(intent: moonriseSet, description: "MOONRISE_SET")
        ]
    }

    func relevances() async -> WidgetRelevance<Intent> {
        let asyncModels = await AsyncLocalModels()

        async let sunTimes = nextSunTimes(chineseCalendar: asyncModels.chineseCalendar)
        async let moonTimes = nextMoonTimes(chineseCalendar: asyncModels.chineseCalendar)
        async let solarTerms = nextSolarTerm(chineseCalendar: asyncModels.chineseCalendar)
        async let moonPhases = nextMoonPhase(chineseCalendar: asyncModels.chineseCalendar)
        async let chineseHolidays = nextChineseHoliday(chineseCalendar: asyncModels.chineseCalendar)

        var relevantIntents = [WidgetRelevanceAttribute<Entry.Intent>]()

        for date in await sunTimes {
            let config = Intent()
            config.target = .sunriseSet
            let relevantContext = RelevantContext.date(range: (date - 3600)...(date + 900), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        for date in await moonTimes {
            let config = Intent()
            config.target = .moonriseSet
            let relevantContext = RelevantContext.date(range: (date - 3600)...(date + 900), kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        for date in await solarTerms {
            let config = Intent()
            config.target = .solarTerms
            var solarTermDate = asyncModels.chineseCalendar
            solarTermDate.update(time: date)
            let relevantContext = RelevantContext.date(range: solarTermDate.startOfDay...solarTermDate.startOfNextDay, kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        for date in await moonPhases {
            let config = Intent()
            config.target = .lunarPhases
            var lunarPhaseDate = asyncModels.chineseCalendar
            lunarPhaseDate.update(time: date)
            let relevantContext = RelevantContext.date(range: lunarPhaseDate.startOfDay...lunarPhaseDate.startOfNextDay, kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        for date in await chineseHolidays {
            let config = Intent()
            config.target = .chineseHoliday
            var holidayDate = asyncModels.chineseCalendar
            holidayDate.update(time: date)
            let relevantContext = RelevantContext.date(range: holidayDate.startOfDay...holidayDate.startOfNextDay, kind: .informational)
            let relevantIntent = WidgetRelevanceAttribute(configuration: config, context: relevantContext)
            relevantIntents.append(relevantIntent)
        }

        return WidgetRelevance(relevantIntents)
    }
}

struct CountDownEntry: TimelineEntry, ChinendarEntry {
    let date: Date
    let configuration: CountDownProvider.Intent
    let chineseCalendar: ChineseCalendar
    let watchLayout: WatchLayout
    let previousDate: ChineseCalendar.NamedDate?
    let nextDate: ChineseCalendar.NamedDate?
    let color: CGColor
    let barColor: CGColor

    init(configuration: CountDownProvider.Intent, chineseCalendar: ChineseCalendar, watchLayout: WatchLayout) {
        let baseLayout = watchLayout.baseLayout
        self.configuration = configuration
        self.chineseCalendar = chineseCalendar
        self.watchLayout = watchLayout

        (previousDate, nextDate) = next(configuration.target, in: chineseCalendar)

        switch configuration.target {
        case .lunarPhases:
            self.date = chineseCalendar.startOfNextDay
            if let nextDate {
                color = if nextDate.name == ChineseCalendar.moonPhases.newmoon {
                    baseLayout.colors.monthlyIndicators.newMoon.cgColor
                } else {
                    baseLayout.colors.monthlyIndicators.fullMoon.cgColor
                }
                barColor = if nextDate.name == ChineseCalendar.moonPhases.newmoon { // New moon
                    baseLayout.colors.secondRing.interpolate(at: chineseCalendar.eventInMonth.eclipse.first?.pos ?? 0.0)
                } else { // Full moon
                    baseLayout.colors.secondRing.interpolate(at: chineseCalendar.eventInMonth.fullMoon.first?.pos ?? 0.5)
                }
            } else {
                color = baseLayout.colors.monthlyIndicators.fullMoon.cgColor
                barColor = CGColor(gray: 0, alpha: 0)
            }

        case .solarTerms:
            self.date = chineseCalendar.startOfNextDay
            if let nextDate, previousDate != nil {
                let yearStart = chineseCalendar.solarTerms[0].date
                let yearEnd = chineseCalendar.solarTerms[24].date
                color = ChineseCalendar.evenSolarTermChinese.contains(nextDate.name) ? baseLayout.colors.monthlyIndicators.evenSolarTerm.cgColor : baseLayout.colors.monthlyIndicators.oddSolarTerm.cgColor
                barColor = baseLayout.colors.firstRing.interpolate(at: yearStart.distance(to: nextDate.date) / yearStart.distance(to: yearEnd))
            } else {
                color = baseLayout.colors.monthlyIndicators.evenSolarTerm.cgColor
                barColor = CGColor(gray: 0, alpha: 0)
            }

        case .chineseHoliday:
            self.date = chineseCalendar.startOfNextDay
            if let nextDate, previousDate != nil {
                let yearStart = chineseCalendar.solarTerms[0].date
                let yearEnd = chineseCalendar.solarTerms[24].date
                color = baseLayout.colors.firstRing.interpolate(at: yearStart.distance(to: nextDate.date) / yearStart.distance(to: yearEnd))
                barColor = baseLayout.colors.firstRing.colors.first ?? CGColor(gray: 0, alpha: 0)
            } else {
                color = baseLayout.colors.firstRing.colors.first ?? CGColor(gray: 1, alpha: 1)
                barColor = CGColor(gray: 0, alpha: 0)
            }

        case .moonriseSet:
            var chineseCalendar = chineseCalendar
            self.date = chineseCalendar.time + 1800 // Half Hour
            if let nextDate {
                color = if nextDate.name == ChineseCalendar.moonTimeName.moonrise {
                    baseLayout.colors.moonPositionIndicator.moonrise.cgColor
                } else {
                    baseLayout.colors.moonPositionIndicator.moonset.cgColor
                }
                barColor = if nextDate.name == ChineseCalendar.moonTimeName.moonrise { // Moonrise
                    baseLayout.colors.secondRing.interpolate(at: chineseCalendar.sunMoonPositions.lunar.moonrise?.pos ?? 0.25)
                } else { // Moonset
                    baseLayout.colors.secondRing.interpolate(at: chineseCalendar.sunMoonPositions.lunar.moonset?.pos ?? 0.75)
                }
            } else {
                color = baseLayout.colors.moonPositionIndicator.highMoon.cgColor
                barColor = CGColor(gray: 0, alpha: 0)
            }

        case .sunriseSet:
            var chineseCalendar = chineseCalendar
            self.date = chineseCalendar.time + 1800 // Half Hour
            if let nextDate {
                color = if nextDate.name == ChineseCalendar.dayTimeName.sunrise {
                    baseLayout.colors.sunPositionIndicator.sunrise.cgColor
                } else {
                    baseLayout.colors.sunPositionIndicator.sunset.cgColor
                }
                barColor = if nextDate.name == ChineseCalendar.dayTimeName.sunrise { // Sunrise
                    baseLayout.colors.thirdRing.interpolate(at: chineseCalendar.sunMoonPositions.solar.sunrise?.pos ?? 0.25)
                } else { // Sunset
                    baseLayout.colors.thirdRing.interpolate(at: chineseCalendar.sunMoonPositions.solar.sunset?.pos ?? 0.75)
                }
            } else {
                color = baseLayout.colors.sunPositionIndicator.noon.cgColor
                barColor = CGColor(gray: 0, alpha: 0)
            }
        }
    }
}

struct CountDownEntryView: View {
    var entry: CountDownEntry
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch entry.configuration.target {
        case .solarTerms:
            if let next = entry.nextDate, let previous = entry.previousDate {
                let index = findSolarTerm(next.name)
                if index >= 0 {
                    let icon = IconType.solarTerm(view: SolarTerm(angle: CGFloat(index) / 24.0, color: entry.color))

                    switch family {
                    case .accessoryRectangular:
                        RectanglePanel(icon: icon, name: Text(Locale.translate(next.name)), color: entry.color, start: previous.date, end: next.date)
                    case .accessoryCorner:
                        Curve(icon: icon, barColor: entry.barColor, start: previous.date, end: next.date)
                    default:
                        EmptyView()
                    }
                }
            }
        case .lunarPhases:
            if let next = entry.nextDate, let previous = entry.previousDate {
                let icon = IconType.moon(view: MoonPhase(angle: next.name == ChineseCalendar.moonPhases.newmoon ? 0.05 : 0.5, color: entry.color))

                switch family {
                case .accessoryRectangular:
                    RectanglePanel(icon: icon, name: Text(Locale.translate(next.name)), color: entry.color, start: previous.date, end: next.date)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor,
                          start: previous.date, end: next.date)
                default:
                    EmptyView()
                }
            }
        case .chineseHoliday:
            if let next = entry.nextDate, let previous = entry.previousDate {
                let nextDateCalendar = {
                    var calendar = entry.chineseCalendar
                    calendar.update(time: next.date)
                    return calendar
                }()
                let icon = IconType.date(view: SunMoon(month: nextDateCalendar.nominalMonth, day: nextDateCalendar.day))

                switch family {
                case .accessoryRectangular:
                    RectanglePanel(icon: icon, name: Text(Locale.translate(next.name)), color: entry.color, start: previous.date, end: next.date)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor,
                          start: previous.date, end: next.date)
                default:
                    EmptyView()
                }
            }

        case .sunriseSet:
            var chineseCalendar = entry.chineseCalendar
            let noonTime = chineseCalendar.getSunTimes(for: .current).noon
            if let next = entry.nextDate, let previous = entry.previousDate {
                let icon = IconType.sunrise(view: Sun(color: entry.color, rise: next.name == ChineseCalendar.dayTimeName.sunrise))

                switch family {
                case .accessoryRectangular:
                    RectanglePanel(icon: icon, name: Text(Locale.translate(next.name)), color: entry.color, start: previous.date, end: next.date)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor, start: previous.date, end: next.date)
                default:
                    EmptyView()
                }

            } else {
                let icon = IconType.sunrise(view: Sun(color: entry.color, rise: nil))

                switch family {
                case .accessoryRectangular:
                    let sunDescription = if entry.chineseCalendar.location != nil {
                        if noonTime != nil {
                            Text("LONG_DAY")
                        } else {
                            Text("LONG_NIGHT")
                        }
                    } else {
                        Text("SUN_UNKNOWN")
                    }
                    RectanglePanel(icon: icon, name: sunDescription, color: entry.color)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor, start: nil, end: nil)
                default:
                    EmptyView()
                }
            }
        case .moonriseSet:
            var chineseCalendar = entry.chineseCalendar
            let highMoonTime = chineseCalendar.getMoonTimes(for: .current).highMoon
            if let next = entry.nextDate, let previous = entry.previousDate {
                let icon = IconType.moon(view: MoonPhase(angle: entry.chineseCalendar.currentDayInMonth, color: entry.color, rise: next.name == ChineseCalendar.moonTimeName.moonrise))

                switch family {
                case .accessoryRectangular:
                    RectanglePanel(icon: icon, name: Text(Locale.translate(next.name)), color: entry.color, start: previous.date, end: next.date)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor,
                          start: previous.date, end: next.date)
                default:
                    EmptyView()
                }
            } else {
                let icon = IconType.moon(view: MoonPhase(angle: entry.chineseCalendar.currentDayInMonth, color: entry.color, rise: nil))

                switch family {
                case .accessoryRectangular:
                    let moonDescription = if entry.chineseCalendar.location != nil {
                        if highMoonTime != nil {
                            Text("LONG_MOON")
                        } else {
                            Text("MOONLESS")
                        }
                    } else {
                        Text("MOON_UNKNOWN")
                    }
                    RectanglePanel(icon: icon, name: moonDescription, color: entry.color)
                case .accessoryCorner:
                    Curve(icon: icon, barColor: entry.barColor,
                          start: nil, end: nil)
                default:
                    EmptyView()
                }
            }
        }
    }

    private func findSolarTerm(_ solarTerm: String) -> Int {
        if let even = ChineseCalendar.evenSolarTermChinese.firstIndex(of: solarTerm) {
            return even * 2
        } else if let odd = ChineseCalendar.oddSolarTermChinese.firstIndex(of: solarTerm) {
            return odd * 2 + 1
        } else {
            return -1
        }
    }
}

struct RectWidget: Widget {
    static let kind: String = "Card"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: Self.kind, intent: CountDownProvider.Intent.self, provider: CountDownProvider()) { entry in
            CountDownEntryView(entry: entry)
                .containerBackground(Material.ultraThin, for: .widget)
        }
        .containerBackgroundRemovable()
        .configurationDisplayName("WGT_COUNTDOWN")
        .description("WGT_COUNTDOWN_MSG")
        .supportedFamilies([.accessoryRectangular])
    }
}

#Preview("Lunar Phase", as: .accessoryRectangular, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .lunarPhases
    return intent
}()) {
    RectWidget()
} timelineProvider: {
    CountDownProvider()
}

#Preview("Solar Term", as: .accessoryRectangular, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .solarTerms
    return intent
}()) {
    RectWidget()
} timelineProvider: {
    CountDownProvider()
}

#Preview("Sunrise", as: .accessoryRectangular, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .sunriseSet
    return intent
}()) {
    RectWidget()
} timelineProvider: {
    CountDownProvider()
}

#Preview("Moonrise", as: .accessoryRectangular, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .moonriseSet
    return intent
}()) {
    RectWidget()
} timelineProvider: {
    CountDownProvider()
}
