//
//  Layout.swift
//  Chinendar
//
//  Created by Leo Liu on 9/23/21.
//

import SwiftUI
import SwiftData

typealias WatchLayout = ExtraLayout<BaseLayout>

struct ExtraLayout<Base>: LayoutExpressible, Equatable, Codable where Base: LayoutExpressible, Base: Equatable, Base: Codable {
    var baseLayout = Base()

    var textFont: UIFont {
        UIFont.systemFont(ofSize: UIFont.systemFontSize, weight: .regular)
    }
    var centerFont: UIFont {
        UIFont(name: "SourceHanSansKR-Heavy", size: UIFont.systemFontSize)!
    }

    private enum CodingKeys: String, CodingKey {
        case baseLayout
    }

    init() {}

    init(from decoder: Decoder) throws {
        self.init()
        let container = try decoder.container(keyedBy: CodingKeys.self)

        baseLayout = try container.decode(Base.self, forKey: .baseLayout)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)

        try container.encode(baseLayout, forKey: .baseLayout)
    }
}

struct WatchSetting: Equatable {
    enum Selection: String, CaseIterable {
        case datetime, location, configs, reminders, ringColor, decoration, markColor, layout, themes, documentation
    }

    var displayTime: Date?
    var presentSetting = false
    var vertical = true
    var effectiveTime: Date {
        displayTime ?? .now
    }
    var path = NavigationPath()
}
