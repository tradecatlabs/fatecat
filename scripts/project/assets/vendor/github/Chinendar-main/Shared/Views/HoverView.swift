//
//  HoverView.swift
//  Chinendar
//
//  Created by Leo Liu on 6/26/23.
//

import SwiftUI
import Observation

struct Hover: View {
    @Environment(ViewModel.self) var viewModel
    @State var isEastAsian = Locale.isEastAsian
    @State var entityPresenting: EntitySelection
    @Binding var tapPos: CGPoint?

    var body: some View {
        if entityPresenting.activeNote.count > 0 {
            if isEastAsian {
                HStack(alignment: .top) {
                    ForEach(entityPresenting.activeNote) {note in
                        VStack(spacing: 0) {
                            RoundedRectangle(cornerRadius: fontSize * 0.2)
                                .frame(width: fontSize, height: fontSize)
                                .foregroundStyle(Color(cgColor: note.color))
                                .padding(.vertical, fontSize * 0.08)
                            Spacer(minLength: fontSize * 0.2)
                                .frame(maxHeight: fontSize * 0.2)
                            ForEach(Array(Locale.translate(note.name)), id: \.self) { char in
                                Text(String(char))
                                    .font(.system(size: fontSize))
                                    .padding(0)
                            }
                        }
                    }
                }
                .dynamicHover(tapPos: $tapPos, fontSize: fontSize)
            } else {
                VStack(alignment: .leading) {
                    ForEach(entityPresenting.activeNote) {note in
                        HStack(spacing: 0) {
                            RoundedRectangle(cornerRadius: fontSize * 0.2)
                                .frame(width: fontSize, height: fontSize)
                                .foregroundStyle(Color(cgColor: note.color))
                                .padding(.horizontal, fontSize * 0.08)
                                .padding(.vertical, 0)
                            Spacer(minLength: fontSize * 0.2)
                                .frame(maxWidth: fontSize * 0.2)
                            Text(Locale.translate(note.name))
                                .font(.system(size: fontSize))
                                .padding(0)
                        }
                    }
                }
                .dynamicHover(tapPos: $tapPos, fontSize: fontSize)
            }
        }
    }

    var fontSize: CGFloat {
        let shortEdge = min(viewModel.baseLayout.offsets.watchSize.width, viewModel.baseLayout.offsets.watchSize.height)
        let longEdge = min(viewModel.baseLayout.offsets.watchSize.width, viewModel.baseLayout.offsets.watchSize.height)
        return min(shortEdge * 0.04, longEdge * 0.032)
    }
}

@MainActor
@Observable final class EntitySelection {
    @ObservationIgnored var entityNotes = EntityNotes()
    @ObservationIgnored var timer: Timer?
    @ObservationIgnored var _activeNote: [EntityNotes.EntityNote] = [] {
        didSet {
            timer?.invalidate()
            if _activeNote.count > 0 {
                timer = Timer.scheduledTimer(withTimeInterval: 3, repeats: false) { _ in
                    Task { @MainActor in
                        self.activeNote = []
                    }
                }
            } else {
                timer = nil
            }
        }
    }
    var activeNote: [EntityNotes.EntityNote] {
        get {
            self.access(keyPath: \.activeNote)
            return _activeNote
        } set {
            self.withMutation(keyPath: \.activeNote) {
                _activeNote = newValue
            }
        }
    }
}

private func edgeSafePos(pos: CGPoint, size: CGSize, screen: CGSize) -> CGPoint {
    var idealPos = pos
    let halfSize = CGPoint(x: size.width / 2, y: size.height / 2)
    if idealPos.x < halfSize.x {
        idealPos.x = halfSize.x
    } else if idealPos.x + halfSize.x > screen.width {
        idealPos.x = screen.width - halfSize.x
    }
    if idealPos.y < halfSize.y {
        idealPos.y = halfSize.y
    } else if idealPos.y + halfSize.y > screen.height {
        idealPos.y = screen.height - halfSize.y
    }
    return idealPos
}

private struct HoverModifier: ViewModifier {
    @State private var size: CGSize = .zero
    @Binding var tapPos: CGPoint?
    let fontSize: CGFloat

    func body(content: Content) -> some View {
        GeometryReader { proxy in
            if let tapPos {
                content
                .padding(fontSize * 0.3)
#if os(visionOS)
                .background(.ultraThinMaterial, in: .rect(cornerRadius: fontSize * 0.5, style: .continuous))
#else
                .glassEffect(.regular.interactive(), in: .rect(cornerRadius: fontSize * 0.5, style: .continuous))
#endif
                .anchorPreference(key: SizePreferenceKey.self, value: .bounds) { proxy[$0].size }
                .onPreferenceChange(SizePreferenceKey.self) { [$size] newValue in
                    $size.wrappedValue = newValue
                }
                .position(tapPos)
                .task(id: CGRect(origin: tapPos, size: size)) {
                    let safePos = edgeSafePos(pos: tapPos, size: size, screen: proxy.size)
                    if safePos != tapPos {
                        $tapPos.wrappedValue = safePos
                    }
                }
            }
        }
    }
}

private extension View {
    func dynamicHover(tapPos: Binding<CGPoint?>, fontSize: CGFloat) -> some View {
        self.modifier(HoverModifier(tapPos: tapPos, fontSize: fontSize))
    }
}

private struct SizePreferenceKey: PreferenceKey {
    static let defaultValue: CGSize = .zero

    static func reduce(value: inout CGSize, nextValue: () -> CGSize) {
        value = nextValue()
    }

}
