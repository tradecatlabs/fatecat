//
//  ColorSetting.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI

struct ColorSetting: View {
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            Section("PLANETS") {
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("MERCURY"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.mercury.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("VENUS"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.venus.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("MARS"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.mars.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("JUPYTER"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.jupiter.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("SATURN"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.saturn.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("MOON"), color: viewModel.binding(\.baseLayout.colors.planetIndicator.moon.cgColor))
                }
            }

            Section("MP_&_ST") {
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("NEW_MOON"), color: viewModel.binding(\.baseLayout.colors.monthlyIndicators.newMoon.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("FULL_MOON"), color: viewModel.binding(\.baseLayout.colors.monthlyIndicators.fullMoon.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("ODD_ST"), color: viewModel.binding(\.baseLayout.colors.monthlyIndicators.oddSolarTerm.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("EVEN_ST"), color: viewModel.binding(\.baseLayout.colors.monthlyIndicators.evenSolarTerm.cgColor))
                }
            }

            Section("SUNRISE_SET") {
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("SUNRISE"), color: viewModel.binding(\.baseLayout.colors.sunPositionIndicator.sunrise.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("NOON"), color: viewModel.binding(\.baseLayout.colors.sunPositionIndicator.noon.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("SUNSET"), color: viewModel.binding(\.baseLayout.colors.sunPositionIndicator.sunset.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("MID_NIGHT"), color: viewModel.binding(\.baseLayout.colors.sunPositionIndicator.midnight.cgColor))
                }
            }

            Section("MOONRISE_SET") {
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("MOONRISE"), color: viewModel.binding(\.baseLayout.colors.moonPositionIndicator.moonrise.cgColor))
                    Divider()
                    ColorSettingCell(text: Text("LUNAR_NOON"), color: viewModel.binding(\.baseLayout.colors.moonPositionIndicator.highMoon.cgColor))
                }
                HStack(spacing: 20) {
                    ColorSettingCell(text: Text("MOONSET"), color: viewModel.binding(\.baseLayout.colors.moonPositionIndicator.moonset.cgColor))
                }
            }
        }
        .formStyle(.grouped)
        .navigationTitle("COLOR_MARKS")
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

struct ColorSettingCell: View {
    let text: Text
    @Binding var color: CGColor

    var body: some View {
        HStack {
            text
                .lineLimit(1)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.trailing, 10)
            ColorPicker("", selection: $color)
                .labelsHidden()
        }
    }
}

#Preview("Color Setting", traits: .modifier(SampleData())) {
    NavigationStack {
        ColorSetting()
    }
}
