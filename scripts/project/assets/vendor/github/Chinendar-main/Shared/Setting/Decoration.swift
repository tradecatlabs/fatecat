//
//  Decoration.swift
//  Chinendar
//
//  Created by Leo Liu on 1/16/24.
//

import SwiftUI

struct DecorationSetting: View {
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            Section("TRANSPARENCY") {
                SliderView(value: viewModel.binding(\.baseLayout.colors.shadeAlpha), min: 0, max: 1, label: Text("OFF_RING_OPACITY"))
                SliderView(value: viewModel.binding(\.baseLayout.colors.majorTickAlpha), min: 0, max: 1, label: Text("MJ_TICK_OPACITY"))
                SliderView(value: viewModel.binding(\.baseLayout.colors.minorTickAlpha), min: 0, max: 1, label: Text("MN_TICK_OPACITY"))
            }
            Section("COLOR_IN_L/D") {
#if os(visionOS)
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("MJ_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.majorTickColor.dark.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("MN_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.minorTickColor.dark.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("ODD_ST_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.oddSolarTermTickColor.dark.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("EVEN_ST_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.evenSolarTermTickColor.dark.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("TEXT_COLOR"), color: viewModel.binding(\.baseLayout.colors.fontColor.dark.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("CENTER_BACK_COLOR"), color: viewModel.binding(\.baseLayout.colors.innerColor.dark.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("RING_BACK_COLOR"), color: viewModel.binding(\.baseLayout.colors.backColor.dark.cgColor))
                }
#else
                ThemedColorSettingCell(text: Text("MJ_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.majorTickColor))
                ThemedColorSettingCell(text: Text("MN_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.minorTickColor))
                ThemedColorSettingCell(text: Text("ODD_ST_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.oddSolarTermTickColor))
                ThemedColorSettingCell(text: Text("EVEN_ST_TICK_COLOR"), color: viewModel.binding(\.baseLayout.colors.evenSolarTermTickColor))
                ThemedColorSettingCell(text: Text("TEXT_COLOR"), color: viewModel.binding(\.baseLayout.colors.fontColor))
                ThemedColorSettingCell(text: Text("CENTER_BACK_COLOR"), color: viewModel.binding(\.baseLayout.colors.innerColor))
                ThemedColorSettingCell(text: Text("RING_BACK_COLOR"), color: viewModel.binding(\.baseLayout.colors.backColor))
#endif
            }
        }
        .formStyle(.grouped)
        .navigationTitle("ADDON_COLORS")
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
}

struct SliderView: View {
    @Binding var value: CGFloat
    @State var currentValue: CGFloat = 0
    let min: CGFloat
    let max: CGFloat
    let label: Text

    var body: some View {
#if os(iOS) || os(visionOS)
        VStack {
            HStack {
                label
                Spacer()

                let formatter: NumberFormatter = {
                    let formatter = NumberFormatter()
                    formatter.maximumFractionDigits = 2
                    formatter.minimumFractionDigits = 0
                    return formatter
                }()
                Text(formatter.string(from: NSNumber(value: currentValue)) ?? "")
                    .frame(alignment: .trailing)
            }
            Slider(value: $currentValue, in: min...max, step: 0.01) { editing in
                if !editing {
                    value = currentValue
                }
            }
            .labelsHidden()
        }
        .onAppear {
            currentValue = value
        }
#elseif os(macOS)
        HStack {
            label
                .frame(maxWidth: 150, alignment: .leading)
            Slider(value: $currentValue, in: min...max, step: 0.01) { editing in
                if !editing {
                    value = currentValue
                }
            }
            .labelsHidden()

            let formatter: NumberFormatter = {
                let formatter = NumberFormatter()
                formatter.maximumFractionDigits = 2
                formatter.minimumFractionDigits = 0
                return formatter
            }()
            Text(formatter.string(from: NSNumber(value: currentValue)) ?? "")
                .frame(maxWidth: 40, alignment: .trailing)
        }
        .onAppear {
            currentValue = value
        }
#endif
    }
}

struct ThemedColorSettingCell: View {
    let text: Text
    @Binding var color: ThemedColor

    var body: some View {
        HStack {
            text
                .lineLimit(1)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.trailing, 10)
            Text("LIGHT")
                .lineLimit(1)
                .frame(alignment: .trailing)
                .padding(.horizontal, 5)
            ColorPicker("", selection: $color.light.cgColor)
                .labelsHidden()
                .padding(.trailing, 10)
            Divider()
            Text("DARK")
                .lineLimit(1)
                .frame(alignment: .trailing)
                .padding(.horizontal, 5)
            ColorPicker("", selection: $color.dark.cgColor)
                .labelsHidden()

        }
    }
}

#Preview("Decoration Setting", traits: .modifier(SampleData())) {
    NavigationStack {
        DecorationSetting()
    }
}
