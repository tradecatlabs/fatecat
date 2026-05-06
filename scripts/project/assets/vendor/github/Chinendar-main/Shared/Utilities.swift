//
//  Utilities.swift
//  Chinendar
//
//  Created by Leo Liu on 4/29/23.
//

import Foundation

func + (lhs: CGPoint, rhs: CGPoint) -> CGPoint {
    return CGPoint(x: lhs.x + rhs.x, y: lhs.y + rhs.y)
}

func - (lhs: CGPoint, rhs: CGPoint) -> CGPoint {
    return CGPoint(x: lhs.x - rhs.x, y: lhs.y - rhs.y)
}

func * (lhs: CGPoint, rhs: CGFloat) -> CGPoint {
    return CGPoint(x: lhs.x * rhs, y: lhs.y * rhs)
}

func / (lhs: CGPoint, rhs: CGFloat) -> CGPoint {
    return CGPoint(x: lhs.x / rhs, y: lhs.y / rhs)
}

func /= ( lhs: inout CGPoint, rhs: CGFloat) {
    lhs.x /= rhs
    lhs.y /= rhs
}

infix operator %%: MultiplicationPrecedence
infix operator /%: MultiplicationPrecedence
infix operator ?= : AssignmentPrecedence

extension BinaryInteger {
    static func %% (_ left: Self, _ right: Self) -> Self {
        let mod = left % right
        return mod >= 0 ? mod : mod + right
    }
}

extension FloatingPoint {
    static func %% (_ left: Self, _ right: Self) -> Self {
        let mod = left.truncatingRemainder(dividingBy: right)
        return mod >= 0 ? mod : mod + right
    }
}

func ?= <T>(left: inout T, right: T?) {
  if let right {
    left = right
  }
}

func ?= <T>(left: inout T?, right: T?) {
  if let right {
    left = right
  }
}

extension BinaryInteger {
    static func /% (_ left: Self, _ right: Self) -> Self {
        if left < 0 {
            return (left - right + 1) / right
        } else {
            return left / right
        }
    }
}

func /% <F: BinaryFloatingPoint, I: BinaryInteger>(lhs: F, rhs: I) -> F {
    return floor(lhs / F(rhs))
}

extension Array {
    func insertionIndex(of value: Element, comparison: (Element, Element) -> Bool) -> Index {
        var slice: SubSequence = self[...]

        while !slice.isEmpty {
            let middle = slice.index(slice.startIndex, offsetBy: slice.count / 2)
            if comparison(value, slice[middle]) {
                slice = slice[..<middle]
            } else {
                slice = slice[index(after: middle)...]
            }
        }
        return slice.startIndex
    }

    func slice(from: Int = 0, to: Int? = nil, step: Int = 1) -> Self {
        var sliced = Self()
        var i = from
        let limit = to ?? count
        while i < limit {
            sliced.append(self[i])
            i += step
        }
        return sliced
    }
}

extension Array where Element: Hashable {
    func find(indices: IndexSet) -> Set<Element> {
        var container = Set<Element>()
        for index in indices {
            container.insert(self[index])
        }
        return container
    }
}

protocol NamedPoint: Sendable, Equatable, Codable {
    var name: String { get }
    var pos: Double { get }
}

protocol NamedArray: Sendable, Equatable, Codable {
    func getValues<S>(_ properties: [KeyPath<Self, S>]) -> [S]
}

extension NamedArray {
    func getValues<S>(_ properties: [KeyPath<Self, S>]) -> [S] {
        properties.map { self[keyPath: $0] }
    }
}

struct Planets<S>: NamedArray where S: Sendable, S: Equatable, S: Codable {
    var moon: S
    var mercury: S
    var venus: S
    var mars: S
    var jupiter: S
    var saturn: S
}

struct Solar<S>: NamedArray where S: Sendable, S: Equatable, S: Codable {
    var midnight: S
    var sunrise: S
    var noon: S
    var sunset: S
}

struct Lunar<S>: NamedArray where S: Sendable, S: Equatable, S: Codable {
    var moonrise: S
    var highMoon: S
    var moonset: S
}

struct MonthTerm<S>: NamedArray where S: Sendable, S: Equatable, S: Codable {
    var fullMoon: S
    var newMoon: S
    var oddSolarTerm: S
    var evenSolarTerm: S
}
