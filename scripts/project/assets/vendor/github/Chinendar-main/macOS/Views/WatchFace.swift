//
//  WatchFace.swift
//  Chinendar
//
//  Created by Leo Liu on 7/1/23.
//

import SwiftUI

struct WatchFace: View {
    @Environment(ViewModel.self) var viewModel
    @State var entityPresenting = EntitySelection()
    @State var tapPos: CGPoint?
    @State var touchState = PressState()

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

    var body: some View {
        GeometryReader { proxy in
            let size: CGSize = viewModel.baseLayout.offsets.watchSize
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
            .animation(.easeInOut(duration: 0.2), value: entityPresenting.activeNote)
        }
        .frame(width: viewModel.baseLayout.offsets.watchSize.width, height: viewModel.baseLayout.offsets.watchSize.height)
    }
}

#Preview("WatchFace", traits: .modifier(SampleData())) {
    WatchFace()
}
