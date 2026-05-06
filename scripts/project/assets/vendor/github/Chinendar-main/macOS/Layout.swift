//
//  Layout.swift
//  Chinendar
//
//  Created by Leo Liu on 9/23/21.
//

import SwiftUI

typealias WatchLayout = ExtraLayout<BaseLayout>

struct ExtraLayout<Base>: LayoutExpressible where Base: LayoutExpressible {
    var baseLayout = Base()
    var statusBar = StatusBar()

    private var _textFont: String = NSFont.systemFont(ofSize: NSFont.systemFontSize).fontName
    private var _centerFont: String = NSFont.systemFont(ofSize: NSFont.systemFontSize, weight: .heavy).fontName
    var textFont: NSFont {
        get {
            NSFont(name: _textFont, size: NSFont.systemFontSize) ?? NSFont.systemFont(ofSize: NSFont.systemFontSize)
        } set {
            _textFont = newValue.fontName
        }
    }
    var centerFont: NSFont {
        get {
            NSFont(name: _centerFont, size: NSFont.systemFontSize) ?? NSFont.systemFont(ofSize: NSFont.systemFontSize, weight: .heavy)
        } set {
            _centerFont = newValue.fontName
        }
    }

    private enum CodingKeys: String, CodingKey {
        case baseLayout, statusBar, textFont, centerFont
    }

    init() {}

    init(from decoder: Decoder) throws {
        self.init()
        let container = try decoder.container(keyedBy: CodingKeys.self)

        baseLayout = try container.decode(Base.self, forKey: .baseLayout)
        statusBar = try container.decode(StatusBar.self, forKey: .statusBar)
        _textFont ?= try container.decodeIfPresent(String.self, forKey: .textFont)
        _centerFont ?= try container.decodeIfPresent(String.self, forKey: .centerFont)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        try container.encode(baseLayout, forKey: .baseLayout)
        try container.encode(statusBar, forKey: .statusBar)
        try container.encode(_textFont, forKey: .textFont)
        try container.encode(_centerFont, forKey: .centerFont)
    }
}

struct WatchSetting: Equatable {
    enum Selection: String, CaseIterable {
        case datetime, location, configs, reminders, ringColor, decoration, markColor, layout, themes, documentation
    }

    var settingIsOpen = false
    var position: CGRect = .zero
    var selection: Selection?
    var previousSelection: Selection? = .datetime
    var displayTime: Date?
    var effectiveTime: Date {
        displayTime ?? .now
    }
    var path = NavigationPath()
}
