//
//  WatchFace.swift
//  Chinendar
//
//  Created by Leo Liu on 6/25/23.
//

import SwiftUI
import WidgetKit

struct AdaptiveSheet<PresentedContent: View>: ViewModifier {
    @Binding var isPresented: Bool
    @ViewBuilder var presentedContent: () -> PresentedContent
    @Environment(\.horizontalSizeClass) var horizontalSizeClass

    func body(content: Content) -> some View {
        if horizontalSizeClass == .compact {
            content
                .sheet(isPresented: $isPresented) {
                    presentedContent()
                        .presentationDetents([.medium, .large])
                }
        } else {
            content
                .inspector(isPresented: $isPresented) {
                    presentedContent()
                }
        }
    }
}

fileprivate extension View {
    func adaptiveSheet<PresentedContent: View>(isPresented: Binding<Bool>, presentedContent: @escaping () -> PresentedContent) -> some View {
        self.modifier(AdaptiveSheet(isPresented: isPresented, presentedContent: presentedContent))
    }
}

struct WatchFace: View {
    @Environment(ViewModel.self) var viewModel
    @Environment(\.scenePhase) var scenePhase
    @State var showWelcome = false
    @State var entityPresenting = EntitySelection()
    @State var touchState = PressState()
    @State var tapPos: CGPoint?
    @State var timer: Timer?
    @GestureState private var dragging = false
    let notificationManager = NotificationManager.shared

    func tapped(tapPosition: CGPoint, proxy: GeometryProxy, size: CGSize) {
        var tapPosition = tapPosition
        tapPos = tapPosition
        tapPosition.x -= (proxy.size.width - size.width) / 2
        tapPosition.y -= (proxy.size.height - size.height) / 2
        entityPresenting.activeNote = []
        for mark in entityPresenting.entityNotes.entities {
            let diff = tapPosition - mark.position
            let dist = sqrt(diff.x * diff.x + diff.y * diff.y)
            if dist.isFinite && dist < 5 * min(size.width, size.height) * Marks.markSize {
                entityPresenting.activeNote.append(mark)
            }
        }
    }

    func mainSize(proxy: GeometryProxy) -> CGSize {
        var idealSize = viewModel.baseLayout.offsets.watchSize
        if proxy.size.height < proxy.size.width {
            let width = idealSize.width
            idealSize.width = idealSize.height
            idealSize.height = width
        }
        if proxy.size.width * 0.95 < idealSize.width {
            let ratio = proxy.size.width * 0.95 / idealSize.width
            idealSize.width *= ratio
            idealSize.height *= ratio
        }
        if proxy.size.height * 0.95 < idealSize.height {
            let ratio = proxy.size.height * 0.95 / idealSize.height
            idealSize.width *= ratio
            idealSize.height *= ratio
        }
        return idealSize
    }

    var body: some View {
        GeometryReader { proxy in
            let size = mainSize(proxy: proxy)
            let centerOffset = if size.height >= size.width {
                viewModel.baseLayout.offsets.centerTextOffset.width
            } else {
                viewModel.baseLayout.offsets.centerTextOffset.height
            }
            let gesture = DragGesture(minimumDistance: 0, coordinateSpace: .local)
                .updating($dragging) { _, state, _ in
                    state = true
                }
                .onChanged { value in
                    touchState.pressing = true
                    touchState.location = value.location
                }

            ZStack {
                Watch(displaySubquarter: true, displaySolarTerms: true, compact: false, watchLayout: viewModel.watchLayout, markSize: 1.0, chineseCalendar: viewModel.chineseCalendar, highlightType: .flicker, widthScale: 0.9, centerOffset: centerOffset, entityNotes: entityPresenting.entityNotes, textShift: true)
                    .frame(width: size.width, height: size.height)
                    .position(CGPoint(x: proxy.size.width / 2, y: proxy.size.height / 2))
                    .environment(\.directedScale, DirectedScale(value: touchState.pressing ? -0.1 : 0.0, anchor: pressAnchor(pos: touchState.location, size: size, proxy: proxy)))
                    .gesture(gesture)

                Hover(entityPresenting: entityPresenting, tapPos: $tapPos)
            }
            .onChange(of: dragging) { _, newValue in
                if newValue {
                    timer = Timer.scheduledTimer(withTimeInterval: 0.5, repeats: false) { _ in
                        Task { @MainActor in
                            if !viewModel.settings.presentSetting {
                                UIImpactFeedbackGenerator(style: .rigid).impactOccurred()
                                viewModel.settings.presentSetting = true
                                touchState.ended = true
                            }
                        }
                    }
                } else {
                    timer?.invalidate()
                    if touchState.tapped {
                        tapped(tapPosition: touchState.location!, proxy: proxy, size: size)
                    }
                    touchState.pressing = false
                    touchState.location = nil
                    touchState.ended = false
                }
            }
            .onChange(of: proxy.size) {
                viewModel.settings.vertical = proxy.size.height >= proxy.size.width
            }
            .animation(.easeInOut(duration: 0.2), value: entityPresenting.activeNote)
        }
        .sheet(isPresented: $showWelcome) {
            Welcome()
        }
        .adaptiveSheet(isPresented: viewModel.binding(\.settings.presentSetting)) {
            Setting()
                    .inspectorColumnWidth(min: 350, ideal: 400, max: 500)
        }
        .task(priority: .background) {
            showWelcome = LocalStats.notLatest()
            try? await viewModel.watchConnectivity.send(messages: [
                "layout": viewModel.watchLayout.encode(),
                "config": viewModel.config.encode()
            ])
            try? await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
        }
        .task(id: scenePhase) {
            switch scenePhase {
            case .background:
                try? viewModel.modelContainer.mainContext.save()
                WidgetCenter.shared.reloadAllTimelines()
            default:
                break
            }
        }
    }
}

#Preview("Watch Face", traits: .modifier(SampleData())) {
    WatchFace()
        .environment(\.locale, Locale(identifier: "en"))
}
