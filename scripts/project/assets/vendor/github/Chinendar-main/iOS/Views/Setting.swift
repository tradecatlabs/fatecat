//
//  Setting.swift
//  Chinendar
//
//  Created by Leo Liu on 6/25/23.
//

import SwiftUI
import StoreKit

struct Setting: View {
    @Environment(ViewModel.self) var viewModel
    @Environment(\.modelContext) private var modelContext
    @Environment(\.requestReview) var requestReview
    let notificationManager = NotificationManager.shared

    var body: some View {
        NavigationStack(path: viewModel.binding(\.settings.path)) {
            List {
                Section("LOC_TIME") {
                    NavigationLink(value: WatchSetting.Selection.datetime) {
                        Label("DATETIME", systemImage: "clock")
                    }
                    NavigationLink(value: WatchSetting.Selection.location) {
                        Label("LAT&LON", systemImage: "location")
                    }
                    NavigationLink(value: WatchSetting.Selection.configs) {
                        Label("CALENDAR_LIST", systemImage: "globe")
                    }
                    NavigationLink(value: WatchSetting.Selection.reminders) {
                        Label("REMINDERS_LIST", systemImage: "deskclock")
                    }
                }

                Section("DESIGN") {
                    NavigationLink(value: WatchSetting.Selection.ringColor) {
                        Label("RING_COLORS", systemImage: "pencil.and.outline")
                    }
                    NavigationLink(value: WatchSetting.Selection.decoration) {
                        Label("ADDON_COLORS", systemImage: "paintpalette")
                    }
                    NavigationLink(value: WatchSetting.Selection.markColor) {
                        Label("COLOR_MARKS", systemImage: "wand.and.stars")
                    }
                    NavigationLink(value: WatchSetting.Selection.layout) {
                        Label("LAYOUTS", systemImage: "square.resize")
                    }
                    NavigationLink(value: WatchSetting.Selection.themes) {
                        Label("THEME_LIST", systemImage: "archivebox")
                    }
                }
                Section {
                    NavigationLink(value: WatchSetting.Selection.documentation) {
                        Label("Q&A", systemImage: "doc.questionmark")
                    }
                }
            }
            .navigationDestination(for: WatchSetting.Selection.self) { selection in
                switch selection {
                case .datetime:
                    Datetime()
                case .location:
                    Location()
                case .configs:
                    ConfigList()
                case .reminders:
                    RemindersSetting()
                case .ringColor:
                    RingSetting()
                case .decoration:
                    DecorationSetting()
                case .markColor:
                    ColorSetting()
                case .layout:
                    LayoutSetting()
                case .themes:
                    ThemesList()
                case .documentation:
                    Documentation()
                }
            }
            .navigationTitle("SETTINGS")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                Button {
                    viewModel.settings.presentSetting = false
                } label: {
                    Label("DONE", systemImage: "checkmark")
                }
                .fontWeight(.semibold)
            }
        }
        .onDisappear {
            if LocalStats.experienced() {
                requestReview()
            }
            try? modelContext.save()
            viewModel.settings.path = NavigationPath()
            Task {
                try await viewModel.watchConnectivity.send(messages: [
                    "layout": viewModel.watchLayout.encode(),
                    "config": viewModel.config.encode()
                ])
                try await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
            }
        }
    }
}

#Preview("Settings", traits: .modifier(SampleData())) {
    NavigationStack {
        Setting()
    }
}
