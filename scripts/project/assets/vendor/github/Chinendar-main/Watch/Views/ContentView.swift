//
//  ContentView.swift
//  Chinendar
//
//  Created by Leo Liu on 5/3/23.
//

import SwiftUI
import WidgetKit

struct WatchFaceTab<Tab: View>: View {
    @Environment(ViewModel.self) var viewModel
    let proxy: GeometryProxy
    let tab: Tab

    init(proxy: GeometryProxy, @ViewBuilder content: () -> Tab) {
        self.proxy = proxy
        self.tab = content()
    }

    var body: some View {
        NavigationStack(path: viewModel.binding(\.settings.path)) {
            TabView {
                tab
                    .toolbar(.hidden)
                Setting()
            }
            .navigationDestination(for: WatchSetting.Selection.self) { selection in
                switch selection {
                case .datetime:
                    DateTimeAdjust()
                case .themes:
                    ThemesList()
                case .configs:
                    ConfigList()
                case .reminders:
                    RemindersSetting()
                }
            }
        }
        .tabViewStyle(VerticalPageTabViewStyle(transitionStyle: .blur))
        .onAppear {
            viewModel.settings.size = proxy.size
        }
    }
}

struct ContentView: View {
    @Environment(ViewModel.self) var viewModel
    @Environment(\.scenePhase) var scenePhase
    @Environment(\.modelContext) private var modelContext
    let notificationManager = NotificationManager.shared

    var body: some View {
        GeometryReader { proxy in
            if viewModel.watchLayout.dualWatch {
                WatchFaceTab(proxy: proxy) {
                    WatchFaceDate()
                        .ignoresSafeArea()
                    WatchFaceTime()
                        .ignoresSafeArea()
                }
            } else {
                WatchFaceTab(proxy: proxy) {
                    WatchFaceFull()
                        .ignoresSafeArea()
                }
            }
        }
        .ignoresSafeArea()
        .task(id: scenePhase) {
            switch scenePhase {
            case .active:
                if viewModel.watchLayout.syncFromPhone {
                    await viewModel.watchConnectivity.requestLayout()
                }
            case .background:
                try? viewModel.modelContainer.mainContext.save()
                WidgetCenter.shared.reloadAllTimelines()
            default:
                break
            }
        }
        .task {
            try? await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
        }
    }
}

#Preview("Watch Face", traits: .modifier(SampleData())) {
    ContentView()
        .environment(\.locale, Locale(identifier: "en"))
}
