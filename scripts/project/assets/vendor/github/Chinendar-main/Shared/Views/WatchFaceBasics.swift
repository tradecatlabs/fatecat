//
//  WatchFaceBasics.swift
//  Chinendar
//
//  Created by Leo Liu on 5/4/23.
//

import SwiftUI

private func changePhase(phase: CGFloat, angle: CGFloat) -> CGFloat {
    if phase >= 0 {
        return (angle + phase) %% 1.0
    } else {
        return (-angle + phase) %% 1.0
    }
}
private func changePhase(phase: CGFloat, angles: [CGFloat]) -> [CGFloat] {
    return angles.map { changePhase(phase: phase, angle: $0) }
}

class EntityNotes {
    struct EntityNote: Identifiable, Equatable {
        let name: String
        let ringIndex: Int
        let position: CGPoint
        let color: CGColor
        let id = UUID()

        static func == (lhs: EntityNotes.EntityNote, rhs: EntityNotes.EntityNote) -> Bool {
            return lhs.id == rhs.id
        }
    }

    var entities = [EntityNote]()
}

struct WatchFont {
    #if os(macOS)
        var font: NSFont
        init(_ font: NSFont) {
            self.font = font
        }
    #else
        var font: UIFont
        init(_ font: UIFont) {
            self.font = font
        }
    #endif
}

enum HighlightType {
    case none
    case alwaysOn
    case flicker
}

struct ZeroRing: View {
    static let width: CGFloat = 0.05
    let shortEdge: CGFloat
    let oddColor: CGColor
    let evenColor: CGColor
    let innerRing: RoundedRect
    let ringBoundPath: CGPath
    let oddTicksPath: CGPath
    let evenTicksPath: CGPath
    fileprivate let drawableTexts: [DrawableText]
#if !os(visionOS)
    @Environment(\.widgetRenderingMode) var renderingMode
#endif

    init(width: CGFloat, viewSize: CGSize, compact: Bool, textFont: WatchFont, outerRing: RoundedRect, startingAngle: CGFloat, oddTicks: [CGFloat], evenTicks: [CGFloat], oddColor: CGColor, evenColor: CGColor, oddTexts: [String], evenTexts: [String], offset: CGSize = .zero) {
        self.shortEdge = min(viewSize.width, viewSize.height)
        let longEdge = max(viewSize.width, viewSize.height)
        self.oddColor = oddColor
        self.evenColor = evenColor

        let innerRing = outerRing.shrink(by: width * shortEdge)
        self.innerRing = innerRing
        let textRing = outerRing.shrink(by: (width + 0.003)/2 * shortEdge)
        let ringBoundPath = outerRing.path
        self.ringBoundPath = ringBoundPath
        self.oddTicksPath = outerRing.arcPosition(lambdas: changePhase(phase: startingAngle, angles: oddTicks), width: 0.15 * shortEdge)
        self.evenTicksPath = outerRing.arcPosition(lambdas: changePhase(phase: startingAngle, angles: evenTicks), width: 0.15 * shortEdge)

        let fontSize: CGFloat = min(shortEdge * 0.03, longEdge * 0.025) * (compact ? 1.5 : 1.0)
        let font = textFont.font.withSize(fontSize)
        var drawableTexts = [DrawableText]()

        let oddPoints = textRing.arcPoints(lambdas: oddTicks.map { changePhase(phase: startingAngle, angle: $0) })
        for i in 0..<oddTexts.count {
            let tickName = oddTexts[i]
            let position = oddPoints[i]
            let texts = prepareText(tickName: tickName, at: position, font: WatchFont(font), compact: compact, color: oddColor, offset: offset)
            drawableTexts += texts
        }
        let evenPoints = textRing.arcPoints(lambdas: evenTicks.map { changePhase(phase: startingAngle, angle: $0) })
        for i in 0..<evenTexts.count {
            let tickName = evenTexts[i]
            let position = evenPoints[i]
            let texts = prepareText(tickName: tickName, at: position, font: WatchFont(font), compact: compact, color: evenColor, offset: offset)
            drawableTexts += texts
        }
        self.drawableTexts = drawableTexts
    }

    var body: some View {
        let majorLineWidth = shortEdge/300
#if !os(visionOS)
        let tinted = renderingMode == .accented
#else
        let tinted = false
#endif

        Canvas { context, _ in
            if tinted {
                context.addFilter(.luminanceToAlpha, options: .linearColor)
                let outlinePath = innerRing.path
                outlinePath.addPath(ringBoundPath)
                context.clip(to: Path(outlinePath), style: FillStyle(eoFill: true))
            } else {
                context.clip(to: Path(ringBoundPath), style: FillStyle(eoFill: true))
            }

            context.stroke(Path(oddTicksPath), with: .color(Color(cgColor: oddColor)), style: StrokeStyle(lineWidth: majorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))
            context.stroke(Path(evenTicksPath), with: .color(Color(cgColor: evenColor)), style: StrokeStyle(lineWidth: majorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))

            var transform = CGAffineTransform()
            var textContext = context
            for drawabeText in drawableTexts {
                if drawabeText.transform != transform {
                    textContext = context
                    textContext.concatenate(drawabeText.transform)
                }
                textContext.draw(Text(drawabeText.string).foregroundColor(Color(cgColor: drawabeText.color)), in: drawabeText.position)
                transform = drawabeText.transform
            }
        }
    }
}

struct Ring: View {
    static let paddedWidth: CGFloat = 0.07546
    let order: Int
    let alpha: CGFloat
    let width: CGFloat
    let majorTickAlpha: CGFloat
    let minorTickAlpha: CGFloat
    let shadowDirection: CGFloat
    let shadowSize: CGFloat
    let shortEdge: CGFloat
    let startingAngle: Angle
    let highlightAngle: Angle
    let outerRing: RoundedRect
    let innerRing: RoundedRect
    let outerRingPath: CGPath
    let majorTicksPath: CGPath
    let minorTicksPath: CGPath
    let minorTrackPath: CGPath
    let textMaskPath: CGPath
    let pathWithAngle: CGPath
    let majorTickColor: CGColor
    let minorTickColor: CGColor
    let backColor: CGColor
    let gradient: Gradient
    let highlightGradient: Gradient
    let highlightType: HighlightType
    fileprivate let drawableTexts: [DrawableText]
    fileprivate let drawableMarks: [DrawableMark]
#if !os(visionOS)
    @Environment(\.widgetRenderingMode) var renderingMode
#endif

    init(order: Int, width: CGFloat, viewSize: CGSize, compact: Bool, ticks: ChineseCalendar.Ticks, startingAngle: CGFloat, angle: CGFloat, textFont: WatchFont, textColor: CGColor, alpha: CGFloat, majorTickAlpha: CGFloat, minorTickAlpha: CGFloat, majorTickColor: CGColor, minorTickColor: CGColor, backColor: CGColor, gradientColor: CodableGradient, outerRing: RoundedRect, marks: [Marks], shadowDirection: CGFloat, entityNotes: EntityNotes?, shadowSize: CGFloat, highlightType: HighlightType, offset: CGSize = .zero) {
        self.order = order
        let shortEdge = min(viewSize.width, viewSize.height)
        self.shortEdge = shortEdge
        let longEdge = max(viewSize.width, viewSize.height)
        self.alpha = alpha
        self.width = width
        self.majorTickAlpha = majorTickAlpha
        self.minorTickAlpha = minorTickAlpha
        self.majorTickColor = majorTickColor
        self.minorTickColor = minorTickColor
        self.backColor = backColor
        self.outerRing = outerRing
        let innerRing = outerRing.shrink(by: width * shortEdge)
        self.innerRing = innerRing
        self.shadowDirection = shadowDirection
        self.shadowSize = shadowSize

        self.gradient = gradientColor.apply(startingAngle: startingAngle)
        let outerRingPath = outerRing.path
        self.outerRingPath = outerRingPath
        self.majorTicksPath = outerRing.arcPosition(lambdas: changePhase(phase: startingAngle, angles: ticks.majorTicks.map { CGFloat($0) }), width: 0.15 * shortEdge)
        self.minorTicksPath = outerRing.arcPosition(lambdas: changePhase(phase: startingAngle, angles: ticks.minorTicks.map { CGFloat($0) }), width: 0.15 * shortEdge)
        let minorTrackOuter = outerRing.shrink(by: width / 2 * shortEdge)
        let minorTrackPath = minorTrackOuter.path
        self.minorTrackPath = minorTrackPath

        let textRing = outerRing.shrink(by: (width - 0.005)/2 * shortEdge)
        let fontSize: CGFloat = min(shortEdge * 0.03, longEdge * 0.025) * (compact ? 1.5 : 1.0)
        let font = textFont.font.withSize(fontSize)
        let mappedTicks = ticks.majorTickNames.map { ChineseCalendar.Ticks.TickName(pos: changePhase(phase: startingAngle, angle: CGFloat($0.pos)), name: $0.name, active: $0.active) }
        let tickPositions: [RoundedRect.OrientedPoint] = textRing.arcPoints(lambdas: mappedTicks)
        var drawableTexts = [DrawableText]()
        let textMaskPath = CGMutablePath()
        for i in 0..<ticks.majorTickNames.count {
            let tickName = ticks.majorTickNames[i]
            let position = tickPositions[i]
            let textAlpha = textColor.alpha
            let color = textColor.copy(alpha: tickName.active ? textAlpha : (textAlpha * alpha))!
            let texts = prepareText(tickName: tickName.name, at: position, font: WatchFont(font), compact: compact, color: color, offset: offset)
            drawableTexts += texts
            for text in drawableTexts {
                textMaskPath.addPath(text.boundingBox)
            }
        }
        self.drawableTexts = drawableTexts
        self.textMaskPath = textMaskPath
        let (anglePath, realStartingAngle, realAngle, realLength) = anglePath(angle: angle, startingAngle: startingAngle, in: outerRing)
        self.pathWithAngle = anglePath
        self.startingAngle = Angle(radians: realStartingAngle)
        self.highlightAngle = Angle(radians: realAngle)
        self.highlightGradient = if startingAngle >= 0 {
            Gradient(stops: [.init(color: Color(white: 1, opacity: 0.5), location: 0),
                             .init(color: .clear, location: min(angle, width / 4 * shortEdge / realLength)),
                             .init(color: .clear, location: 1)])
        } else {
            Gradient(stops: [.init(color: .clear, location: 0),
                             .init(color: .clear, location: 1 - min(angle, width / 4 * shortEdge / realLength)),
                             .init(color: Color(white: 1, opacity: 0.5), location: 1)])
        }
        self.highlightType = highlightType
        entityNotes?.entities.removeAll { $0.ringIndex == order }

        var drawableMarks = [DrawableMark]()
        for mark in marks {
            let points: [RoundedRect.OrientedPoint]
            let mappedNames = mark.namedLocations.filter { $0.pos >= 0 && $0.pos < 1 }.map { ChineseCalendar.NamedPosition(name: $0.name, pos: changePhase(phase: startingAngle, angle: $0.pos)) }
            if mark.outer {
                points = outerRing.arcPoints(lambdas: mappedNames)
            } else {
                points = innerRing.arcPoints(lambdas: mappedNames)
            }

            for i in 0..<points.count {
                let point = points[i]
                let color = mark.colors[i]
                entityNotes?.entities.append(EntityNotes.EntityNote(name: point.name, ringIndex: order, position: point.position, color: color))
                var transform = CGAffineTransform(translationX: -point.position.x, y: -point.position.y)
                transform = transform.concatenating(CGAffineTransform(rotationAngle: -point.direction))
                transform = transform.concatenating(CGAffineTransform(translationX: point.position.x, y: point.position.y))
                let markPath: CGPath = RoundedRect(rect: CGRect(x: point.position.x - mark.radius, y: point.position.y - mark.radius, width: 2 * mark.radius, height: 2 * mark.radius), nodePos: 0.7 * mark.radius, ankorPos: 0.3 * mark.radius).path.copy(using: &transform)!
                let drawableMark = DrawableMark(path: markPath, radius: mark.radius, color: color)
                drawableMarks.append(drawableMark)
            }
        }
        self.drawableMarks = drawableMarks
    }

    var body: some View {
        let minorLineWidth = shortEdge/500
        let majorLineWidth = shortEdge/300
#if !os(visionOS)
        let tinted = renderingMode == .accented
#else
        let tinted = false
#endif

        if !tinted {
            Path(outerRingPath)
                .fill(.thickMaterial)
            Path(outerRingPath)
                .fill(Color(cgColor: backColor))
        }

        Canvas { graphicsContext, size in
            if tinted {
                graphicsContext.addFilter(.luminanceToAlpha, options: .linearColor)
            }

            var shadowContext = graphicsContext
            shadowContext.clip(to: Path(outerRingPath), options: .inverse)
            shadowContext.addFilter(.shadow(color: Color(white: 0, opacity: 0.5 * Double(tanh(shadowSize * 32))), radius: shadowSize * shortEdge,
                                      x: -shadowSize / 2 * sin(CGFloat.pi * 2 * shadowDirection) * shortEdge,
                                      y: -shadowSize / 2 * cos(CGFloat.pi * 2 * shadowDirection) * shortEdge, options: .shadowOnly))
            shadowContext.fill(Path(outerRing.path), with: .color(white: 1))

            var context = graphicsContext
            if tinted {
                let outlinePath = innerRing.path
                outlinePath.addPath(outerRingPath)
                context.clip(to: Path(outlinePath), style: FillStyle(eoFill: true))
            } else {
                context.clip(to: Path(outerRingPath), style: FillStyle(eoFill: true))
            }

            var gradientContext = context
            gradientContext.clipToLayer(options: .inverse) { ctx in
                ctx.addFilter(.luminanceToAlpha)
                ctx.fill(Path(roundedRect: CGRect(origin: .zero, size: size), cornerSize: .zero), with: .color(white: 0))
                if tinted {
                    var transform = CGAffineTransform()
                    var textContext = ctx
                    for drawabeText in drawableTexts {
                        if drawabeText.transform != transform {
                            textContext = ctx
                            textContext.concatenate(drawabeText.transform)
                        }
                        textContext.draw(Text(drawabeText.string).foregroundColor(.white), in: drawabeText.position)
                        transform = drawabeText.transform
                    }
                }
                ctx.clip(to: Path(textMaskPath), options: .inverse)
                ctx.stroke(Path(majorTicksPath), with: .color(white: 1 - majorTickAlpha), style: StrokeStyle(lineWidth: majorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))
                ctx.clip(to: Path(minorTrackPath), style: FillStyle(eoFill: true))
                ctx.stroke(Path(minorTicksPath), with: .color(white: 1 - minorTickAlpha), style: StrokeStyle(lineWidth: minorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))
            }

            var inactiveRingContext = gradientContext
            inactiveRingContext.clipToLayer(opacity: alpha) { cont in
                cont.fill(Path(CGRect(origin: .zero, size: size)), with: .color(white: 1))
            }
            inactiveRingContext.fill(Path(outerRingPath), with: .conicGradient(gradient, center: CGPoint(x: size.width/2, y: size.height/2), angle: startingAngle))
            gradientContext.clip(to: Path(pathWithAngle))
            gradientContext.fill(Path(outerRingPath), with: .conicGradient(gradient, center: CGPoint(x: size.width/2, y: size.height/2), angle: startingAngle))

            var tickContext = context
            tickContext.clip(to: Path(textMaskPath), options: .inverse)
            tickContext.stroke(Path(majorTicksPath), with: .color(Color(cgColor: majorTickColor)), style: StrokeStyle(lineWidth: majorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))
            tickContext.clip(to: Path(minorTrackPath), style: FillStyle(eoFill: true))
            tickContext.stroke(Path(minorTicksPath), with: .color(Color(cgColor: minorTickColor)), style: StrokeStyle(lineWidth: minorLineWidth, lineCap: .square, lineJoin: .bevel, miterLimit: .leastNonzeroMagnitude))

            var transform = CGAffineTransform()
            var textContext = context
            for drawabeText in drawableTexts {
                if drawabeText.transform != transform {
                    textContext = context
                    textContext.concatenate(drawabeText.transform)
                }
                textContext.draw(Text(drawabeText.string).foregroundColor(Color(cgColor: drawabeText.color)), in: drawabeText.position)
                transform = drawabeText.transform
            }

            for drawableMark in drawableMarks {
                var markContext = context
                markContext.addFilter(.shadow(color: Color(white: 0, opacity: 0.5), radius: drawableMark.radius/2, x: 0, y: 0))
                markContext.fill(Path(drawableMark.path), with: .color(Color(cgColor: drawableMark.color)))
            }
        }
#if !os(visionOS)
        .widgetAccentable()
#endif
        if highlightType != .none {
            TimelineView(.periodic(from: .now, by: 1)) { timeline in
                Canvas { context, size in
                    if tinted {
                        let outlinePath = innerRing.path
                        outlinePath.addPath(outerRingPath)
                        context.clip(to: Path(outlinePath), style: FillStyle(eoFill: true))
                    }
                    context.fill(Path(outerRingPath), with: .conicGradient(highlightGradient, center: CGPoint(x: size.width/2, y: size.height/2), angle: highlightAngle))
                }
                .blendMode(.hardLight)
                .blur(radius: width * shortEdge * 0.4)
                .opacity(highlightType == .flicker ? Double(Int(timeline.date.timeIntervalSince1970) % 2) : 1.0)
                .animation(.easeInOut(duration: 0.5), value: timeline.date)
            }
        }
    }
}

struct Core: View {
    let viewSize: CGSize
    let innerColor: CGColor
    let backColor: CGColor
    let shadowDirection: CGFloat
    let shadowSize: CGFloat
    let shortEdge: CGFloat
    let outerBoundPath: CGPath
    let gradient: Gradient
    fileprivate let drawableTexts: [DrawableText]
#if !os(visionOS)
    @Environment(\.widgetRenderingMode) var renderingMode
#endif

    init(viewSize: CGSize, dateString: String, timeString: String, font: WatchFont, maxLength: Int, textColor: CodableGradient, outerBound: RoundedRect, innerColor: CGColor, backColor: CGColor, centerOffset: CGFloat, shadowDirection: CGFloat, shadowSize: CGFloat) {
        self.viewSize = viewSize
        self.shortEdge = min(viewSize.width, viewSize.height)
        self.innerColor = innerColor
        self.backColor = backColor
        self.shadowDirection = shadowDirection
        self.shadowSize = shadowSize
        self.outerBoundPath = outerBound.path
        self.gradient = textColor.apply(startingAngle: -1)
        var drawableTexts = prepareCoreText(text: dateString, offsetRatio: 0.7, centerOffset: centerOffset, outerBound: outerBound, maxLength: maxLength, viewSize: viewSize, font: font)
        drawableTexts += prepareCoreText(text: timeString, offsetRatio: -0.7, centerOffset: centerOffset, outerBound: outerBound, maxLength: maxLength, viewSize: viewSize, font: font)
        self.drawableTexts = drawableTexts
    }

    var body: some View {
#if !os(visionOS)
        let tinted = renderingMode == .accented
#else
        let tinted = false
#endif

        if !tinted {
            Path(outerBoundPath)
                .fill(.thickMaterial)
            Path(outerBoundPath)
                .fill(Color(cgColor: backColor))
        }

        Canvas { context, _ in
            if !tinted {
                var shadowContext = context
                shadowContext.clip(to: Path(outerBoundPath), options: .inverse)
                shadowContext.addFilter(.shadow(color: Color(white: 0, opacity: 0.5 * Double(tanh(shadowSize * 32))), radius: shadowSize * shortEdge,
                                          x: -shadowSize / 2 * sin(CGFloat.pi * 2 * shadowDirection) * shortEdge,
                                          y: -shadowSize / 2 * cos(CGFloat.pi * 2 * shadowDirection) * shortEdge, options: .shadowOnly))
                shadowContext.fill(Path(outerBoundPath), with: .color(white: 1))

                context.fill(Path(outerBoundPath), with: .color(Color(cgColor: innerColor)))
            }

            var startPoint = CGPoint(x: viewSize.width/2, y: viewSize.height/2)
            var endPoint = startPoint

            var textContext = context
            textContext.clipToLayer { ctx in
                for text in drawableTexts {
                    let resolved = ctx.resolve(Text(text.string))
                    ctx.draw(resolved, at: CGPoint(x: text.position.midX, y: text.position.midY))
                    startPoint.x = min(startPoint.x, text.position.minX)
                    startPoint.y = max(startPoint.y, text.position.maxY)
                    endPoint.x = max(endPoint.x, text.position.maxX)
                    endPoint.y = min(endPoint.y, text.position.minY)
                }
            }

            textContext.fill(Path(outerBoundPath), with: .linearGradient(gradient, startPoint: startPoint, endPoint: endPoint))
        }
    }
}

struct Marks {
    static let markSize: CGFloat = 0.012
    let outer: Bool
    let namedLocations: [ChineseCalendar.NamedPosition]
    let colors: [CGColor]
    let radius: CGFloat

    static func pairMarkPositionColor(rawPositions: [ChineseCalendar.NamedPosition?], rawColors: [CGColor]) -> ([ChineseCalendar.NamedPosition], [CGColor]) {
        var newPositions = [ChineseCalendar.NamedPosition]()
        var newColors = [CGColor]()
        for i in 0..<rawPositions.count {
            if let pos = rawPositions[i] {
                newPositions.append(pos)
                newColors.append(rawColors[i % rawColors.count])
            }
        }
        return (pos: newPositions, color: newColors)
    }

    init(outer: Bool, locations: [ChineseCalendar.NamedPosition?], colors: [CGColor], radius: CGFloat) {
        self.outer = outer
        let (pos, col) = Marks.pairMarkPositionColor(rawPositions: locations, rawColors: colors)
        self.namedLocations = pos
        self.colors = col
        self.radius = radius
    }
}

private struct DrawableText {
    let string: AttributedString
    let position: CGRect
    let boundingBox: CGPath
    let transform: CGAffineTransform
    let color: CGColor
}

private struct DrawableMark {
    let path: CGPath
    let radius: CGFloat
    let color: CGColor
}

private func prepareText(tickName: String, at point: RoundedRect.OrientedPoint, font: WatchFont, compact: Bool, color: CGColor, offset: CGSize) -> [DrawableText] {
    let string: String
    var hasSpace = false
    let fontSize = font.font.pointSize
    if compact {
        hasSpace = tickName.firstIndex(of: "　") != nil
        string = String(tickName.replacingOccurrences(of: "　", with: ""))
    } else {
        string = tickName
    }
    let attrStr = NSMutableAttributedString(string: string)
    attrStr.addAttributes([.font: font.font, .foregroundColor: color], range: NSRange(location: 0, length: attrStr.length))

    var boxTransform = CGAffineTransform(translationX: -point.position.x, y: -point.position.y)
    let transform: CGAffineTransform
    if point.direction <= CGFloat.pi/4 {
        transform = CGAffineTransform(rotationAngle: -point.direction)
    } else if point.direction < CGFloat.pi * 3/4 {
        transform = CGAffineTransform(rotationAngle: CGFloat.pi/2 - point.direction)
    } else if point.direction < CGFloat.pi * 5/4 {
        transform = CGAffineTransform(rotationAngle: CGFloat.pi - point.direction)
    } else if point.direction < CGFloat.pi * 7/4 {
        transform = CGAffineTransform(rotationAngle: -point.direction - CGFloat.pi/2)
    } else {
        transform = CGAffineTransform(rotationAngle: -point.direction)
    }
    boxTransform = boxTransform.concatenating(transform)
    boxTransform = boxTransform.concatenating(CGAffineTransform(translationX: point.position.x, y: point.position.y))

    let characters = string.map { NSMutableAttributedString(string: String($0), attributes: attrStr.attributes(at: 0, effectiveRange: nil)) }
    let mean = CGFloat(characters.count - 1)/2

    var text = [DrawableText]()
    for i in 0..<characters.count {
        let shift = (CGFloat(i) - mean) * fontSize * (hasSpace ? 1.5 : 0.95)
        var box = characters[i].boundingRect(with: CGSize.zero, options: .usesLineFragmentOrigin, context: .none)
        box.origin = CGPoint(x: point.position.x - box.width/2, y: point.position.y - box.height/2)
        let cornerSize = 0.2 * min(box.height, box.width)
        if (point.direction > CGFloat.pi/4 && point.direction < CGFloat.pi * 3/4) || (point.direction > CGFloat.pi * 5/4 && point.direction < CGFloat.pi * 7/4) {
            box.origin.y += shift
            box.origin.x += offset.width * pow(fontSize, 0.9)
        } else {
            box.origin.x -= shift
            box.origin.y -= offset.height * pow(fontSize, 0.9)
        }
        let boxPath = CGPath(roundedRect: box, cornerWidth: cornerSize, cornerHeight: cornerSize, transform: &boxTransform)
        text.append(DrawableText(string: AttributedString(characters[i]), position: box, boundingBox: boxPath, transform: boxTransform, color: color))
    }
    return text
}

private func prepareCoreText(text: String, offsetRatio: CGFloat, centerOffset: CGFloat, outerBound: RoundedRect, maxLength: Int, viewSize: CGSize, font: WatchFont) -> [DrawableText] {
    let centerTextShortSize = min(outerBound._boundBox.width, outerBound._boundBox.height) * 0.31
    let centerTextLongSize = max(outerBound._boundBox.width, outerBound._boundBox.height) * 0.17
    let centerTextSize = min(centerTextShortSize, centerTextLongSize) * sqrt(5/CGFloat(maxLength))
    let isVertical = viewSize.height >= viewSize.width
    let minSeparation = min(outerBound._boundBox.width, outerBound._boundBox.height) / 5
    var offset = min(centerTextSize * abs(offsetRatio) * sqrt(CGFloat(maxLength)/3), minSeparation)
    offset *= offsetRatio >= 0 ? 1.0 : -1.0
    offset += centerTextSize * centerOffset * sqrt(CGFloat(maxLength)/3)

    var drawableTexts = [DrawableText]()
    let centerFont = font.font.withSize(centerTextSize)

    let attrStr = NSMutableAttributedString(string: text)
    attrStr.addAttributes([.font: centerFont, .foregroundColor: CGColor(gray: 1, alpha: 1)], range: NSRange(location: 0, length: attrStr.length))

    var characters = attrStr.string.map { NSMutableAttributedString(string: String($0), attributes: attrStr.attributes(at: 0, effectiveRange: nil)) }
    if characters.count > maxLength {
        characters = Array(characters[..<maxLength])
    }

    for i in 0..<characters.count {
        let mean = CGFloat(characters.count - 1)/2
        let shift = (CGFloat(i) - mean) * centerTextSize
        var box = characters[i].boundingRect(with: .zero, options: .usesLineFragmentOrigin, context: .none)
        if isVertical {
            box.origin = CGPoint(x: viewSize.width/2 + offset - box.width/2, y: viewSize.height/2 + shift - box.height/2 - (box.height - centerTextSize)/5)
        } else {
            box.origin = CGPoint(x: viewSize.width/2 - shift - box.width/2, y: viewSize.height/2 - offset - box.height/2)
        }
        drawableTexts.append(DrawableText(string: AttributedString(characters[i]), position: box, boundingBox: CGMutablePath(), transform: CGAffineTransform(), color: CGColor(gray: 1, alpha: 1)))
    }
    return drawableTexts
}

private func anglePath(angle: CGFloat, startingAngle: CGFloat, in circle: RoundedRect) -> (CGMutablePath, CGFloat, CGFloat, CGFloat) {
    let radius = sqrt(pow(circle._boundBox.width, 2)+pow(circle._boundBox.height, 2))
    let center = CGPoint(x: circle._boundBox.midX, y: circle._boundBox.midY)
    let anglePoints = circle.arcPoints(lambdas: [startingAngle %% 1.0, (startingAngle+(startingAngle >= 0 ? angle : -angle)) %% 1.0])
    let realStartingAngle = atan2(anglePoints[0].position.y - center.y, anglePoints[0].position.x - center.x)
    let realAngle = atan2(anglePoints[1].position.y - center.y, anglePoints[1].position.x - center.x)
    let realLength = sqrt(pow(anglePoints[1].position.y - center.y, 2) + pow(anglePoints[1].position.x - center.x, 2))
    let path = CGMutablePath()
    path.move(to: center)
    path.addLine(to: center+CGPoint(x: radius * cos(realStartingAngle), y: radius * sin(realStartingAngle)))
    path.addArc(center: center, radius: radius, startAngle: realStartingAngle, endAngle: realAngle, clockwise: startingAngle >= 0)
    path.closeSubpath()
    return (path, realStartingAngle, realAngle, realLength)
}
