//
//  LayoutSetting.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI
import Observation

struct LayoutSetting: View {
    @Environment(ViewModel.self) var viewModel
#if os(macOS) || os(visionOS)
    static let nameMapping = [
        " ": LocalizedStringKey("SPACE"),
        "・": LocalizedStringKey("・"),
        "": LocalizedStringKey("NONE")
    ]
#endif
#if os(macOS)
    @State var fontHandler = FontHandler()
#endif

    var body: some View {
        Form {
#if os(macOS) || os(visionOS)
            Section("STATUS_BAR") {
                HStack(spacing: 20) {
                    Toggle("DATE", isOn: viewModel.binding(\.watchLayout.statusBar.date))
                    Divider()
                    Toggle("TIME", isOn: viewModel.binding(\.watchLayout.statusBar.time))
                }
                HStack(spacing: 20) {
                    Picker("NUMBER_OF_HOLIDAY", selection: viewModel.binding(\.watchLayout.statusBar.holiday)) {
                        ForEach(0...2, id: \.self) { Text(String($0)) }
                    }
                    Divider()
                    Picker("SEPARATOR", selection: viewModel.binding(\.watchLayout.statusBar.separator)) {
                        ForEach(StatusBar.Separator.allCases, id: \.self) { separator in
                            if let label = LayoutSetting.nameMapping[separator.rawValue] {
                                Text(label)
                            } else {
                                Text(separator.rawValue)
                            }
                        }
                    }
                }
            }
#endif
#if os(macOS)
            Section("FONT") {
                HStack(spacing: 20) {
                    Picker("TEXT_FONT", selection: $fontHandler.textFontSelection) {
                        ForEach(fontHandler.allFonts, id: \.self) { family in
                            Text(family)
                        }
                    }
                    Divider()
                    Picker("FONT_WEIGHT", selection: $fontHandler.textFontMemberSelection) {
                        ForEach(fontHandler.textFontMembers, id: \.self) { member in
                            Text(member)
                        }
                    }
                    .labelsHidden()
                }

                HStack(spacing: 20) {
                    Picker("CENTER_TEXT_FONT", selection: $fontHandler.centerFontSelection) {
                        ForEach(fontHandler.allFonts, id: \.self) { family in
                            Text(family)
                        }
                    }
                    Divider()
                    Picker("FONT_WEIGHT", selection: $fontHandler.centerFontMemberSelection) {
                        ForEach(fontHandler.centerFontMembers, id: \.self) { member in
                            Text(member)
                        }
                    }
                    .labelsHidden()
                }
            }
                .onChange(of: fontHandler.textFont) {
                    if let font = fontHandler.textFont {
                        viewModel.watchLayout.textFont = font
                    }
                }

                .onChange(of: fontHandler.centerFont) {
                    if let font = fontHandler.centerFont {
                        viewModel.watchLayout.centerFont = font
                    }
                }
#endif
#if os(iOS)
            Section("SHAPE") {
                LayoutSettingCell(text: viewModel.settings.vertical ? Text("WIDTH") : Text("HEIGHT"), value: viewModel.binding(\.baseLayout.offsets.watchSize.width)) { max(10.0, $0) }
                LayoutSettingCell(text: viewModel.settings.vertical ? Text("HEIGHT") : Text("WIDTH"), value: viewModel.binding(\.baseLayout.offsets.watchSize.height)) { max(10.0, $0) }
                SliderView(value: viewModel.binding(\.baseLayout.offsets.cornerRadiusRatio), min: 0, max: 1, label: Text("CORNER_RD_RATIO"))
                SliderView(value: viewModel.binding(\.baseLayout.colors.shadowSize), min: 0, max: 0.1, label: Text("SHADOW_SIZE"))
            }
            Section(header: Text("TEXT_OFFSET")) {
                LayoutSettingCell(text: Text("CENTER_TEXT_H_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.centerTextOffset.width))
                LayoutSettingCell(text: Text("CENTER_TEXT_V_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.centerTextOffset.height))
                LayoutSettingCell(text: Text("TEXT_H_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.textOffset.width))
                LayoutSettingCell(text: Text("TEXT_V_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.textOffset.height))
            }
#elseif os(macOS) || os(visionOS)
            Section("SHAPE") {
#if os(macOS)
                HStack(spacing: 20) {
                    LayoutSettingCell(text: Text("WIDTH"), value: viewModel.binding(\.baseLayout.offsets.watchSize.width)) { max(10.0, $0) }
                    Divider()
                    LayoutSettingCell(text: Text("HEIGHT"), value: viewModel.binding(\.baseLayout.offsets.watchSize.height)) { max(10.0, $0) }
                }
#endif
                SliderView(value: viewModel.binding(\.baseLayout.offsets.cornerRadiusRatio), min: 0, max: 1, label: Text("CORNER_RD_RATIO"))
                SliderView(value: viewModel.binding(\.baseLayout.colors.shadowSize), min: 0, max: 0.1, label: Text("SHADOW_SIZE"))
            }
            Section("TEXT_OFFSET") {
                HStack(spacing: 20) {
                    LayoutSettingCell(text: Text("CENTER_TEXT_H_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.centerTextOffset.width))
                    Divider()
                    LayoutSettingCell(text: Text("CENTER_TEXT_V_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.centerTextOffset.height))
                }
                HStack(spacing: 20) {
                    LayoutSettingCell(text: Text("TEXT_H_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.textOffset.width))
                    Divider()
                    LayoutSettingCell(text: Text("TEXT_V_OFFSET"), value: viewModel.binding(\.baseLayout.offsets.textOffset.height))
                }
            }
#endif
        }
        .formStyle(.grouped)
        .navigationTitle("LAYOUTS")
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
#elseif os(macOS)
        .task {
            fontHandler.textFont = viewModel.watchLayout.textFont
            fontHandler.centerFont = viewModel.watchLayout.centerFont
        }
#endif
    }
}

struct LayoutSettingCell<V: Numeric>: View {
    let text: Text
    @Binding var value: V
    let validation: ((V) -> V)?
    @State var tempValue: V
    @FocusState var isFocused: Bool

    init(text: Text, value: Binding<V>, validation: ((V) -> V)? = nil) {
        self.text = text
        self._value = value
        self.validation = validation
        self._tempValue = State(initialValue: value.wrappedValue)
    }

    var body: some View {
        HStack {
            text
                .lineLimit(1)
                .frame(maxWidth: .infinity, alignment: .leading)
            TextField("", value: $tempValue, formatter: {
                let formatter = NumberFormatter()
                formatter.maximumFractionDigits = 2
                formatter.minimumFractionDigits = 0
                return formatter
            }())
#if os(iOS) || os(visionOS)
            .keyboardType(.decimalPad)
#endif
            .focused($isFocused)
            .autocorrectionDisabled()
            .onSubmit(of: .text) {
                commit()
            }
            .onChange(of: isFocused) {
                if !isFocused {
                    commit()
                }
            }
            .task {
                tempValue = value
            }
#if os(iOS)
            .padding(.vertical, 5)
#elseif os(macOS)
            .frame(height: 20)
#elseif os(visionOS)
            .frame(height: 40)
#endif
            .padding(.leading, 15)
#if os(iOS) || os(visionOS)
            .background(.thickMaterial, in: RoundedRectangle(cornerRadius: 10))
            .contentShape(.hoverEffect, .rect(cornerRadius: 10, style: .continuous))
            .hoverEffect()
#elseif os(macOS)
            .background(in: RoundedRectangle(cornerRadius: 10))
#endif
        }
    }

    func commit() {
        if let validation {
            tempValue = validation(tempValue)
        }
        value = tempValue
    }
}

#if os(macOS)
@Observable class FontHandler {
    let allFonts = NSFontManager.shared.availableFontFamilies
    var textFontMembers = [String]()
    var centerFontMembers = [String]()
    var textFontSelection: String = "" {
        didSet {
            textFontMembers = populateFontMembers(for: textFontSelection)
            if let first = textFontMembers.first {
                textFontMemberSelection = first
            }
        }
    }
    var textFontMemberSelection: String = ""
    var centerFontSelection: String = "" {
        didSet {
            centerFontMembers = populateFontMembers(for: centerFontSelection)
            if let first = centerFontMembers.first {
                centerFontMemberSelection = first
            }
        }
    }
    var centerFontMemberSelection: String = ""

    var textFont: NSFont? {
        get {
            readFont(family: textFontSelection, style: textFontMemberSelection)
        } set {
            if let newValue {
                let (textFamily, textMember) = getFontFamilyAndMember(font: newValue)
                if let textFamily {
                    textFontSelection = textFamily
                    textFontMembers = populateFontMembers(for: textFamily)
                    textFontMemberSelection = textMember ?? textFontMembers.first ?? textFontMemberSelection
                }
            }
        }
    }

    var centerFont: NSFont? {
        get {
            readFont(family: centerFontSelection, style: centerFontMemberSelection)
        } set {
            if let newValue {
                let (centerFamily, centerMember) = getFontFamilyAndMember(font: newValue)
                if let centerFamily {
                    centerFontSelection = centerFamily
                    centerFontMembers = populateFontMembers(for: centerFamily)
                    centerFontMemberSelection = centerMember ?? centerFontMembers.first ?? centerFontMemberSelection
                }
            }
        }
    }

    func populateFontMembers(for fontFamily: String) -> [String] {
        var allMembers = [String]()
        let members = NSFontManager.shared.availableMembers(ofFontFamily: fontFamily)
        if let members {
            for member in members {
                if let fontType = member[1] as? String {
                    allMembers.append(fontType)
                }
            }
        }
        return allMembers
    }

    func readFont(family: String, style: String) -> NSFont? {
        let size = NSFont.systemFontSize
        if let font = NSFont(name: "\(family.filter { !$0.isWhitespace })-\(style.filter { !$0.isWhitespace })", size: size) {
            return font
        }
        if let members = NSFontManager.shared.availableMembers(ofFontFamily: family) {
            for i in 0..<members.count {
                if let memberName = members[i][1] as? String, memberName == style,
                   let weight = members[i][2] as? Int,
                   let traits = members[i][3] as? UInt {
                    return NSFontManager.shared.font(withFamily: family, traits: NSFontTraitMask(rawValue: traits), weight: weight, size: size)
                }
            }
        }
        if let font = NSFont(name: family, size: size) {
            return font
        }
        return nil
    }

    func getFontFamilyAndMember(font: NSFont) -> (String?, String?) {
        let family = font.familyName
        let member = font.fontName.split(separator: "-").last.map {String($0)}
        return (family, member)
    }
}
#endif

#Preview("LayoutSetting", traits: .modifier(SampleData())) {
    NavigationStack {
        LayoutSetting()
    }
}
