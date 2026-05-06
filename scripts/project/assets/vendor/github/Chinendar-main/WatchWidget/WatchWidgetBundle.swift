//
//  WatchWidgetBundle.swift
//  WatchWidgetExtension
//
//  Created by Leo Liu on 5/11/23.
//

import SwiftUI

@main
struct WatchWidgetBundle: WidgetBundle {

    var body: some Widget {
        OpenAppButton()
        LineWidget()
        CircularWidget()
        CurveWidget()
        RectWidget()
        DateCardWidget()
    }
}
