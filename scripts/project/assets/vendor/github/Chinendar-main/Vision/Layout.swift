//
//  Layout.swift
//  Chinendar
//
//  Created by Leo Liu on 11/12/23.
//

import SwiftUI

typealias WatchLayout = ExtraLayout<BaseLayout>

struct ExtraLayout<Base>: LayoutExpressible, Equatable, Codable where Base: LayoutExpressible, Base: Equatable, Base: Codable {
    var baseLayout = Base()
    var statusBar = StatusBar()

    var textFont: UIFont {
        UIFont.systemFont(ofSize: UIFont.systemFontSize, weight: .regular)
    }
    var centerFont: UIFont {
        UIFont(name: "SourceHanSansKR-Heavy", size: UIFont.systemFontSize)!
    }

    private enum CodingKeys: String, CodingKey {
        case baseLayout, statusBar
    }

    init() {}

    init(from decoder: Decoder) throws {
        self.init()
        let container = try decoder.container(keyedBy: CodingKeys.self)

        baseLayout = try container.decode(Base.self, forKey: .baseLayout)
        statusBar = try container.decode(StatusBar.self, forKey: .statusBar)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        try container.encode(baseLayout, forKey: .baseLayout)
        try container.encode(statusBar, forKey: .statusBar)
    }
}

struct WatchSetting: Equatable {
    enum Selection: String, CaseIterable {
        case datetime, location, configs, reminders, ringColor, decoration, markColor, layout, themes
    }
    enum TabSelection: String, CaseIterable {
        case spaceTime, design, documentation
    }

    var displayTime: Date?
    var vertical = true
    var settingIsOpen = false
    var timeDisplay = ""
    var selectionSpaceTime: Selection? = .datetime
    var selectionDesign: Selection? = .ringColor
    var tabSelection: TabSelection = .spaceTime
    var effectiveTime: Date {
        displayTime ?? .now
    }
    var path = NavigationPath()
}
