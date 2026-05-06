//
//  DateTimeAdjust.swift
//  Chinendar
//
//  Created by Leo Liu on 6/26/23.
//

import SwiftUI
import Observation

struct DateTimeAdjust: View {
    @Environment(ViewModel.self) var viewModel
    @State fileprivate var dateManager = DateManager()

    var body: some View {
        ZStack {
            switch viewModel.settings.selection {
            case .gregorian:
                DateTimePicker(time: dateManager.binding(\.time))
                .tag(WatchSetting.TimeadjSelection.gregorian)
            case .chinese:
                ChinendarPickerPanel(chineseCalendar: dateManager.binding(\.chineseCalendar))
                .tag(WatchSetting.TimeadjSelection.chinese)
            }
        }
        .tint(.accentColor)
        .tabViewStyle(.page)
        .toolbar {
            ToolbarItemGroup(placement: .bottomBar) {
                switchButton
                resetButton
            }
        }
        .navigationTitle("DATETIME_PICKER")
        .onAppear {
            dateManager.setup(viewModel: viewModel)
        }
    }

    var resetButton: some View {
        Button {
            withAnimation {
                dateManager.isCurrent = true
            }
        } label: {
            Image(systemName: "clock.arrow.circlepath")
        }
        .disabled(dateManager.isCurrent)
    }

    var switchButton: some View {
        Button {
            withAnimation {
                switch viewModel.settings.selection {
                case .gregorian:
                    viewModel.settings.selection = .chinese
                case .chinese:
                    viewModel.settings.selection = .gregorian
                }
            }
        } label: {
            switch viewModel.settings.selection {
            case .gregorian:
                Image(.appChinendar)
                    .font(.custom("larger", size: 22, relativeTo: .body))
                    .symbolRenderingMode(.hierarchical)
            case .chinese:
                Image(systemName: "calendar.badge.clock")
            }
        }
    }
}

private struct DateTimePicker: View {
    @Binding var time: Date

    var body: some View {
        GeometryReader { geometry in
            VStack(spacing: geometry.size.height * 0.05) {
                DatePicker(selection: $time, in: ChineseCalendar.start...ChineseCalendar.end, displayedComponents: [.date]) {
                    Text("DATE")
                }
                .minimumScaleFactor(0.75)
                .frame(height: geometry.size.height * 0.45)
                DatePicker(selection: $time, in: ChineseCalendar.start...ChineseCalendar.end, displayedComponents: [.hourAndMinute]) {
                    Text("TIME")
                }
                .minimumScaleFactor(0.75)
                .frame(height: geometry.size.height * 0.45)
            }
        }
    }
}

@MainActor
@Observable private final class DateManager: Bindable {
    var viewModel: ViewModel?

    func setup(viewModel: ViewModel) {
        self.viewModel = viewModel
    }

    var chineseCalendar: ChineseCalendar {
        get {
            viewModel?.chineseCalendar ?? .init()
        } set {
            viewModel?.settings.displayTime = newValue.time
        }
    }

    var time: Date {
        get {
            viewModel?.settings.displayTime ?? viewModel?.chineseCalendar.time ?? .now
        } set {
            if abs(newValue.distance(to: .now)) > 14.4 {
                viewModel?.settings.displayTime = newValue
            }
        }
    }

    var isCurrent: Bool {
        get {
            return viewModel?.settings.displayTime == nil
        } set {
            if newValue {
                viewModel?.settings.displayTime = nil
            } else {
                viewModel?.settings.displayTime = viewModel?.chineseCalendar.time
            }
        }
    }
}

#Preview("Datetime Adjust", traits: .modifier(SampleData())) {
    NavigationStack {
        DateTimeAdjust()
    }
}
