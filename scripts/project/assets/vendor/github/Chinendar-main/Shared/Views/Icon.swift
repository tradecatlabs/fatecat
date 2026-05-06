//
//  Icon.swift
//  Chinendar
//
//  Created by Leo Liu on 1/29/24.
//

import SwiftUI

struct Icon: View {
    @Environment(\.colorScheme) var colorScheme
    let watchLayout: WatchLayout
    let widthScale: CGFloat
    let preview: Bool
    var baseLayout: BaseLayout {
        watchLayout.baseLayout
    }

    init(watchLayout: WatchLayout, preview: Bool = false) {
        self.watchLayout = watchLayout
        self.preview = preview
        if preview {
            widthScale = 1.1
        } else {
            widthScale = 1.5
        }
    }

    var body: some View {
        let isDark = colorScheme == .dark
        let coreColor = baseLayout.colors.innerColor.color(inDark: isDark)
        let backColor = baseLayout.colors.backColor.color(inDark: isDark)
        let clearColor = CGColor(gray: 0, alpha: 0)
        let shadowDirection = 0.62

        GeometryReader { proxy in

            let size = proxy.size
            let shortEdge = min(size.width, size.height)
            let cornerSize = baseLayout.offsets.cornerRadiusRatio * shortEdge
            let outerBound = RoundedRect(rect: CGRect(origin: .zero, size: size), nodePos: cornerSize, ankorPos: cornerSize * 0.2)
            let firstRingOuter = outerBound.shrink(by: ZeroRing.width * shortEdge * widthScale)
            let secondRingOuter = firstRingOuter.shrink(by: Ring.paddedWidth * shortEdge * widthScale)
            let thirdRingOuter = secondRingOuter.shrink(by: Ring.paddedWidth * shortEdge * widthScale)
            let innerBound = if preview {
                thirdRingOuter.shrink(by: Ring.paddedWidth * shortEdge * widthScale)
            } else {
                secondRingOuter.shrink(by: Ring.paddedWidth * shortEdge * widthScale)
            }

            ZStack {
                Ring(order: 1, width: Ring.paddedWidth * widthScale, viewSize: size, compact: false, ticks: ChineseCalendar.Ticks(), startingAngle: 0, angle: preview ? 0.9 : 0.3, textFont: WatchFont(watchLayout.textFont), textColor: clearColor, alpha: baseLayout.colors.shadeAlpha, majorTickAlpha: 1, minorTickAlpha: 1, majorTickColor: clearColor, minorTickColor: clearColor, backColor: backColor, gradientColor: baseLayout.colors.firstRing, outerRing: firstRingOuter, marks: [], shadowDirection: shadowDirection, entityNotes: nil, shadowSize: baseLayout.colors.shadowSize, highlightType: .flicker, offset: .zero)
                Ring(order: 2, width: Ring.paddedWidth * widthScale, viewSize: size, compact: false, ticks: ChineseCalendar.Ticks(), startingAngle: 0, angle: preview ? 0.8 : 0.45, textFont: WatchFont(watchLayout.textFont), textColor: clearColor, alpha: baseLayout.colors.shadeAlpha, majorTickAlpha: 1, minorTickAlpha: 1, majorTickColor: clearColor, minorTickColor: clearColor, backColor: backColor, gradientColor: baseLayout.colors.secondRing, outerRing: secondRingOuter, marks: [], shadowDirection: shadowDirection, entityNotes: nil, shadowSize: baseLayout.colors.shadowSize, highlightType: .flicker, offset: .zero)
                if preview {
                    Ring(order: 3, width: Ring.paddedWidth * widthScale, viewSize: size, compact: false, ticks: ChineseCalendar.Ticks(), startingAngle: 0, angle: 0.7, textFont: WatchFont(watchLayout.textFont), textColor: clearColor, alpha: baseLayout.colors.shadeAlpha, majorTickAlpha: 1, minorTickAlpha: 1, majorTickColor: clearColor, minorTickColor: clearColor, backColor: backColor, gradientColor: baseLayout.colors.thirdRing, outerRing: thirdRingOuter, marks: [], shadowDirection: shadowDirection, entityNotes: nil, shadowSize: baseLayout.colors.shadowSize, highlightType: .flicker, offset: .zero)
                }
                Core(viewSize: size, dateString: "", timeString: "", font: WatchFont(watchLayout.centerFont), maxLength: 5, textColor: baseLayout.colors.centerFontColor, outerBound: innerBound, innerColor: coreColor, backColor: backColor, centerOffset: 0, shadowDirection: shadowDirection, shadowSize: baseLayout.colors.shadowSize)
            }
        }
    }
}

#Preview("Icon") {
    let watchLayout = WatchLayout.defaultLayout
    return Icon(watchLayout: watchLayout)
        .frame(width: 120, height: 120)
}
