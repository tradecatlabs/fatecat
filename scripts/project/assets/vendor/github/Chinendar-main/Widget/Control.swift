//
//  Control.swift
//  Chinendar
//
//  Created by Leo Liu on 8/9/24.
//

import WidgetKit
import SwiftUI
import AppIntents

struct OpenAppButton: ControlWidget {
    static let kind: String = "OpenChinendar"

    var body: some ControlWidgetConfiguration {
        AppIntentControlConfiguration(
            kind: Self.kind,
            intent: OpenApp.self
        ) { _ in
            ControlWidgetButton(action: OpenApp()) {
                Label("LAUNCH_CHINENDAR", image: .appChinendar)
            }
#if os(watchOS)
            .tint(.accentColor)
#endif
        }
        .displayName("LAUNCH_CHINENDAR")
        .description("LAUNCH_CHINENDAR_MSG")
    }
}
