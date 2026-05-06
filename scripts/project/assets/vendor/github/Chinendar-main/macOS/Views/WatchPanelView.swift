//
//  WatchPanelView.swift
//  Chinendar
//
//  Created by Leo Liu on 6/11/25.
//

import SwiftUI

struct WatchPanelView: View {
    @Environment(ViewModel.self) var viewModel
    @Environment(\.openWindow) var openWindow
    @Environment(\.dismissWindow) var dismissWindow

    var body: some View {
        GlassEffectContainer {
            VStack(spacing: 0) {
                WatchFace()
                    .glassEffect(.regular, in: .rect(cornerRadius: viewModel.shortEdge * 0.07, style: .continuous))
                HStack {
                    Button {
                        if viewModel.settings.settingIsOpen {
                            dismissWindow(id: "Settings")
                        } else {
                            openWindow(id: "Settings")
                        }
                    } label: {
                        Image(systemName: "gearshape")
                    }
                    .tint(.primary)
                    .frame(width: viewModel.buttonSize.width, height: viewModel.buttonSize.height)
                    Spacer()
                        .frame(maxWidth: viewModel.buttonSize.width * 0.6)
                    Button(role: .destructive) {
                        NSApp.terminate(nil)
                    } label: {
                        Image(systemName: "xmark")
                    }
                    .tint(.red)
                    .frame(width: viewModel.buttonSize.width, height: viewModel.buttonSize.height)
                }
                .frame(height: viewModel.buttonSize.height)
                .font(.system(size: viewModel.buttonSize.height * 0.5, weight: .medium))
                .buttonStyle(.borderless)
                .glassEffect(.regular, in: .capsule)
                .padding(.bottom, viewModel.buttonSize.height * 0.25)
                .padding(.top, viewModel.buttonSize.height * 0.45)
            }
        }
    }
}

#Preview("WatchFace", traits: .modifier(SampleData())) {
    WatchPanelView()
}
