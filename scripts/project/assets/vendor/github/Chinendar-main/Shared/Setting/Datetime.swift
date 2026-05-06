//
//  Datetime.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI
import Observation

struct Datetime: View {
    @State fileprivate var dateManager = DateManager()
    @State fileprivate var reverseCount = false
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            Section(header: Text("CAL_METHOD")) {
                HStack {
                    Picker("LEAP_M_METHOD", selection: dateManager.binding(\.globalMonth)) {
                        ForEach([true, false], id: \.self) { globalMonth in
                            if globalMonth {
                                Text("LEAP_M_BY_MOMENT")
                            } else {
                                Text("LEAP_M_BY_DAY")
                            }
                        }
                    }
                }

                HStack {
                    Picker("TIME_KEEPING", selection: dateManager.binding(\.apparentTime)) {
                        let choice = if viewModel.location != nil {
                            [true, false]
                        } else {
                            [false]
                        }
                        ForEach(choice, id: \.self) { apparentTime in
                            if apparentTime {
                                Text("APPARENT_TIME")
                            } else {
                                Text("STD_TIME")
                            }
                        }
                    }
                }

                HStack {
                    Picker("HOUR_FORMAT", selection: dateManager.binding(\.largeHour)) {
                        ForEach([true, false], id: \.self) { largeHour in
                            if largeHour {
                                Text("LARGE_HOUR_FORMAT")
                            } else {
                                Text("SMALL_HOUR_FORMAT")
                            }
                        }
                    }
                }
            }
            .pickerStyle(.menu)

            Section(header: Text("DATETIME:\(dateManager.time.formatted(date: .abbreviated, time: .shortened))")) {
                Toggle("NOW", isOn: dateManager.binding(\.isCurrent))
                DatePicker("DATETIME_PICKER", selection: dateManager.binding(\.time), in: ChineseCalendar.start...ChineseCalendar.end, displayedComponents: [.date, .hourAndMinute])
                    .environment(\.timeZone, dateManager.timezone)
            }

            Section(header: Text("CHINENDAR_DATETIME:")) {
                HStack {
                    Text("DATE")
                        .lineLimit(1)
                    ChinendarDatePicker(chineseCalendar: dateManager.binding(\.chineseCalendar))
                        .layoutPriority(1)
                    Spacer(minLength: 0)
                        .frame(idealWidth: 10, maxWidth: 20)
                    Text("TIME")
                        .lineLimit(1)
                    ChinendarTimePicker(chineseCalendar: dateManager.binding(\.chineseCalendar))
                        .layoutPriority(1)
                }
                .buttonStyle(.bordered)
                .frame(maxWidth: .infinity, alignment: .trailing)
            }

            let timezoneTitle = if let desp = dateManager.timezone.localizedName(for: .standard, locale: Locale.current) {
                Text("TIMEZONE:\(desp)")
            } else {
                Text("TIMEZONE")
            }
            Section(header: timezoneTitle) {
                Toggle("NOW_TIMEZONE", isOn: dateManager.binding(\.isTimezoneCurrent))
                timezonePicker
            }
        }
        .formStyle(.grouped)
        .task {
            dateManager.setup(viewModel: viewModel)
        }
        .navigationTitle("DATETIME")
#if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            Button {
                viewModel.settings.presentSetting = false
            } label: {
                Label("DONE", systemImage: "checkmark")
            }
            .fontWeight(.semibold)
        }
#endif
    }

    @ViewBuilder private var timezonePicker: some View {
        HStack(spacing: 10) {
            Picker("TZ_CONTIMENT", selection: dateManager.binding(\.timeZoneSelection.primary)) {
                ForEach(dateManager.timeZoneSelection.timeZones.nextLevel.map { $0.nodeName }, id: \.self) { tz in
                    Text(tz.replacingOccurrences(of: "_", with: " "))

                }
            }
            .lineLimit(1)
            .animation(.default, value: dateManager.timeZoneSelection)
            if let tzList = dateManager.timeZoneSelection.timeZones[dateManager.timeZoneSelection.primary], tzList.count > 0 {
#if os(macOS) || os(visionOS)
                Divider()
#endif
                Picker("TZ_REGION", selection: dateManager.binding(\.timeZoneSelection.secondary)) {
                    ForEach(tzList.nextLevel.map { $0.nodeName }, id: \.self) { tz in
                        Text(tz.replacingOccurrences(of: "_", with: " "))
                    }
                }
                .lineLimit(1)
                .animation(.default, value: dateManager.timeZoneSelection)
            }
            if let tzList = dateManager.timeZoneSelection.timeZones[dateManager.timeZoneSelection.primary], let tzList2 = tzList[dateManager.timeZoneSelection.secondary], tzList2.count > 0 {
#if os(macOS) || os(visionOS)
                Divider()
#endif
                Picker("TZ_LOCAL", selection: dateManager.binding(\.timeZoneSelection.tertiary)) {
                    ForEach(tzList2.nextLevel.map { $0.nodeName }, id: \.self) { tz in
                        Text(tz.replacingOccurrences(of: "_", with: " "))
                    }
                }
                .lineLimit(1)
                .animation(.default, value: dateManager.timeZoneSelection)
            }
        }
        .minimumScaleFactor(0.5)
#if os(iOS)
        .pickerStyle(.wheel)
        .frame(maxHeight: 125)
#else
        .pickerStyle(.menu)
#endif
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

    var timeZoneSelection: TimeZoneSelection {
        get {
            TimeZoneSelection(timezone: timezone)
        } set {
            if let tz = newValue.timezone {
                viewModel?.config.timezone = tz
            }
        }
    }

    var time: Date {
        get {
            viewModel?.settings.displayTime ?? viewModel?.chineseCalendar.time ?? .now
        } set {
            viewModel?.settings.displayTime = newValue
        }
    }

    var timezone: TimeZone {
        viewModel?.config.timezone ?? viewModel?.chineseCalendar.calendar.timeZone ?? Calendar.current.timeZone
    }

    var isCurrent: Bool {
        get {
            viewModel?.settings.displayTime == nil
        } set {
            if newValue {
                viewModel?.settings.displayTime = nil
            } else {
                viewModel?.settings.displayTime = viewModel?.chineseCalendar.time
            }
        }
    }

    var isTimezoneCurrent: Bool {
        get {
            viewModel?.config.timezone == nil
        } set {
            if newValue {
                viewModel?.config.timezone = nil
            } else {
                viewModel?.config.timezone = Calendar.current.timeZone
            }
        }
    }

    var globalMonth: Bool {
        get {
            viewModel?.config.globalMonth ?? false
        } set {
            viewModel?.config.globalMonth = newValue
        }
    }

    var apparentTime: Bool {
        get {
            viewModel?.config.apparentTime ?? false
        } set {
            viewModel?.config.apparentTime = newValue
        }
    }

    var largeHour: Bool {
        get {
            viewModel?.config.largeHour ?? false
        } set {
            viewModel?.config.largeHour = newValue
        }
    }
}

final class DataTree: CustomStringConvertible {
    var nodeName: String
    private var offsprings: [DataTree]
    private var registry: [String: Int]

    init(name: String) {
        nodeName = name
        offsprings = []
        registry = [:]
    }

    var nextLevel: [DataTree] {
        offsprings
    }

    func add(element: String) -> DataTree {
        let data: DataTree
        if let index = registry[element] {
            data = offsprings[index]
        } else {
            registry[element] = offsprings.count
            offsprings.append(DataTree(name: element))
            data = offsprings.last!
        }
        return data
    }

    var count: Int {
        offsprings.count
    }

    subscript(element: String) -> DataTree? {
        if let index = registry[element] {
            return offsprings[index]
        } else {
            return nil
        }
    }

    var description: String {
        var string: String
        if offsprings.count > 0 {
            string = "{\(nodeName): "
        } else {
            string = "\(nodeName)"
        }
        for offspring in offsprings {
            string += offspring.description
        }
        if offsprings.count > 0 {
            string += "}, "
        } else {
            string += ","
        }
        return string
    }
}

private struct TimeZoneSelection: Equatable {
    static func == (lhs: TimeZoneSelection, rhs: TimeZoneSelection) -> Bool {
        lhs.primary == rhs.primary && lhs.secondary == rhs.secondary && lhs.tertiary == rhs.tertiary
    }

    let timeZones = populateTimezones()
    var primary: String {
        didSet {
            if let next = timeZones[primary]?.nextLevel.first?.nodeName {
                secondary = next
            } else {
                secondary = ""
            }
        }
    }
    var secondary: String {
        didSet {
            if let next = timeZones[primary]?[secondary]?.nextLevel.first?.nodeName {
                tertiary = next
            } else {
                tertiary = ""
            }
        }
    }
    var tertiary: String

    init(timezone: TimeZone) {
        let components = timezone.identifier.split(separator: "/")
        primary = if components.count > 0 { String(components[0]) } else { "" }
        secondary = if components.count > 1 { String(components[1]) } else { "" }
        tertiary = if components.count > 2 { String(components[2]) } else { "" }
    }

    var timezone: TimeZone? {
        var identifier = primary
        if secondary != "" {
            identifier += "/" + secondary
        }
        if tertiary != "" {
            identifier += "/" + tertiary
        }
        return TimeZone(identifier: identifier)
    }
}

private func populateTimezones() -> DataTree {
    let root = DataTree(name: "Root")
    let allTimezones = TimeZone.knownTimeZoneIdentifiers
    for timezone in allTimezones {
        let components = timezone.split(separator: "/")
        var currentNode: DataTree? = root
        for component in components {
            currentNode = currentNode?.add(element: String(component))
        }
    }
    return root
}

#Preview("Datetime", traits: .modifier(SampleData())) {
    NavigationStack {
        Datetime()
    }
}
