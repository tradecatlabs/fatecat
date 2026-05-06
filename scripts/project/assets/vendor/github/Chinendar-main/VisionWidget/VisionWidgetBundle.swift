//
//  VisionWidgetBundle.swift
//  VisionWidget
//
//  Created by Leo Liu on 6/10/25.
//

import SwiftUI
import WidgetKit

@main
struct MacWidgetBundle: WidgetBundle {

    var body: some Widget {
        DualWatchWidget()
        FullWatchWidget()
    }
}
