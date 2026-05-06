//
//  RoundedRect.swift
//  Chinendar
//
//  Created by Leo Liu on 5/3/23.
//

import CoreGraphics
import Foundation

struct RoundedRect {
    let _boundBox: CGRect
    let _nodePos: CGFloat
    let _ankorPos: CGFloat

    init(rect: CGRect, nodePos: CGFloat, ankorPos: CGFloat) {
        _boundBox = rect
        _nodePos = nodePos
        _ankorPos = ankorPos
    }

    private func drawPath(vertex: [CGPoint]) -> CGMutablePath {
        let path = CGMutablePath()
        var previousPoint = vertex[vertex.count - 1]
        var point = vertex[0]
        var nextPoint: CGPoint
        var control1: CGPoint
        var control2: CGPoint
        var target = previousPoint
        var diff: CGPoint
        target.x -= _nodePos
        path.move(to: target)
        for i in 0..<vertex.count {
            previousPoint = vertex[(vertex.count+i - 1)%vertex.count]
            point = vertex[i]
            nextPoint = vertex[(i+1)%vertex.count]
            target = point
            control1 = point
            diff = point - previousPoint
            if abs(diff.x) >= abs(diff.y) {
                target.x -= diff.x >= 0 ? _nodePos : -_nodePos
                control1.x -= diff.x >= 0 ? _ankorPos : -_ankorPos
            } else {
                target.y -= diff.y >= 0 ? _nodePos : -_nodePos
                control1.y -= diff.y >= 0 ? _ankorPos : -_ankorPos
            }
            path.addLine(to: target)
            target = point
            control2 = point
            diff = nextPoint - point
            if abs(diff.x) > abs(diff.y) {
                control2.x += diff.x >= 0 ? _ankorPos : -_ankorPos
                target.x += diff.x >= 0 ? _nodePos : -_nodePos
            } else {
                control2.y += diff.y >= 0 ? _ankorPos : -_ankorPos
                target.y += diff.y >= 0 ? _nodePos : -_nodePos
            }
            path.addCurve(to: target, control1: control1, control2: control2)
        }
        path.closeSubpath()
        return path
    }

    var path: CGMutablePath {
        let vertex: [CGPoint] = [CGPoint(x: _boundBox.minX, y: _boundBox.minY),
                                 CGPoint(x: _boundBox.minX, y: _boundBox.maxY),
                                 CGPoint(x: _boundBox.maxX, y: _boundBox.maxY),
                                 CGPoint(x: _boundBox.maxX, y: _boundBox.minY)]
        return drawPath(vertex: vertex)
    }

    func shrink(by diameterChange: CGFloat) -> RoundedRect {
        let shortEdgeLength = min(_boundBox.width, _boundBox.height)
        let horizontalShift = diameterChange * (shortEdgeLength - _nodePos)/max(_boundBox.width, _boundBox.height)
        let newNodePos = max(0, min(shortEdgeLength/2 - diameterChange, _nodePos+horizontalShift - diameterChange))
        let newAnkorPos = max(0, (_ankorPos+0.55 * diameterChange+0.31 * horizontalShift) - diameterChange)
        var newBoundBox = _boundBox
        newBoundBox.origin.x += diameterChange
        newBoundBox.origin.y += diameterChange
        newBoundBox.size.width -= 2 * diameterChange
        newBoundBox.size.height -= 2 * diameterChange
        return RoundedRect(rect: newBoundBox, nodePos: newNodePos, ankorPos: newAnkorPos)
    }

    func bezierLength(t: CGFloat) -> CGFloat {
        guard _nodePos > 0 else { return 0 }
        let alpha = _ankorPos/_nodePos

        var length = pow(t, 2) * (-1 - 2 * alpha+9 * pow(alpha, 2)) - 5 * t * alpha * (1 - alpha)
        length *= 0.3 * (-1+2 * alpha+pow(alpha, 2))
        length += pow(1 - alpha, 2) * (1 - 4 * alpha+5 * pow(alpha, 2))
        length *= pow(t/(1 - alpha), 3)
        length += 3 * t * ((1 - alpha)+t * (2 * alpha - 1))

        return length * _nodePos
    }

    struct OrientedPoint {
        var name: String
        var position: CGPoint
        var direction: CGFloat
    }

    func arcPoints(lambdas: [CGFloat]) -> [OrientedPoint] {
        return arcPoints(lambdas: lambdas.map { ChineseCalendar.NamedPosition(name: "", pos: Double($0)) })
    }

    func arcPoints<T: NamedPoint>(lambdas: [T]) -> [OrientedPoint] {
        let arcLength = bezierLength(t: 0.5) * 2
        let innerWidth = _boundBox.width - 2 * _nodePos
        let innerHeight = _boundBox.height - 2 * _nodePos
        let totalLength = 2 * (innerWidth+innerHeight)+4 * arcLength

        func bezierNorm(l: CGFloat) -> (CGPoint, CGFloat) {
            var t: CGFloat = 0.0
            var otherSide = false
            var effectiveL = l
            if effectiveL > 0.5 {
                effectiveL = 1.0 - effectiveL
                otherSide = true
            }

            let stepSize: CGFloat = 0.1
            var currL: CGFloat = 0.0
            var prevL: CGFloat = -stepSize
            while currL < effectiveL * arcLength {
                prevL = currL
                t += stepSize
                if t > 0.5 {
                    t = 0.5
                }
                currL = bezierLength(t: t)
            }
            t -= (currL - effectiveL * arcLength)/(currL - prevL) * stepSize
            if otherSide {
                t = 1.0 - t
            }
            let alpha = _ankorPos/_nodePos
            let xt = pow(t, 3)+3 * alpha * (1 - t) * pow(t, 2)
            let yt = pow(1 - t, 3)+3 * alpha * t * pow(1 - t, 2)
            let dxt = 3 * (1 - alpha) * pow(1 - t, 2)+6 * alpha * (1 - t) * t
            let dyt = 3 * (1 - alpha) * pow(t, 2)+6 * alpha * (1 - t) * t
            let angle: CGFloat = atan2(dyt, dxt)
            let midPoint = CGPoint(x: xt * _nodePos, y: yt * _nodePos)
            return (midPoint, angle)
        }

        var firstLine = [(CGFloat, Int)](), secondLine = [(CGFloat, Int)](), thirdLine = [(CGFloat, Int)](), fourthLine = [(CGFloat, Int)](), fifthLine = [(CGFloat, Int)]()
        var firstArc = [(CGFloat, Int)](), secondArc = [(CGFloat, Int)](), thirdArc = [(CGFloat, Int)](), fourthArc = [(CGFloat, Int)]()

        var i = 0
        for lambdaPoint in lambdas {
            let lambda = lambdaPoint.pos
            switch lambda * totalLength {
            case 0.0..<innerWidth/2:
                firstLine.append((lambda * totalLength, i))
            case (innerWidth/2)..<(innerWidth/2+arcLength):
                firstArc.append(((lambda * totalLength - innerWidth/2)/arcLength, i))
            case (innerWidth/2+arcLength)..<(innerWidth/2+arcLength+innerHeight):
                secondLine.append((lambda * totalLength - innerWidth/2 - arcLength, i))
            case (innerWidth/2+arcLength+innerHeight)..<(innerWidth/2+2 * arcLength+innerHeight):
                secondArc.append(((lambda * totalLength - (innerWidth/2+arcLength+innerHeight))/arcLength, i))
            case (innerWidth/2+2 * arcLength+innerHeight)..<(innerWidth * 1.5+2 * arcLength+innerHeight):
                thirdLine.append((lambda * totalLength - (innerWidth/2+2 * arcLength+innerHeight), i))
            case (innerWidth * 1.5+2 * arcLength+innerHeight)..<(innerWidth * 1.5+3 * arcLength+innerHeight):
                thirdArc.append(((lambda * totalLength - (innerWidth * 1.5+2 * arcLength+innerHeight))/arcLength, i))
            case (innerWidth * 1.5+3 * arcLength+innerHeight)..<(innerWidth * 1.5+3 * arcLength+2 * innerHeight):
                fourthLine.append((lambda * totalLength - (innerWidth * 1.5+3 * arcLength+innerHeight), i))
            case (innerWidth * 1.5+3 * arcLength+2 * innerHeight)..<(innerWidth * 1.5+4 * arcLength+2 * innerHeight):
                fourthArc.append(((lambda * totalLength - (innerWidth * 1.5+3 * arcLength+2 * innerHeight))/arcLength, i))
            case (totalLength - innerWidth/2) ... totalLength:
                fifthLine.append((lambda * totalLength - (totalLength - innerWidth/2), i))
            default:
                return []
            }
            i += 1
        }

        var points = [(OrientedPoint, Int)]()

        for (lambda, i) in firstLine {
            let start = CGPoint(x: _boundBox.midX+lambda, y: _boundBox.maxY)
            let normAngle: CGFloat = 0
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in firstArc {
            var (start, normAngle) = bezierNorm(l: lambda)
            start = CGPoint(x: _boundBox.maxX - start.y, y: _boundBox.maxY - start.x)
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in secondLine {
            let start = CGPoint(x: _boundBox.maxX, y: _boundBox.maxY - _nodePos - lambda)
            let normAngle = CGFloat.pi/2
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in secondArc {
            var (start, normAngle) = bezierNorm(l: lambda)
            start = CGPoint(x: _boundBox.maxX - start.x, y: _boundBox.minY+start.y)
            normAngle += CGFloat.pi/2
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in thirdLine {
            let start = CGPoint(x: _boundBox.maxX - _nodePos - lambda, y: _boundBox.minY)
            let normAngle = CGFloat.pi
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in thirdArc {
            var (start, normAngle) = bezierNorm(l: lambda)
            normAngle += CGFloat.pi
            start = CGPoint(x: _boundBox.minX+start.y, y: _boundBox.minY+start.x)
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in fourthLine {
            let start = CGPoint(x: _boundBox.minX, y: _boundBox.minY+_nodePos+lambda)
            let normAngle = CGFloat.pi * 3/2
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in fourthArc {
            var (start, normAngle) = bezierNorm(l: lambda)
            normAngle += CGFloat.pi * 3/2
            start = CGPoint(x: _boundBox.minX+start.x, y: _boundBox.maxY - start.y)
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        for (lambda, i) in fifthLine {
            let start = CGPoint(x: _boundBox.minX+_nodePos+lambda, y: _boundBox.maxY)
            let normAngle: CGFloat = 0
            points.append((OrientedPoint(name: lambdas[i].name, position: start, direction: normAngle), i))
        }

        return points.sorted { $0.1 < $1.1 }.map { $0.0 }
    }

    func arcPosition(lambdas: [CGFloat], width: CGFloat) -> CGPath {
        let center = CGPoint(x: _boundBox.midX, y: _boundBox.midY)
        func getEnd(start: CGPoint, center: CGPoint, width: CGFloat) -> CGPoint {
            var direction = start - center
            direction /= sqrt(pow(direction.x, 2)+pow(direction.y, 2))
            let end = start - direction * width
            return end
        }
        let points = arcPoints(lambdas: lambdas)
        let path = CGMutablePath()
        for start in points {
            let end = getEnd(start: start.position, center: center, width: width)
            if end.x.isFinite && end.y.isFinite {
                path.move(to: start.position)
                path.addLine(to: end)
            }
        }

        return path
    }
}
