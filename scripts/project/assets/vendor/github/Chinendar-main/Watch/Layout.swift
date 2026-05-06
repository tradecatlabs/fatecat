//
//  Layout.swift
//  Chinendar
//
//  Created by Leo Liu on 5/11/23.
//

import SwiftUI

typealias WatchLayout = ExtraLayout<BaseLayout>

struct ExtraLayout<Base>: LayoutExpressible, Equatable, Codable where Base: LayoutExpressible, Base: Equatable, Base: Codable {
    var baseLayout = Base()
    var dualWatch = false
    var syncFromPhone = true

    var textFont: UIFont {
        UIFont.systemFont(ofSize: 14, weight: .regular)
    }
    var centerFont: UIFont {
        UIFont(name: "SourceHanSansKR-Heavy", size: 14)!
    }

    private enum CodingKeys: String, CodingKey {
        case baseLayout, dualWatch, syncFromPhone
    }

    init() {}

    init(from decoder: Decoder) throws {
        self.init()
        let container = try decoder.container(keyedBy: CodingKeys.self)

        baseLayout = try container.decode(Base.self, forKey: .baseLayout)
        dualWatch ?= try container.decodeIfPresent(Bool.self, forKey: .dualWatch)
        syncFromPhone ?= try container.decodeIfPresent(Bool.self, forKey: .syncFromPhone)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        try container.encode(baseLayout, forKey: .baseLayout)
        try container.encode(dualWatch, forKey: .dualWatch)
        try container.encode(syncFromPhone, forKey: .syncFromPhone)
    }
}

struct WatchSetting: Equatable {
    enum TimeadjSelection {
        case gregorian, chinese
    }
    enum Selection: String, CaseIterable {
        case datetime, themes, configs, reminders
    }

    var size: CGSize = .zero
    var displayTime: Date?
    var effectiveTime: Date {
        displayTime ?? .now
    }
    var selection: TimeadjSelection = .gregorian
    var path = NavigationPath()
}
