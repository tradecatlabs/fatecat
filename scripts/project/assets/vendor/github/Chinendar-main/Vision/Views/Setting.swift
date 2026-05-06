//
//  Settings.swift
//  Chinendar
//
//  Created by Leo Liu on 11/13/23.
//

import SwiftUI
import StoreKit

struct Setting: View {
    @Environment(ViewModel.self) var viewModel
    @Environment(\.modelContext) private var modelContext
    @Environment(\.requestReview) var requestReview
    let notificationManager = NotificationManager.shared
    let spaceTimePages: [WatchSetting.Selection] = [.datetime, .location, .configs, .reminders]
    let designPages: [WatchSetting.Selection] = [.ringColor, .decoration, .markColor, .layout, .themes]

    var body: some View {
        TabView(selection: viewModel.binding(\.settings.tabSelection)) {
            NavigationSplitView {
                List(selection: viewModel.binding(\.settings.selectionSpaceTime)) {
                    ForEach(spaceTimePages, id: \.self) { selection in
                        buildView(selection: selection)
                    }
                }
                .navigationTitle("LOC_TIME")
            } detail: {
                NavigationStack(path: viewModel.binding(\.settings.path)) {
                    switch viewModel.settings.selectionSpaceTime {
                    case .datetime:
                        Datetime()
                    case .location:
                        Location()
                    case .configs:
                        ConfigList()
                    case .reminders:
                        RemindersSetting()
                    default:
                        EmptyView()
                    }
                }
            }
            .tag(WatchSetting.TabSelection.spaceTime)
            .tabItem {
                Label("LOC_TIME", systemImage: "globe.desk")
            }
            .navigationSplitViewColumnWidth(ideal: 200)

            NavigationSplitView {
                List(selection: viewModel.binding(\.settings.selectionDesign)) {
                    ForEach(designPages, id: \.self) { selection in
                        buildView(selection: selection)
                    }
                }
                .navigationTitle("DESIGN")
            } detail: {
                NavigationStack(path: viewModel.binding(\.settings.path)) {
                    switch viewModel.settings.selectionDesign {
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
                    default:
                        EmptyView()
                    }
                }
            }
            .tag(WatchSetting.TabSelection.design)
            .tabItem {
                Label("DESIGN", systemImage: "paintbrush")
            }
            .navigationSplitViewColumnWidth(ideal: 200)

            NavigationStack(path: viewModel.binding(\.settings.path)) {
                Documentation()
            }
            .tag(WatchSetting.TabSelection.documentation)
            .tabItem {
                Label("Q&A", systemImage: "doc.questionmark")
            }
        }
        .onAppear {
            viewModel.settings.settingIsOpen = true
        }
        .onDisappear {
            viewModel.settings.settingIsOpen = false
            if LocalStats.experienced() {
                requestReview()
            }
            try? modelContext.save()
            viewModel.settings.path = NavigationPath()
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
        }
        return sel
    }
}

#Preview("Settings", traits: .modifier(SampleData())) {
    Setting()
        .frame(width: 900, height: 700)
        .environment(\.locale, Locale(identifier: "en"))
}
