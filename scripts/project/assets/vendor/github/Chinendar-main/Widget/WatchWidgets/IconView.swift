//
//  IconViews.swift
//  WatchWidgetExtension
//
//  Created by Leo Liu on 5/12/23.
//

import SwiftUI

enum IconType {
    case solarTerm(view: SolarTerm)
    case moon(view: MoonPhase)
    case sunrise(view: Sun)
    case date(view: SunMoon)
}

struct SolarTerm: View {
    let angle: CGFloat
    let color: CGColor

    func pointOnCircle(center: CGPoint, radius: CGFloat, angle: CGFloat) -> CGPoint {
        return CGPoint(x: sin(angle) * radius + center.x, y: cos(angle) * radius + center.y)
    }

    var body: some View {
        Canvas { context, size in
            let minEdge = min(size.width, size.height)
            let center = CGPoint(x: size.width / 2, y: size.height / 2)
            let centerRadius = minEdge * 0.3
            let ringRadius = minEdge * 0.42
            let starRadius = minEdge * 0.08
            let smallStarRadius = minEdge * 0.06

            let connectionPath = CGMutablePath()
            connectionPath.move(to: pointOnCircle(center: center, radius: centerRadius, angle: 0.4 * CGFloat.pi))
            connectionPath.addLine(to: pointOnCircle(center: center, radius: centerRadius, angle: 0.6 * CGFloat.pi))
            connectionPath.addCurve(to: pointOnCircle(center: CGPoint(x: ringRadius, y: 0) + center, radius: starRadius, angle: 1.3 * CGFloat.pi),
                                    control1: CGPoint(x: centerRadius, y: 0) + center,
                                    control2: CGPoint(x: ringRadius - starRadius * 1.2, y: 0) + center)
            connectionPath.addLine(to: pointOnCircle(center: CGPoint(x: ringRadius, y: 0) + center, radius: starRadius, angle: 1.7 * CGFloat.pi))
            connectionPath.addCurve(to: pointOnCircle(center: center, radius: centerRadius, angle: 0.4 * CGFloat.pi),
                                    control1: CGPoint(x: ringRadius - starRadius * 1.2, y: 0) + center,
                                    control2: CGPoint(x: centerRadius, y: 0) + center)
            connectionPath.closeSubpath()

            let circlesPath = CGMutablePath()
            circlesPath.addEllipse(in: CGRect(origin: center - CGPoint(x: centerRadius, y: centerRadius), size: CGSize(width: centerRadius * 2, height: centerRadius * 2)))
            circlesPath.addEllipse(in: CGRect(origin: center - CGPoint(x: starRadius - ringRadius, y: starRadius), size: CGSize(width: starRadius * 2, height: starRadius * 2)))

            let dotsPath = CGMutablePath()
            for i in 1...11 {
                let center = pointOnCircle(center: center, radius: ringRadius, angle: CGFloat(i) * CGFloat.pi * 2 / 12 + 0.5 * CGFloat.pi) - CGPoint(x: smallStarRadius, y: smallStarRadius)
                dotsPath.addEllipse(in: CGRect(origin: center, size: CGSize(width: smallStarRadius * 2, height: smallStarRadius * 2)))
            }

            context.fill(Path(connectionPath), with: .color(Color(cgColor: color)))
            context.fill(Path(circlesPath), with: .color(Color(cgColor: color)))
            context.fill(Path(dotsPath), with: .color(.yellow.opacity(0.5)))
        }
        .rotationEffect(.radians(-(angle - 0.25) * CGFloat.pi * 2.0))
    }
}

struct MoonPhase: View {
    let angle: CGFloat
    let color: CGColor
    let rise: Bool?

    init(angle: CGFloat, color: CGColor, rise: Bool? = nil) {
        self.angle = angle
        self.color = color
        self.rise = rise
    }

    func pointOnCircle(center: CGPoint, radius: CGFloat, angle: CGFloat) -> CGPoint {
        return CGPoint(x: sin(angle) * radius + center.x, y: cos(angle) * radius + center.y)
    }

    var body: some View {
        Canvas { context, size in
            let minEdge = min(size.width, size.height)
            let center = CGPoint(x: size.width / 2, y: size.height / 2)
            let centerRadius = minEdge * 0.3
            let ringRadius = minEdge * 0.42
            let starRadius = minEdge * 0.1

            context.clip(to: Path(ellipseIn: CGRect(x: center.x - minEdge * 0.5, y: center.y - minEdge * 0.5, width: minEdge, height: minEdge)))
            var moonContext = context

            if rise != nil {
                let groundMaskPath = CGMutablePath()
                groundMaskPath.addArc(center: center, radius: minEdge * 0.5, startAngle: 0.2 * CGFloat.pi, endAngle: 0.80 * CGFloat.pi, clockwise: false)
                groundMaskPath.closeSubpath()

                let groundPath = CGMutablePath()
                groundPath.addArc(center: center, radius: minEdge * 0.5, startAngle: 0.23 * CGFloat.pi, endAngle: 0.77 * CGFloat.pi, clockwise: false)
                groundPath.closeSubpath()

                let groundContext = context
                groundContext.fill(Path(groundPath), with: .color(.brown))
                moonContext.clip(to: Path(groundMaskPath), options: .inverse)
                moonContext.translateBy(x: 0, y: minEdge * 0.10)
            }
            let backContext = moonContext

            let width = centerRadius * (1.0 + cos(4.0 * CGFloat.pi * angle)) / 2.0
            let ellipse = CGMutablePath(ellipseIn: CGRect(x: center.x - width, y: center.y - centerRadius, width: width * 2, height: centerRadius * 2), transform: nil)
            if cos(2.0 * CGFloat.pi * angle) >= 0 {
                moonContext.clip(to: Path(ellipse), options: .inverse)
            } else {
                moonContext.fill(Path(ellipse), with: .color(Color(cgColor: color)))
            }

            let halfMoon = CGMutablePath()
            if sin(2.0 * CGFloat.pi * angle) >= 0 {
                halfMoon.addArc(center: center, radius: centerRadius, startAngle: -0.5 * CGFloat.pi, endAngle: 0.5 * CGFloat.pi, clockwise: true)
            } else {
                halfMoon.addArc(center: center, radius: centerRadius, startAngle: 0.5 * CGFloat.pi, endAngle: -0.5 * CGFloat.pi, clockwise: true)
            }
            halfMoon.closeSubpath()
            moonContext.fill(Path(halfMoon), with: .color(Color(cgColor: color)))

            let circle = CGMutablePath(ellipseIn: CGRect(x: center.x - centerRadius, y: center.y - centerRadius, width: centerRadius * 2, height: centerRadius * 2), transform: nil)
            backContext.fill(Path(circle), with: .color(Color(cgColor: color).opacity(0.2 * color.alpha)))

            for position in [0.2, 0.4, 0.76] {
                let direction = pointOnCircle(center: center, radius: ringRadius, angle: (position + angle * 0.02) * CGFloat.pi * 2.0)
                let star = starPath(x: direction.x, y: direction.y, radius: starRadius * (0.75 + 0.25 * cos(angle * CGFloat.pi * 2.0)), sides: 5, pointyness: 0.5)
                moonContext.fill(Path(star), with: .color(.yellow.opacity(0.75 + 0.25 * cos(angle * CGFloat.pi * 2.0))))
            }

            if let rise {
                var arrow = context
                arrow.clipToLayer { ctx in
                    var abc = ctx
                    abc.translateBy(x: center.x, y: center.y)
                    abc.rotate(by: .degrees(90))
                    abc.translateBy(x: -center.x, y: -center.y)
                    let arrowName = rise ? "arrowshape.left.fill" : "arrowshape.right.fill"
                    abc.draw(Image(systemName: arrowName), in: CGRect(x: minEdge * 0.0, y: center.y - minEdge * 0.12, width: minEdge * 0.24, height: minEdge * 0.24))
                }
                arrow.fill(Path(ellipseIn: CGRect(origin: .zero, size: CGSize(width: minEdge, height: minEdge))), with: .color(rise ? .orange : .teal))
            }
        }
    }
}

struct Sun: View {
    let color: CGColor
    let rise: Bool?

    init(color: CGColor, rise: Bool? = nil) {
        self.color = color
        self.rise = rise
    }

    var body: some View {
        Canvas { context, size in
            let minEdge = min(size.width, size.height)
            let center = CGPoint(x: size.width / 2, y: size.height / 2)
            let centerRadius = minEdge * 0.3
            let ringRadius = minEdge * 0.42
            let smallStarRadius = minEdge * 0.08

            context.clip(to: Path(ellipseIn: CGRect(x: center.x - minEdge * 0.5, y: center.y - minEdge * 0.5, width: minEdge, height: minEdge)))
            var sunContext = context

            if rise != nil {
                let groundMaskPath = CGMutablePath()
                groundMaskPath.addArc(center: center, radius: minEdge * 0.5, startAngle: 0.20 * CGFloat.pi, endAngle: 0.80 * CGFloat.pi, clockwise: false)
                groundMaskPath.closeSubpath()

                let groundPath = CGMutablePath()
                groundPath.addArc(center: center, radius: minEdge * 0.5, startAngle: 0.23 * CGFloat.pi, endAngle: 0.77 * CGFloat.pi, clockwise: false)
                groundPath.closeSubpath()

                let groundContext = context
                groundContext.fill(Path(groundPath), with: .color(.brown))
                sunContext.clip(to: Path(groundMaskPath), options: .inverse)
                sunContext.translateBy(x: 0, y: minEdge * 0.1)
            }

            let mainCircle = CGMutablePath(ellipseIn: CGRect(x: center.x - centerRadius, y: center.y - centerRadius, width: centerRadius * 2, height: centerRadius * 2), transform: nil)

            let radiationPath = CGMutablePath()
            for i in 0...11 {
                radiationPath.move(to: pointOnCircle(center: center, radius: ringRadius - smallStarRadius, angle: CGFloat(i) / 12.0 * CGFloat.pi * 2.0))
                radiationPath.addCurve(to: pointOnCircle(center: center, radius: ringRadius - smallStarRadius, angle: CGFloat(i) / 12.0 * CGFloat.pi * 2.0),
                                       control1: pointOnCircle(center: center, radius: ringRadius + smallStarRadius, angle: (CGFloat(i) + 0.5) / 12.0 * CGFloat.pi * 2.0),
                                       control2: pointOnCircle(center: center, radius: ringRadius + smallStarRadius, angle: (CGFloat(i) - 0.1) / 12.0 * CGFloat.pi * 2.0))
                radiationPath.closeSubpath()
            }

            sunContext.fill(Path(mainCircle), with: .color(Color(cgColor: color)))
            sunContext.fill(Path(radiationPath), with: .color(.yellow))

            if let rise {
                var arrow = context
                arrow.clipToLayer { ctx in
                    var abc = ctx
                    abc.translateBy(x: center.x, y: center.y)
                    abc.rotate(by: .degrees(90))
                    abc.translateBy(x: -center.x, y: -center.y)
                    let arrowName = rise ? "arrowshape.left.fill" : "arrowshape.right.fill"
                    abc.draw(Image(systemName: arrowName), in: CGRect(x: minEdge * 0.0, y: center.y - minEdge * 0.12, width: minEdge * 0.24, height: minEdge * 0.24))
                }
                arrow.fill(Path(ellipseIn: CGRect(origin: .zero, size: CGSize(width: minEdge, height: minEdge))), with: .color(rise ? .orange : .teal))
            }
        }
    }
}

struct SunMoon: View {
    let month: Int
    let day: Int
    let orbitColor = CGColor(red: 0.6, green: 0.6, blue: 0.6, alpha: 1)
    let moonColor = CGColor(red: 0.9, green: 0.7, blue: 0.0, alpha: 1)

    var body: some View {
        Canvas { context, size in
            let minEdge = min(size.width, size.height)
            let center = CGPoint(x: size.width / 2, y: size.height / 2)
            let orbitRadius = minEdge * 0.3
            let moonRadius = minEdge * 0.4

            let monthPosition = Double((month - 1) %% 12) / 12.0
            let moonPhase = Double((day  - 1) %% 30) / 30.0
            let iconCenter = pointOnCircle(center: center, radius: 0.5 * moonRadius, angle: (monthPosition + 0.5) * 2 * Double.pi)
            let moonCenter = pointOnCircle(center: iconCenter, radius: orbitRadius, angle: monthPosition * 2 * Double.pi)
            let iconTranslation = CGAffineTransform(translationX: iconCenter.x - center.x, y: iconCenter.y - center.y)
            var moonTranslation = CGAffineTransform(translationX: moonCenter.x - iconCenter.x, y: moonCenter.y - iconCenter.y)
            let moonOutline = CGPath(ellipseIn: CGRect(x: center.x - moonRadius, y: center.y - moonRadius, width: 2 * moonRadius, height: 2 * moonRadius), transform: &moonTranslation)
            let orbitCircle = CGPath(ellipseIn: CGRect(x: center.x - orbitRadius, y: center.y - orbitRadius, width: orbitRadius * 2, height: orbitRadius * 2), transform: nil)

            var moonContext = context
            var orbitContext = context
            moonContext.transform = iconTranslation.concatenating(moonTranslation)
            orbitContext.transform = iconTranslation

            orbitContext.clip(to: Path(moonOutline), options: .inverse)
            orbitContext.stroke(Path(orbitCircle), with: .color(Color(cgColor: orbitColor)), style: .init(lineWidth: 0.02 * minEdge, lineCap: .round, dash: [2 * Double.pi * orbitRadius / 24], dashPhase: 2 * Double.pi * orbitRadius / 48))

            let moonBackContext = moonContext
            let width = moonRadius * (1.0 + cos(4.0 * CGFloat.pi * moonPhase)) / 2.0
            let ellipse = CGMutablePath(ellipseIn: CGRect(x: center.x - width, y: center.y - moonRadius, width: width * 2, height: moonRadius * 2), transform: nil)
            if cos(2.0 * CGFloat.pi * moonPhase) >= 0 {
                moonContext.clip(to: Path(ellipse), options: .inverse)
            } else {
                moonContext.fill(Path(ellipse), with: .color(Color(cgColor: moonColor)))
            }

            let halfMoon = CGMutablePath()
            if sin(2.0 * CGFloat.pi * moonPhase) >= 0 {
                halfMoon.addArc(center: center, radius: moonRadius, startAngle: -0.5 * CGFloat.pi, endAngle: 0.5 * CGFloat.pi, clockwise: true)
            } else {
                halfMoon.addArc(center: center, radius: moonRadius, startAngle: 0.5 * CGFloat.pi, endAngle: -0.5 * CGFloat.pi, clockwise: true)
            }
            halfMoon.closeSubpath()
            moonContext.fill(Path(halfMoon), with: .color(Color(cgColor: moonColor)))

            let circle = CGMutablePath(ellipseIn: CGRect(x: center.x - moonRadius, y: center.y - moonRadius, width: moonRadius * 2, height: moonRadius * 2), transform: nil)
            moonBackContext.fill(Path(circle), with: .color(Color(cgColor: moonColor).opacity(0.2 * moonColor.alpha)))
        }
    }
}

private func starPath(x: CGFloat, y: CGFloat, radius: CGFloat, sides: Int, pointyness: CGFloat) -> CGPath {
    func polygonPointArray(sides: Int, x: CGFloat, y: CGFloat, radius: CGFloat, adjustment: CGFloat = 0) -> [CGPoint] {
        let angle = 2 * CGFloat.pi / CGFloat(sides)
        let cx = x // x origin
        let cy = y // y origin
        let r = radius // radius of circle
        var i = sides
        var points = [CGPoint]()
        while points.count <= sides {
            let xpo = cx - r * cos(angle * CGFloat(i) + adjustment * 2 * CGFloat.pi)
            let ypo = cy - r * sin(angle * CGFloat(i) + adjustment * 2 * CGFloat.pi)
            points.append(CGPoint(x: xpo, y: ypo))
            i -= 1
        }
        return points
    }

    let adjustment = 0.5 / CGFloat(sides)
    let path = CGMutablePath()
    let points = polygonPointArray(sides: sides, x: x, y: y, radius: radius)
    let points2 = polygonPointArray(sides: sides, x: x, y: y, radius: radius * pointyness, adjustment: adjustment)
    path.move(to: points[0])
    for i in 0 ..< points.count {
        path.addLine(to: points2[i])
        path.addLine(to: points[i])
    }
    path.closeSubpath()
    return path
}

private func pointOnCircle(center: CGPoint, radius: CGFloat, angle: CGFloat) -> CGPoint {
    return CGPoint(x: sin(angle) * radius + center.x, y: cos(angle) * radius + center.y)
}

#Preview("SolarTerm") {
    SolarTerm(angle: 0.4, color: Color.white.cgColor!)
}

#Preview("MoonPhase") {
    MoonPhase(angle: 0.4, color: CGColor(red: 0.9, green: 0.6, blue: 0.3, alpha: 1))
}

#Preview("Moonrise") {
    MoonPhase(angle: 0.4, color: CGColor(red: 0.9, green: 0.6, blue: 0.3, alpha: 1), rise: true)
}

#Preview("Sunrise") {
    Sun(color: CGColor(red: 0.9, green: 0.2, blue: 0.1, alpha: 1), rise: true)
}

#Preview("SunMoon") {
    SunMoon(month: 8, day: 15)
}
