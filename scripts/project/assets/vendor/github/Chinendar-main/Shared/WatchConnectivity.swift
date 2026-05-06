//
//  WatchConnectivity.swift
//  Chinendar
//
//  Created by Leo Liu on 5/5/23.
//

import WatchConnectivity

final class WatchConnectivityManager<T: ViewModelType>: NSObject, WCSessionDelegate, Sendable {
    private let getViewModel: @Sendable () -> T

    init(viewModel: @autoclosure @escaping @Sendable () -> T) {
        self.getViewModel = viewModel
        super.init()
        if WCSession.isSupported() {
            WCSession.default.delegate = self
            WCSession.default.activate()
        }
    }

    func session(_ session: WCSession, didReceiveMessage message: [String: Any]) {
#if os(watchOS)
        if let message = message as? [String: Data] {
            Task { @MainActor in
                let viewModel = getViewModel()
                guard viewModel.watchLayout.syncFromPhone else { return }
                if let newLayout = message["layout"] {
                    var layout = try WatchLayout(fromData: newLayout)
                    layout.baseLayout.offsets = viewModel.baseLayout.offsets
                    viewModel.watchLayout.baseLayout = layout.baseLayout
                }
                if let newConfig = message["config"] {
                    let config = try CalendarConfigure(fromData: newConfig)
                    viewModel.config = config

                    if viewModel.config.locationEnabled {
                        try await viewModel.locationManager.getLocation(wait: .seconds(5))
                    } else {
                        await viewModel.locationManager.clearLocation()
                    }
                }
            }
        }

#elseif os(iOS)
        if let request = message["request"] as? String {
            let requests = request.split(separator: /,/, omittingEmptySubsequences: true).map { String($0) }
            Task { @MainActor in
                let viewModel = getViewModel()
                var response = [String: Data]()
                if requests.contains("layout") {
                    if viewModel.layoutInitialized {
                        response["layout"] = try viewModel.watchLayout.encode()
                    }
                }
                if requests.contains("config") {
                    if viewModel.configInitialized {
                        response["config"] = try viewModel.config.encode()
                    }
                }
                await send(messages: response)
            }
        }
#endif
    }

    func session(_ session: WCSession,
                 activationDidCompleteWith activationState: WCSessionActivationState,
                 error: Error?) {}

#if os(iOS)
    func sessionDidBecomeInactive(_ session: WCSession) {}
    func sessionDidDeactivate(_ session: WCSession) {
        session.activate()
    }
#endif

    func send<D: Sendable>(messages: [String: D]) async {
        guard WCSession.default.activationState == .activated else { return }
#if os(iOS)
        guard WCSession.default.isWatchAppInstalled else { return }
#else
        guard WCSession.default.isCompanionAppInstalled else { return }
#endif
        WCSession.default.sendMessage(messages, replyHandler: nil) { error in
            print("Cannot send message: \(error.localizedDescription), resending in 3s")
            Task {
                try await Task.sleep(nanoseconds: 3_000_000_000)
                WCSession.default.sendMessage(messages, replyHandler: nil, errorHandler: nil)
            }
        }
    }

#if os(watchOS)
    func requestLayout() async {
        await send(messages: ["request": "layout,config"])
    }
#endif
}
