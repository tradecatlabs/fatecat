//
//  Corner.swift
//  Watch Widget Extension
//
//  Created by Leo Liu on 6/28/23.
//

import SwiftUI
import WidgetKit

struct CurveWidget: Widget {
    static let kind: String = "Corner"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(kind: Self.kind, intent: CountDownProvider.Intent.self, provider: CountDownProvider()) { entry in
            CountDownEntryView(entry: entry)
                .containerBackground(Material.thin, for: .widget)
        }
        .configurationDisplayName("WGT_CORNER")
        .description("WGT_CORNER_MSG")
        .supportedFamilies([.accessoryCorner])
    }
}

#Preview("Sunrise", as: .accessoryCorner, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .sunriseSet
    return intent
}(), widget: {
    CurveWidget()
}, timelineProvider: {
    CountDownProvider()
})

#Preview("Moonrise", as: .accessoryCorner, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .moonriseSet
    return intent
}(), widget: {
    CurveWidget()
}, timelineProvider: {
    CountDownProvider()
})

#Preview("Solar Terms", as: .accessoryCorner, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .solarTerms
    return intent
}(), widget: {
    CurveWidget()
}, timelineProvider: {
    CountDownProvider()
})

#Preview("Moon Phases", as: .accessoryCorner, using: {
    let intent = CountDownProvider.Intent()
    intent.calendarConfig = .ConfigQuery().defaultResult()
    intent.target = .lunarPhases
    return intent
}(), widget: {
    CurveWidget()
}, timelineProvider: {
    CountDownProvider()
})
