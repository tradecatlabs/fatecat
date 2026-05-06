//
//  DatePicker.swift
//  Chinendar
//
//  Created by Leo Liu on 9/21/24.
//

import SwiftUI

@MainActor
private final class DatePickerModel: Bindable {
    @Binding var chineseCalendar: ChineseCalendar

    init(chineseCalendar: Binding<ChineseCalendar>) {
        self._chineseCalendar = chineseCalendar
    }

    var chineseDate: ChineseCalendar.ChineseDate {
        get {
            chineseCalendar.chineseDate
        } set {
            if let newDate = chineseCalendar.find(chineseDate: newValue) {
                chineseCalendar.update(time: newDate.time)
            }
        }
    }

    var chinendarMonth: Int {
        get {
            chineseDate.monthIndex(in: chineseCalendar)
        } set {
            chineseDate.update(monthIndex: newValue, in: chineseCalendar)
        }
    }

    func nextMonth() {
        if let newDate = chineseCalendar.nextMonth() {
            chineseCalendar.update(time: newDate)
        }
    }

    func previousMonth() {
        if let newDate = chineseCalendar.previousMonth() {
            chineseCalendar.update(time: newDate)
        }
    }

    func nextYear() {
        if let newDate = chineseCalendar.nextYear() {
            chineseCalendar.update(time: newDate)
        }
    }

    func previousYear() {
        if let newDate = chineseCalendar.previousYear() {
            chineseCalendar.update(time: newDate)
        }
    }
}

@MainActor
private final class TimePickerModel: Bindable {
    @Binding var chineseCalendar: ChineseCalendar

    init(chineseCalendar: Binding<ChineseCalendar>) {
        self._chineseCalendar = chineseCalendar
    }

    var largeHour: Bool {
        chineseCalendar.largeHour
    }
    var maxQuarterMajor: Int {
        chineseCalendar.maxQuarterMajor
    }
    var maxQuarterMinor: Int {
        chineseCalendar.maxQuarterMinor
    }

    var hour: Int {
        get {
            chineseCalendar.hour
        } set {
            updateSubquarters(hour: newValue)
        }
    }
    var quarterMajor: Int {
        get {
            chineseCalendar.quarterMajor
        } set {
            updateSubquarters(quarterMajor: newValue)
        }
    }
    var quarterMinor: Int {
        get {
            chineseCalendar.quarterMinor
        } set {
            updateSubquarters(quarterMinor: newValue)
        }
    }

    func prevHour() {
        if largeHour {
            updateSubquarters(hour: hour - 2)
        } else {
            updateSubquarters(hour: hour - 1)
        }
    }
    func nextHour() {
        if largeHour {
            updateSubquarters(hour: hour + 2)
        } else {
            updateSubquarters(hour: hour + 1)
        }
    }
    func prevDay() {
        var newChineseCalendar = chineseCalendar
        newChineseCalendar.update(time: chineseCalendar.startOfDay - 1)
        var datetime = chineseCalendar.chineseDateTime
        datetime.date.month = newChineseCalendar.nominalMonth
        datetime.date.day = newChineseCalendar.day
        datetime.date.leap = newChineseCalendar.isLeapMonth
        if let newDate = newChineseCalendar.find(chineseDateTime: datetime) {
            chineseCalendar.update(time: newDate)
        }
    }
    func nextDay() {
        var newChineseCalendar = chineseCalendar
        newChineseCalendar.update(time: chineseCalendar.startOfNextDay + 1)
        var datetime = chineseCalendar.chineseDateTime
        datetime.date.month = newChineseCalendar.nominalMonth
        datetime.date.day = newChineseCalendar.day
        datetime.date.leap = newChineseCalendar.isLeapMonth
        if let newDate = newChineseCalendar.find(chineseDateTime: datetime) {
            chineseCalendar.update(time: newDate)
        }
    }

    private func updateSubquarters(hour: Int? = nil, quarterMajor: Int? = nil, quarterMinor: Int? = nil) {
        var time = chineseCalendar.chineseTime
        time.smallHour ?= hour
        time.quarter ?= quarterMajor
        time.subQuarter ?= quarterMinor
        if let newDate = chineseCalendar.find(chineseTime: time) {
            chineseCalendar.update(time: newDate)
        }
    }
}

#if os(watchOS)
struct ChinendarPickerPanel: View {
    private var dateModel: DatePickerModel
    private var timeModel: TimePickerModel

    init(chineseCalendar: Binding<ChineseCalendar>) {
        self.dateModel = DatePickerModel(chineseCalendar: chineseCalendar)
        self.timeModel = TimePickerModel(chineseCalendar: chineseCalendar)
    }

    var body: some View {
        GeometryReader { geometry in
            VStack(spacing: geometry.size.height * 0.05) {
                HStack(spacing: 3) {
                    Button {
                        dateModel.previousYear()
                    } label: {
                        Label("PREV_YEAR", systemImage: "chevron.backward.2")
                            .fontWeight(.bold)
                    }
                    .padding(.top)
                    Picker("MONTH", selection: dateModel.binding(\.chinendarMonth)) {
                        ForEach(1...dateModel.chineseCalendar.numberOfMonths, id: \.self) { monthIndex in
                            Text(dateModel.chineseCalendar.monthLabel(monthIndex: monthIndex))
                                .minimumScaleFactor(0.8)
                                .lineLimit(1)
                        }
                    }
                    .animation(.default, value: dateModel.chinendarMonth)
                    Picker("DAY", selection: dateModel.binding(\.chineseDate.day)) {
                        ForEach(1...dateModel.chineseCalendar.numberOfDaysInMonth, id: \.self) { day in
                            Text("\(ChineseCalendar.dayChineseLocalized[day-1])DAY")
                                .minimumScaleFactor(0.8)
                                .lineLimit(1)
                        }
                    }
                    .animation(.default, value: dateModel.chineseDate)
                    Button {
                        dateModel.nextYear()
                    } label: {
                        Label("NEXT_YEAR", systemImage: "chevron.forward.2")
                            .fontWeight(.bold)
                    }
                    .padding(.top)
                }
                .labelStyle(.iconOnly)
                .buttonStyle(.borderless)
                .buttonBorderShape(.capsule)
                .frame(height: geometry.size.height * 0.45)

                HStack(spacing: 3) {
                    Picker("CHINESE_HOUR", selection: timeModel.binding(\.hour)) {
                        ForEach(Array(stride(from: 0, to: 24, by: timeModel.largeHour ? 2 : 1)), id: \.self) { hour in
                            Text(timeModel.chineseCalendar.hourName(hour: hour))
                                .lineLimit(1)
                                .minimumScaleFactor(0.5)
                        }
                    }
                    .animation(.default, value: timeModel.hour)
                    Picker("QUARTER", selection: timeModel.binding(\.quarterMajor)) {
                        ForEach(0..<timeModel.maxQuarterMajor, id: \.self) { quarterIndex in
                            Text("\(ChineseCalendar.chineseNumbersLocalized[quarterIndex])QUARTER")
                                .lineLimit(1)
                                .minimumScaleFactor(0.5)
                        }
                    }
                    .animation(.default, value: timeModel.quarterMajor)
                    Picker("SUB_QUARTER", selection: timeModel.binding(\.quarterMinor)) {
                        ForEach(0..<timeModel.maxQuarterMinor, id: \.self) { subquarterIndex in
                            Text(ChineseCalendar.chineseNumbersLocalized[subquarterIndex])
                                .lineLimit(1)
                                .minimumScaleFactor(0.75)
                        }
                    }
                    .animation(.default, value: timeModel.quarterMinor)
                }
                .frame(height: geometry.size.height * 0.45)
            }
        }
    }
}

#Preview("Watch") {
    @Previewable @State var chineseCalendar = ChineseCalendar()
    ChinendarPickerPanel(chineseCalendar: $chineseCalendar)
}
#else
private struct DragablePicker<V: View>: View {
    @State private var dragOffset: CGFloat = 0
    @State private var size: CGSize = .zero
    @State private var dragTriggered: Int = 0
    let view: V
    let prevAction: () -> Void
    let nextAction: () -> Void

    init(@ViewBuilder view: () -> V, prevAction: @escaping () -> Void, nextAction: @escaping () -> Void) {
        self.view = view()
        self.prevAction = prevAction
        self.nextAction = nextAction
    }

    var body: some View {
        let dragGesture = DragGesture()
            .onChanged { value in
                dragOffset = value.translation.width
                if abs(value.translation.width) > size.width / 3 {
                    dragTriggered = value.translation.width > 0 ? 1 : -1
                } else {
                    withAnimation(.easeIn(duration: 0.2)) {
                        dragTriggered = 0
                    }
                }
            }
            .onEnded { value in
                if abs(value.translation.width) < size.width / 3 {
                    withAnimation(.bouncy) {
                        dragOffset = 0
                    }
                } else if value.translation.width > 0 {
                    dragOffset = -size.width
                    prevAction()
                    withAnimation(.easeOut) {
                        dragOffset = 0
                    }
                } else {
                    dragOffset = size.width
                    nextAction()
                    withAnimation(.easeOut) {
                        dragOffset = 0
                    }
                }
            }

        ZStack {
            HStack {
                Image(systemName: "chevron.backward")
                    .font(dragTriggered > 0 ? .largeTitle : .title3)
                    .opacity(max(0, min(1, dragOffset / (size.width + 1.0) * 2.0)))
                Spacer()
                Image(systemName: "chevron.forward")
                    .font(dragTriggered < 0 ? .largeTitle : .title3)
                    .opacity(max(0, min(1, -dragOffset / (size.width + 1.0) * 2.0)))
            }
#if os(iOS)
            .foregroundStyle(.blue)
#endif
            view
                .contentShape(.interaction, .containerRelative)
                .background(GeometryReader { geometry in
                    Color.clear
                        .onChange(of: geometry.size, initial: true) {
                            size = geometry.size
                        }
                })
                .offset(x: dragOffset, y: 0)
                .highPriorityGesture(dragGesture)
        }
    }
}

private struct ChinendarDatePickerPanel: View {
    private var model: DatePickerModel
    private let dateColumns = Array(repeating: GridItem(spacing: 0), count: 10)
    private let monthColumns = Array(repeating: GridItem(spacing: 0), count: 6)
    @State private var monthView = false
#if os(visionOS)
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 65
#elseif os(iOS)
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 50
#else
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 30
#endif

    init(chineseCalendar: Binding<ChineseCalendar>) {
        self.model = DatePickerModel(chineseCalendar: chineseCalendar)
    }

    var body: some View {
        VStack {
            HStack {
                Button {
                    withAnimation {
                        monthView.toggle()
                    }
                } label: {
                    HStack {
                        Text(model.chineseCalendar.monthLabel(monthIndex: model.chinendarMonth))
                            .fontWeight(.bold)
                            .lineLimit(1)
                        if monthView {
                            Image(systemName: "chevron.up")
                                .font(.footnote)
                        } else {
                            Image(systemName: "chevron.forward")
                                .font(.footnote)
                        }
                    }
                    .animation(.default, value: monthView)
                }
                .padding(.horizontal)
                .animation(.default, value: model.chinendarMonth)
                Spacer()
                if monthView {
                    Button {
                        withAnimation {
                            model.previousYear()
                        }
                    } label: {
                        Label("PREV_YEAR", systemImage: "chevron.backward")
                            .fontWeight(.bold)
                    }
                    Text("YEAR_ABV")
                    Button {
                        withAnimation {
                            model.nextYear()
                        }
                    } label: {
                        Label("NEXT_YEAR", systemImage: "chevron.forward")
                            .fontWeight(.bold)
                    }
                } else {
                    Button {
                        withAnimation {
                            model.previousMonth()
                        }
                    } label: {
                        Label("PREV_MONTH", systemImage: "chevron.backward")
                            .fontWeight(.bold)
                    }
                    Text("MONTH_ABV")
                    Button {
                        withAnimation {
                            model.nextMonth()
                        }
                    } label: {
                        Label("NEXT_MONTH", systemImage: "chevron.forward")
                            .fontWeight(.bold)
                    }
                }
            }
            .labelStyle(.iconOnly)

            Divider()
                .padding(5)

            if monthView {
                DragablePicker {
                    LazyVGrid(columns: monthColumns, spacing: 0) {
                        ForEach(1...model.chineseCalendar.numberOfMonths, id: \.self) { monthIndex in
                            let monthButton = Button {
                                withAnimation {
                                    model.chinendarMonth = monthIndex
                                }
                            } label: {
                                Text(model.chineseCalendar.monthLabel(monthIndex: monthIndex))
                                    .lineLimit(1)
                                    .fixedSize()
                            }
                                .buttonBorderShape(.capsule)
                                .frame(minWidth: cellSize * 1.7, minHeight: cellSize)
                            if monthIndex == model.chinendarMonth {
                                monthButton
#if os(visionOS)
                                    .buttonStyle(.automatic)
#else
                                    .buttonStyle(.bordered)
                                    .fontWeight(.bold)
                                    .tint(.blue)
#endif
                            } else {
                                monthButton
                                    .foregroundStyle(.primary)
                                    .buttonStyle(.borderless)
                            }
                        }
                    }
                    .animation(.default, value: model.chinendarMonth)
                } prevAction: {
                    model.previousYear()
                } nextAction: {
                    model.nextYear()
                }
            } else {
                DragablePicker {
                    LazyVGrid(columns: dateColumns, spacing: 0) {
                        let fullMoonDay = model.chineseCalendar.dayTicks.majorTicks.count { tick in
                            tick < (model.chineseCalendar.eventInMonth.fullMoon.first?.pos ?? 0.0)
                        }
                        ForEach(1...model.chineseCalendar.numberOfDaysInMonth, id: \.self) { day in
                            let dateText = switch day {
                            case fullMoonDay:
                                Text("\(day)")
                                    .foregroundStyle(.orange)
                            default:
                                Text("\(day)")
                            }
                            let dayButton = Button {
                                withAnimation {
                                    model.chineseDate.day = day
                                }
                            } label: {
                                dateText
                                    .lineLimit(1)
                                    .fixedSize()
                            }
                                .buttonBorderShape(.circle)
                                .frame(minWidth: cellSize, minHeight: cellSize)

                            if model.chineseDate.day == day {
                                dayButton
#if os(visionOS)
                                    .buttonStyle(.automatic)
#else
                                    .buttonStyle(.bordered)
                                    .fontWeight(.bold)
                                    .tint(.blue)
#endif
                            } else {
                                dayButton
                                    .foregroundStyle(.primary)
                                    .buttonStyle(.borderless)
                            }
                        }
                    }
                    .animation(.default, value: model.chineseDate)
                } prevAction: {
                    model.previousMonth()
                } nextAction: {
                    model.nextMonth()
                }
            }
        }
    }
}

struct ChinendarTimePickerPanel: View {
    private var model: TimePickerModel
    private let columns = Array(repeating: GridItem(spacing: 0), count: 6)
    @State private var hourView = false
#if os(visionOS)
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 65
#elseif os(iOS)
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 50
#else
    @ScaledMetric(relativeTo: .body) var cellSize: CGFloat = 30
#endif

    init(chineseCalendar: Binding<ChineseCalendar>) {
        self.model = TimePickerModel(chineseCalendar: chineseCalendar)
    }

    var body: some View {
        VStack {
            HStack {
                Button {
                    withAnimation {
                        hourView.toggle()
                    }
                } label: {
                    HStack {
                        Text(model.chineseCalendar.hourName(hour: model.hour))
                            .fontWeight(.bold)
                            .lineLimit(1)
                        if hourView {
                            Image(systemName: "chevron.up")
                                .font(.footnote)
                        } else {
                            Image(systemName: "chevron.forward")
                                .font(.footnote)
                        }
                    }
                    .labelStyle(.titleAndIcon)
                    .animation(.default, value: hourView)
                }
                .padding(.horizontal)
                .animation(.default, value: model.hour)
                Spacer()
                if hourView {
                    Button {
                        withAnimation {
                            model.prevDay()
                        }
                    } label: {
                        Label("PREV_DAY", systemImage: "chevron.backward")
                            .fontWeight(.bold)
                    }
                    Text("DAY_ABV")
                    Button {
                        withAnimation {
                            model.nextDay()
                        }
                    } label: {
                        Label("NEXT_DAY", systemImage: "chevron.forward")
                            .fontWeight(.bold)
                    }
                } else {
                    Button {
                        withAnimation {
                            model.prevHour()
                        }
                    } label: {
                        Label("PREV_HOUR", systemImage: "chevron.backward")
                            .fontWeight(.bold)
                    }
                    Text("HOUR_ABV")
                    Button {
                        withAnimation {
                            model.nextHour()
                        }
                    } label: {
                        Label("NEXT_HOUR", systemImage: "chevron.forward")
                            .fontWeight(.bold)
                    }
                }
            }
            .labelStyle(.iconOnly)

            Divider()
                .padding(5)

            if hourView {
                DragablePicker {
                    LazyVGrid(columns: columns) {
                        ForEach(Array(stride(from: 0, to: 24, by: model.largeHour ? 2 : 1)), id: \.self) { hour in
                            let hourButton = Button {
                                withAnimation {
                                    model.hour = hour
                                }
                            } label: {
                                Text(model.chineseCalendar.hourName(hour: hour))
                                    .lineLimit(1)
                                    .fixedSize()
                            }
                                .frame(minWidth: cellSize * 2, minHeight: model.largeHour ? cellSize : cellSize * 0.8)
                                .buttonBorderShape(.capsule)
                            if hour == model.hour {
                                hourButton
#if os(visionOS)
                                    .buttonStyle(.automatic)
#else
                                    .buttonStyle(.bordered)
                                    .fontWeight(.bold)
                                    .tint(.blue)
#endif
                            } else {
                                hourButton
                                    .foregroundStyle(.primary)
                                    .buttonStyle(.borderless)
                            }
                        }
                    }
                    .animation(.default, value: model.hour)
#if os(macOS)
                    .fixedSize()
#endif
                } prevAction: {
                    model.prevDay()
                } nextAction: {
                    model.nextDay()
                }
            } else {
                DragablePicker {
                    VStack {
                        LazyVGrid(columns: columns) {
                            ForEach(0..<model.maxQuarterMajor, id: \.self) { quarterMajor in
                                let quarterMajorButton = Button {
                                    withAnimation {
                                        model.quarterMajor = quarterMajor
                                    }
                                } label: {
                                    Text("\(ChineseCalendar.chineseNumbersLocalized[quarterMajor])QUARTER")
                                        .lineLimit(1)
                                        .fixedSize()
                                }
                                    .frame(minWidth: cellSize * 1.7, minHeight: cellSize)
                                    .buttonBorderShape(.capsule)
                                if quarterMajor == model.quarterMajor {
                                    quarterMajorButton
#if os(visionOS)
                                        .buttonStyle(.automatic)
#else
                                        .buttonStyle(.bordered)
                                        .fontWeight(.bold)
                                        .tint(.blue)
#endif
                                } else {
                                    quarterMajorButton
                                        .foregroundStyle(.primary)
                                        .buttonStyle(.borderless)
                                }
                            }
                        }
                        .animation(.default, value: model.quarterMinor)
                        .animation(.default, value: model.quarterMajor)
                        Divider()
                            .padding(0)
                        LazyVGrid(columns: columns) {
                            ForEach(0..<model.maxQuarterMinor, id: \.self) { quarterMinor in
                                let quarterMinorButton = Button {
                                    withAnimation {
                                        model.quarterMinor = quarterMinor
                                    }
                                } label: {
                                    Text(ChineseCalendar.chineseNumbersLocalized[quarterMinor])
                                        .lineLimit(1)
                                        .fixedSize()
                                }
                                    .frame(minWidth: cellSize, minHeight: cellSize)
                                    .buttonBorderShape(.circle)
                                if quarterMinor == model.quarterMinor {
                                    quarterMinorButton
#if os(visionOS)
                                        .buttonStyle(.automatic)
#else
                                        .buttonStyle(.bordered)
                                        .fontWeight(.bold)
                                        .tint(.blue)
#endif
                                } else {
                                    quarterMinorButton
                                        .foregroundStyle(.primary)
                                        .buttonStyle(.borderless)
                                }
                            }
                        }
                        .animation(.default, value: model.hour)
                        .animation(.default, value: model.quarterMajor)
                        .animation(.default, value: model.quarterMinor)
                    }
                } prevAction: {
                    model.prevHour()
                } nextAction: {
                    model.nextHour()
                }
            }
        }
    }
}

struct ChinendarDatePicker: View {
    @Binding var chineseCalendar: ChineseCalendar
    @State private var presentPicker = false

    var body: some View {
        Button {
            presentPicker = true
        } label: {
            Text(chineseCalendar.dateStringLocalized)
        }
        .foregroundStyle(.primary)
        .popover(isPresented: $presentPicker, arrowEdge: .top) {
            ChinendarDatePickerPanel(chineseCalendar: $chineseCalendar)
                .padding()
                .presentationCompactAdaptation(.popover)
        }
    }
}

struct ChinendarTimePicker: View {
    @Binding var chineseCalendar: ChineseCalendar
    @State private var presentPicker = false

    var body: some View {
        Button {
            presentPicker = true
        } label: {
            Text(chineseCalendar.timeStringLocalized)
        }
        .foregroundStyle(.primary)
        .popover(isPresented: $presentPicker, arrowEdge: .top) {
            ChinendarTimePickerPanel(chineseCalendar: $chineseCalendar)
                .padding()
                .presentationCompactAdaptation(.popover)
        }
    }
}

#Preview("non Watch") {
    @Previewable @State var chineseCalendar = ChineseCalendar()
    HStack {
        ChinendarDatePicker(chineseCalendar: $chineseCalendar)
        ChinendarTimePicker(chineseCalendar: $chineseCalendar)
    }
}
#endif
