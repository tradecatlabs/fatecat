//
//  iOSApp.swift
//  Chinendar
//
//  Created by Leo Liu on 4/17/23.
//

import SwiftUI
import SwiftData

@main
struct Chinendar: App {
    let viewModel = ViewModel.shared
    let timer = Timer.publish(every: ChineseCalendar.updateInterval, on: .main, in: .common).autoconnect()
    let modelContainer = DataSchema.container

    var body: some Scene {
        WindowGroup {
            WatchFace()
                .modelContainer(modelContainer)
                .environment(viewModel)
                .onReceive(timer) { _ in
                    viewModel.updateChineseCalendar()
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
    @ObservationIgnored lazy var watchConnectivity = WatchConnectivityManager(viewModel: self)
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
