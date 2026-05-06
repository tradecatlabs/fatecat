//
//  RingSetting.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI

struct RingSetting: View {
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            Section("GRADIENT") {
#if os(iOS) || os(visionOS)
                let height = 80.0
                let loopSize = 10.0
#else
                let height = 45.0
                let loopSize = 0.0
#endif
                GradientSliderView(text: Text("YEAR_RING"), gradient: viewModel.binding(\.baseLayout.colors.firstRing), allowLoop: true)
                    .frame(height: height)
                GradientSliderView(text: Text("MONTH_RING"), gradient: viewModel.binding(\.baseLayout.colors.secondRing), allowLoop: true)
                    .frame(height: height)
                GradientSliderView(text: Text("DAY_RING"), gradient: viewModel.binding(\.baseLayout.colors.thirdRing), allowLoop: true)
                    .frame(height: height)
                GradientSliderView(text: Text("CENTER_TEXT"), gradient: viewModel.binding(\.baseLayout.colors.centerFontColor), allowLoop: false)
                    .frame(height: height - loopSize)
            }

            Section("START_ANGLE") {
                SliderView(value: viewModel.binding(\.baseLayout.startingPhase.zeroRing), min: -1, max: 1, label: Text("ST"))
                SliderView(value: viewModel.binding(\.baseLayout.startingPhase.firstRing), min: -1, max: 1, label: Text("YEAR_RING"))
                SliderView(value: viewModel.binding(\.baseLayout.startingPhase.secondRing), min: -1, max: 1, label: Text("MONTH_RING"))
                SliderView(value: viewModel.binding(\.baseLayout.startingPhase.thirdRing), min: -1, max: 1, label: Text("DAY_RING"))
                SliderView(value: viewModel.binding(\.baseLayout.startingPhase.fourthRing), min: -1, max: 1, label: Text("HOUR_RING"))
            }
        }
        .formStyle(.grouped)
        .navigationTitle("RING_COLORS")
#if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            Button {
                viewModel.settings.presentSetting = false
            } label: {
                Label("DONE", systemImage: "checkmark")
            }
            .fontWeight(.semibold)
        }
#endif
    }
}

struct ViewGradient {
    private var colors: [CGColor] = []
    private var values: [CGFloat] = []
    var isLoop: Bool = false

    subscript(color index: Int) -> CGColor {
        get {
            if index >= 0 && index < self.colors.count {
                self.colors[index]
            } else {
                CGColor(gray: 0, alpha: 0)
            }
        } set {
            if index >= 0 && index < self.colors.count {
                self.colors[index] = newValue
            }
        }
    }

    subscript(position index: Int) -> CGFloat {
        get {
            if index >= 0 && index < self.values.count {
                self.values[index]
            } else {
                0
            }
        } set {
            if index >= 0 && index < self.colors.count {
                self.values[index] = newValue
            }
        }
    }

    var gradientStops: [Gradient.Stop] {
        var stops: [Gradient.Stop] = zip(values, colors).map { value, color in
            Gradient.Stop(color: Color(cgColor: color), location: value)
        }
        stops.sort { $0.location < $1.location }
        if isLoop, let firstStop = stops.first {
            var lastStop = firstStop
            lastStop.location = 1.0
            stops.append(lastStop)
        }
        return stops
    }

    var count: Int {
        colors.count
    }

    mutating func add(color: CGColor, at value: CGFloat) {
        let index = values.insertionIndex(of: value, comparison: { $0 < $1 })
        colors.insert(color, at: index)
        values.insert(value, at: index)
    }

    mutating func remove(at index: Int) {
        if index >= 0 && index < colors.count {
            colors.remove(at: index)
            values.remove(at: index)
        }
    }

    func export(allowLoop: Bool = true) -> CodableGradient {
        return CodableGradient(locations: values, colors: colors, loop: allowLoop && isLoop)
    }

    init() {}

    init(from gradient: CodableGradient, allowLoop: Bool = true) {
        isLoop = allowLoop && gradient.isLoop
        if isLoop {
            colors = gradient.colors.dropLast()
            values = gradient.locations.dropLast()
        } else {
            colors = gradient.colors
            values = gradient.locations
        }
    }
}

struct GradientSliderView: View {
#if os(visionOS)
    let barHeight: CGFloat = 10
#else
    let barHeight: CGFloat = 5
#endif
#if os(iOS) || os(visionOS)
    let slideHeight: CGFloat = 18
    let pickerSize: CGFloat = 14
#elseif os(macOS)
    let slideHeight: CGFloat = 10
    let pickerSize: CGFloat = 10
#endif
    let padding: CGFloat = 0
    let text: Text
    @Binding var gradient: CodableGradient
    let allowLoop: Bool

    @State private var viewGradient = ViewGradient()
    @State private var position: (index: Int, pos: CGPoint)?

    var body: some View {
        GeometryReader { proxy in
            VStack {
                HStack {
                    text
                        .lineLimit(1)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    Spacer()
                    if allowLoop {
                        loopToggle
                    }
                }
                ZStack {
                    // Gradient background
                    LinearGradient(gradient: Gradient(stops: viewGradient.gradientStops), startPoint: .leading, endPoint: .trailing)
                        .frame(height: barHeight)
                        .cornerRadius(proxy.size.height / 2)
                        .padding(.horizontal, padding + pickerSize / 2)
                        .padding(.vertical, slideHeight - barHeight / 2)
#if os(visionOS)
                        .contentShape(
                            .rect(cornerRadius: 16, style: .continuous)
                        )
                        .hoverEffect()
#endif
                        .gesture(tapGesture(size: proxy.size))

                    ForEach(0..<viewGradient.count, id: \.self) { index in
#if os(iOS) || os(visionOS)
                        ColorPicker("", selection: $viewGradient[color: index])
                            .labelsHidden()
                            .shadow(color: .black.opacity(0.15), radius: 6, x: -3, y: 4)
                            .opacity(removing(index: index) ? 0.3 : 1.0)
                            .onChange(of: viewGradient[color: index]) {
                                gradient = viewGradient.export(allowLoop: allowLoop)
                            }
                            .frame(width: pickerSize * 2, height: pickerSize * 2)
                            .position(targetPos(index: index, size: proxy.size))
                            .simultaneousGesture(dragGesture(index: index, size: proxy.size))
#elseif os(macOS)
                        ColorNodeView(size: CGSize(width: pickerSize * 2, height: pickerSize * 2), color: $viewGradient[color: index])
                            .shadow(color: .black.opacity(0.3), radius: 2, x: -1, y: 1)
                            .opacity(removing(index: index) ? 0.3 : 1.0)
                            .onChange(of: viewGradient[color: index]) {
                                gradient = viewGradient.export(allowLoop: allowLoop)
                            }
                            .frame(width: pickerSize * 2, height: pickerSize * 2)
                            .position(targetPos(index: index, size: proxy.size))
                            .gesture(dragGesture(index: index, size: proxy.size))
#endif
                    }
                }
#if os(visionOS)
                .padding(.horizontal, 5)
#endif
                .task {
                    viewGradient = ViewGradient(from: gradient, allowLoop: allowLoop)
                }
                .contentShape(Rectangle())
                .padding(.horizontal, padding)
            }
        }
    }

    @ViewBuilder private var loopToggle: some View {
        Text("LOOP")
            .lineLimit(1)
            .frame(alignment: .trailing)
            .padding(.leading, 10)
        Toggle("", isOn: $viewGradient.isLoop)
            .labelsHidden()
            .onChange(of: viewGradient.isLoop) {
                gradient = viewGradient.export(allowLoop: allowLoop)
            }
    }

    private func tapGesture(size: CGSize) -> some Gesture {
        SpatialTapGesture()
            .onEnded { value in
                var newPosition = valueForPosition(value.location, in: size)
                newPosition = max(0, min(1, newPosition))
                let interpolateColor = gradient.interpolate(at: newPosition)
                viewGradient.add(color: interpolateColor, at: newPosition)
            }
    }

    private func dragGesture(index: Int, size: CGSize) -> some Gesture {
        DragGesture()
            .onChanged { value in
                nodeDragged(index: index, translation: value, size: size)
            }
            .onEnded { value in
                nodeFinishedDrag(index: index, translation: value)
            }
    }

    private func nodeDragged(index: Int, translation: DragGesture.Value, size: CGSize) {
        if viewGradient.count > 2 && abs(translation.location.y - pickerSize) > slideHeight * 2 {
#if os(iOS)
            if position == nil {
                UIImpactFeedbackGenerator(style: .rigid).impactOccurred()
            }
#endif
            let boundedPos = boundByView(point: translation.location, bound: size)
            position = (index: index, pos: boundedPos)
        } else {
            viewGradient[position: index] = valueForPosition(translation.location, in: size)
#if os(iOS)
            if position != nil {
                UIImpactFeedbackGenerator(style: .rigid).impactOccurred()
            }
#endif
            position = nil
        }
    }

    private func nodeFinishedDrag(index: Int, translation: DragGesture.Value) {
        if viewGradient.count > 2 && abs(translation.location.y - pickerSize) > slideHeight * 2 {
            viewGradient.remove(at: index)
            position = nil
        }
        gradient = viewGradient.export(allowLoop: allowLoop)
    }

    private func targetPos(index: Int, size: CGSize) -> CGPoint {
        if let position, position.index == index {
            position.pos
        } else {
            positionForValue(viewGradient[position: index], in: size)
        }
    }

    private func removing(index: Int) -> Bool {
        if let position {
            position.index == index
        } else {
            false
        }
    }

    private func boundByView(point: CGPoint, bound: CGSize) -> CGPoint {
        var boundedPoint = point
#if os(iOS)
        let verticalOffset = -pickerSize + barHeight - 33 + (allowLoop ? 0 : 10)
#elseif os(visionOS)
        let verticalOffset = -pickerSize + barHeight - 39 + (allowLoop ? 0 : 12)
#elseif os(macOS)
        let verticalOffset = -pickerSize + barHeight - 19
#endif
        boundedPoint.x = max(min(boundedPoint.x, bound.width - padding * 2), 0)
        boundedPoint.y = max(min(boundedPoint.y, bound.height + verticalOffset), verticalOffset)
        return boundedPoint
    }

    private func positionForValue(_ value: CGFloat, in size: CGSize) -> CGPoint {
        return CGPoint(x: (size.width - (pickerSize + padding) * 2) * value + pickerSize, y: slideHeight)
    }

    private func valueForPosition(_ position: CGPoint, in size: CGSize) -> CGFloat {
        let value = (position.x - pickerSize) / (size.width - (pickerSize + padding) * 2)
        return max(0.0, min(1.0, value))
    }
}

// MARK: macOS color selector

#if os(macOS)
class ColorNode: NSControl, @MainActor NSColorChanging {
    private let callBack: (NSColor) -> Void
    var color: NSColor {
        didSet {
            if let layer = self.layer as? CAShapeLayer {
                layer.fillColor = color.cgColor
            }
        }
    }

    init(frame frameRect: NSRect, color: NSColor, action: @escaping (NSColor) -> Void) {
        self.color = color
        self.callBack = action
        super.init(frame: frameRect)
        self.wantsLayer = true
        let colorLayer = CAShapeLayer()
        colorLayer.path = CGPath(ellipseIn: frameRect, transform: nil)
        colorLayer.fillColor = color.cgColor
        self.layer = colorLayer
        let clickGesture = NSClickGestureRecognizer(target: self, action: #selector(onTap(sender:)))
        self.addGestureRecognizer(clickGesture)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    @objc func onTap(sender: NSClickGestureRecognizer) {
        let colorPanel = NSColorPanel.shared
        colorPanel.setTarget(nil)
        colorPanel.setAction(nil)
        var position = convert(NSPoint(x: bounds.midX, y: bounds.midY), to: nil)
        position = window?.convertPoint(toScreen: position) ?? position
        position.x -= colorPanel.frame.width / 2
        position.y -= colorPanel.frame.height / 2
        colorPanel.setFrameOrigin(position)
        colorPanel.mode = .RGB
        colorPanel.showsAlpha = true
        colorPanel.colorSpace = .displayP3
        colorPanel.color = color
        colorPanel.orderFrontRegardless()
        colorPanel.setTarget(self)
        colorPanel.setAction(#selector(changeColor(_:)))
    }

    @objc func changeColor(_ sender: NSColorPanel?) {
        if let newColor = sender?.color {
            color = newColor
            callBack(newColor)
        }
    }
}

struct ColorNodeView: NSViewRepresentable {
    let size: CGSize
    @Binding var color: CGColor

    func makeNSView(context: Context) -> ColorNode {
        return ColorNode(frame: NSRect(origin: .zero, size: size), color: NSColor(cgColor: color)!, action: { color = $0.cgColor })
    }

    func updateNSView(_ nsView: ColorNode, context: Context) {
        nsView.color = NSColor(cgColor: color)!
    }
}
#endif

#Preview("Ring Setting", traits: .modifier(SampleData())) {
    NavigationStack {
        RingSetting()
    }
}
