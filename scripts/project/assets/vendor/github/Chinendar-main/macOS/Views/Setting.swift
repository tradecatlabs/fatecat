//
//  Setting.swift
//  Chinendar
//
//  Created by Leo Liu on 6/30/23.
//

import SwiftUI
import WidgetKit
import StoreKit

struct Setting: View {
    @Environment(ViewModel.self) var viewModel
    @State private var columnVisibility = NavigationSplitViewVisibility.automatic
    @Environment(\.modelContext) private var modelContext
    @Environment(\.requestReview) var requestReview
    let notificationManager = NotificationManager.shared

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            List(selection: viewModel.binding(\.settings.selection)) {
                Section("LOC_TIME") {
                    ForEach([WatchSetting.Selection.datetime,
                             .location, .configs, .reminders], id: \.self) { selection in
                        buildView(selection: selection)
                    }
                }
                Section("DESIGN") {
                    ForEach([WatchSetting.Selection.ringColor,
                             .decoration, .markColor, .layout, .themes], id: \.self) { selection in
                        buildView(selection: selection)
                    }
                }
                Section {
                    ForEach([WatchSetting.Selection.documentation], id: \.self) { selection in
                        buildView(selection: selection)
                    }
                }
            }
        } detail: {
            NavigationStack(path: viewModel.binding(\.settings.path)) {
                switch viewModel.settings.selection {
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
                case .none:
                    EmptyView()
                }
            }
        }
        .navigationSplitViewStyle(.balanced)
        .onAppear {
            viewModel.settings.settingIsOpen = true
            viewModel.settings.selection = viewModel.settings.previousSelection
        }
        .task(id: viewModel.settings.selection) {
            cleanColorPanel()
        }
        .onDisappear {
            viewModel.settings.settingIsOpen = false
            viewModel.settings.previousSelection = viewModel.settings.selection
            viewModel.settings.selection = nil
            cleanColorPanel()
            if LocalStats.experienced() {
                requestReview()
            }
            try? modelContext.save()
            Task {
                try await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
            }
        }
    }

    func buildView(selection: WatchSetting.Selection) -> some View {
        let sel = switch selection {
        case .datetime:
            Label("DATETIME", systemImage: "clock")
        case .location:
            Label("LAT&LON", systemImage: "location")
        case .configs:
            Label("CALENDAR_LIST", systemImage: "globe")
        case .reminders:
            Label("REMINDERS_LIST", systemImage: "deskclock")
        case .ringColor:
            Label("RING_COLORS", systemImage: "pencil.and.outline")
        case .decoration:
            Label("ADDON_COLORS", systemImage: "paintpalette")
        case .markColor:
            Label("COLOR_MARKS", systemImage: "wand.and.stars")
        case .layout:
            Label("LAYOUTS", systemImage: "square.resize")
        case .themes:
            Label("THEME_LIST", systemImage: "archivebox")
        case .documentation:
            Label("Q&A", systemImage: "doc.questionmark")
        }
        return sel
    }

    @MainActor func cleanColorPanel() {
        NSColorPanel.shared.setTarget(nil)
        NSColorPanel.shared.setAction(nil)
        NSColorPanel.shared.close()
    }
}

#Preview("Settings", traits: .modifier(SampleData())) {
    Setting()
        .environment(\.locale, Locale(identifier: "en"))
}
