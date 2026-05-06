//
//  WatchPanel.swift
//  Chinendar
//
//  Created by Leo Liu on 8/1/23.
//

import SwiftUI

class WatchPanel: NSPanel {
    private var _isPresented: Bool
    private let statusItem: NSStatusItem
    private let viewModel: ViewModel

    var isPresented: Bool {
        get {
            _isPresented
        } set {
            _isPresented = newValue
            self.present()
        }
    }

    init(statusItem: NSStatusItem, viewModel: ViewModel, isPresented: Bool) {
        self._isPresented = isPresented
        self.statusItem = statusItem
        self.viewModel = viewModel

        super.init(contentRect: .zero, styleMask: .borderless, backing: .buffered, defer: true)
        self.level = NSWindow.Level.floating
        self.hasShadow = true
        self.isOpaque = false
        self.backgroundColor = .clear
        self.autoUpdatePanelPosition()
    }

    private func present() {
        if _isPresented {
            self.panelPosition()
            self.orderFront(nil)
            NSApp.activate(ignoringOtherApps: true)
        } else {
            self.close()
        }
    }

    func panelPosition() {
        if let statusItemFrame = statusItem.button?.window?.frame {
            let windowRect = getCurrentScreen()
            let baseLayout = viewModel.baseLayout
            let buttonSize = viewModel.buttonSize
            var frame = NSRect(x: statusItemFrame.midX - baseLayout.offsets.watchSize.width / 2,
                               y: statusItemFrame.minY - baseLayout.offsets.watchSize.height - 6,
                               width: baseLayout.offsets.watchSize.width,
                               height: baseLayout.offsets.watchSize.height)
            viewModel.settings.position = frame
            frame.origin.y -= buttonSize.height * 1.7
            frame.size.height += buttonSize.height * 1.7
            if frame.maxX >= windowRect.maxX {
                frame.origin.x = windowRect.maxX - frame.width
            } else if frame.minX <= windowRect.minX {
                frame.origin.x = windowRect.minX
            }
            setFrame(frame, display: true)
        }
    }

    func autoUpdatePanelPosition() {
        withObservationTracking {
            panelPosition()
        } onChange: {
            Task { @MainActor in
                self.autoUpdatePanelPosition()
            }
        }
    }

    private func getCurrentScreen() -> NSRect {
        var screenRect = NSScreen.main!.frame
        let screens = NSScreen.screens
        for i in 0 ..< screens.count {
            let rect = screens[i].frame
            if let statusBarFrame = statusItem.button?.window?.frame, rect.contains(NSPoint(x: statusBarFrame.midX, y: statusBarFrame.midY)) {
                screenRect = rect
                break
            }
        }
        return screenRect
    }
}

internal final class WatchPanelHosting<MainView: View>: WatchPanel {
    private let mainView: NSHostingView<MainView>

    init(view: MainView, statusItem: NSStatusItem, viewModel: ViewModel, isPresented: Bool) {
        mainView = NSHostingView(rootView: view)
        super.init(statusItem: statusItem, viewModel: viewModel, isPresented: isPresented)
        contentView?.addSubview(mainView)
    }

    override func panelPosition() {
        super.panelPosition()
        if let bounds = contentView?.bounds {
            mainView.frame = bounds
        }
    }
}
