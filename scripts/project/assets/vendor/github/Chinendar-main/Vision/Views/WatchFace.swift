//
//  WatchFace.swift
//  Chinendar
//
//  Created by Leo Liu on 11/14/23.
//

import SwiftUI

struct WatchFace: View {
    @Environment(ViewModel.self) var viewModel
    @State var showWelcome = false
    @State var entityPresenting = EntitySelection()
    @State var tapPos: CGPoint?
    @State var touchState = PressState()
    @State var frame: CGSize?
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

            let size = viewModel.baseLayout.offsets.watchSize
            let centerOffset = if size.height >= size.width {
                viewModel.baseLayout.offsets.centerTextOffset.width
            } else {
                viewModel.baseLayout.offsets.centerTextOffset.height
            }
            let gesture = DragGesture(minimumDistance: 0, coordinateSpace: .local)
                .onChanged { value in
                    touchState.pressing = true
                    touchState.location = value.location
                }
                .onEnded { _ in
                    if touchState.tapped {
                        tapped(tapPosition: touchState.location!, proxy: proxy, size: size)
                    }
                    touchState.pressing = false
                    touchState.location = nil
                }

            ZStack {
                Watch(displaySubquarter: true, displaySolarTerms: true, compact: false, watchLayout: viewModel.watchLayout, markSize: 1.0, chineseCalendar: viewModel.chineseCalendar, highlightType: .flicker, widthScale: 0.9, centerOffset: centerOffset, entityNotes: entityPresenting.entityNotes, textShift: true)
                    .frame(width: size.width, height: size.height)
                    .position(CGPoint(x: proxy.size.width / 2, y: proxy.size.height / 2))
                    .environment(\.directedScale, DirectedScale(value: touchState.pressing ? -0.1 : 0.0, anchor: pressAnchor(pos: touchState.location, size: size, proxy: proxy)))
                    .gesture(gesture)

                Hover(entityPresenting: entityPresenting, tapPos: $tapPos)
            }
            .onChange(of: proxy.size) {
                viewModel.settings.vertical = proxy.size.height >= proxy.size.width
                viewModel.baseLayout.offsets.watchSize = proxy.size
            }
            .animation(.easeInOut(duration: 0.2), value: entityPresenting.activeNote)
        }
        .sheet(isPresented: $showWelcome) {
            Welcome(size: CGSize(width: viewModel.baseLayout.offsets.watchSize.width * 0.8, height: viewModel.baseLayout.offsets.watchSize.height * 0.8))
        }
        .task(priority: .background) {
            showWelcome = LocalStats.notLatest()
            try? await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
        }
    }
}

#Preview("Watch Face", traits: .modifier(SampleData())) {
    WatchFace()
}
