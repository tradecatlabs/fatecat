//
//  visionApp.swift
//  Chinendar
//
//  Created by Leo Liu on 11/5/23.
//

import SwiftUI
import SwiftData

@main
struct Chinendar: App {
    let viewModel = ViewModel.shared
    let timer = Timer.publish(every: ChineseCalendar.updateInterval, on: .main, in: .common).autoconnect()
    let modelContainer = DataSchema.container
    @Environment(\.openWindow) var openWindow
    @Environment(\.dismissWindow) var dismissWindow

    init() {
        autoUpdateStatusBar()
    }

    var body: some Scene {
        WindowGroup(id: "WatchFace") {
            WatchFace()
                .padding(15)
                .modelContainer(modelContainer)
                .environment(viewModel)
                .onReceive(timer) { _ in
                    self.viewModel.updateChineseCalendar()
                }
                .ornament(attachmentAnchor: .scene(.bottom)) {
                    ornament
                }
        }
        .defaultSize(width: viewModel.baseLayout.offsets.watchSize.width + 30, height: viewModel.baseLayout.offsets.watchSize.height + 30)
        .windowResizability(.contentSize)

        WindowGroup(id: "Settings") {
            Setting()
                .modelContainer(modelContainer)
                .environment(viewModel)
        }
        .defaultSize(width: 900, height: 700)
    }

    var ornament: some View {
        HStack(spacing: 0) {
            if viewModel.settings.timeDisplay.count > 0 {
                Text(viewModel.settings.timeDisplay)
                    .padding()
            }
            Button {
                if viewModel.settings.settingIsOpen {
                    dismissWindow(id: "Settings")
                } else {
                    openWindow(id: "Settings")
                }
            } label: {
                if viewModel.settings.timeDisplay.count > 0 {
                    Label("SETTINGS", systemImage: "gear")
                        .labelStyle(.iconOnly)
                } else {
                    Label("SETTINGS", systemImage: "gear")
                        .labelStyle(.titleAndIcon)
                }
            }
            .buttonStyle(.borderless)
        }
        .glassBackgroundEffect()
        .alignmentGuide(VerticalAlignment.center) { _ in 15 }
    }

    func statusBar(from chineseCalendar: ChineseCalendar, options watchLayout: WatchLayout) -> String {
        var displayText = [String]()
        if watchLayout.statusBar.date {
            displayText.append(chineseCalendar.dateString)
        }
        if watchLayout.statusBar.holiday > 0 {
            let holidays = chineseCalendar.holidays
            displayText.append(contentsOf: holidays[..<min(holidays.count, watchLayout.statusBar.holiday)])
        }
        if watchLayout.statusBar.time {
            displayText.append(chineseCalendar.hourString + chineseCalendar.quarterString)
        }
        return displayText.joined(separator: watchLayout.statusBar.separator.rawValue)
    }

    func updateStatusBar() {
        viewModel.settings.timeDisplay = String(statusBar(from: viewModel.chineseCalendar, options: viewModel.watchLayout).reversed())
    }

    func autoUpdateStatusBar() {
        withObservationTracking {
            updateStatusBar()
        } onChange: {
            Task { @MainActor in
                self.autoUpdateStatusBar()
            }
        }
    }
}

@Observable final class ViewModel: ViewModelType {
    static let shared = ViewModel()

    let modelContainer: ModelContainer
    let themeData: LocalTheme
    let configData: LocalConfig
    var settings = WatchSetting()
    var chineseCalendar = ChineseCalendar()
    @ObservationIgnored let locationManager = LocationManager.shared
    var gpsLocation: GeoLocation?
    var error: (any Error)?

    private init() {
        modelContainer = LocalSchema.container
        themeData = LocalTheme.load(context: modelContainer.mainContext)
        configData = LocalConfig.load(context: modelContainer.mainContext)
        self.setup()
    }
}
