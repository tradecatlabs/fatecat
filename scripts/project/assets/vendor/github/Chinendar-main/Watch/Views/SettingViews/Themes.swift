//
//  Themes.swift
//  Chinendar
//
//  Created by Leo Liu on 1/21/25.
//

import SwiftUI
import SwiftData

struct ThemesList: View {
    @Query(filter: ThemeData.predicate, sort: \ThemeData.modifiedDate, order: .reverse) private var dataStack: [ThemeData]
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext
    private let currentDeviceName = AppInfo.deviceName
    private var themes: [String: [ThemeData]] {
        loadThemes(data: dataStack)
    }
    private var deviceNames: [String] {
        [currentDeviceName] + themes.keys.filter { $0 != currentDeviceName }
    }

    var body: some View {
        List {
            Section {
                Toggle("SYNC_PHONE", isOn: viewModel.binding(\.watchLayout.syncFromPhone))
            }
            ForEach(deviceNames, id: \.self) { groupName in
                if themes[groupName] != nil || groupName == currentDeviceName {
                    let group = themes[groupName] ?? []
                    ThemeGroup(groupName: groupName, themes: group, isCurrentDevice: groupName == currentDeviceName)
                }
            }
        }
        .onAppear {
            cleanup()
        }
        .navigationTitle("THEME_LIST")
    }

    private func cleanup() {
        var records = Set<[String]>()
        for data in dataStack {
            if data.isNil {
                modelContext.delete(data)
            } else {
                if records.contains([data.name!, data.deviceName!]) {
                    modelContext.delete(data)
                } else {
                    records.insert([data.name!, data.deviceName!])
                }
            }
        }
    }

    private func loadThemes(data: [ThemeData]) -> [String: [ThemeData]] {
        var newThemes = [String: [ThemeData]]()
        for data in data where !data.isNil {
            if newThemes[data.deviceName!] == nil {
                newThemes[data.deviceName!] = [data]
            } else {
                newThemes[data.deviceName!]!.append(data)
            }
        }
        for deviceName in newThemes.keys {
            newThemes[deviceName]!.sort { $0.modifiedDate! > $1.modifiedDate! }
        }
        return newThemes
    }
}

struct ThemeGroup: View {
    @Environment(ViewModel.self) private var viewModel
    let groupName: String
    let themes: [ThemeData]
    let isCurrentDevice: Bool

    @State private var target: ThemeData?
    @State private var showSwitch = false

    var body: some View {
        Section {
            if isCurrentDevice {
                let data = try! ThemeData(WatchLayout.defaultLayout, name: AppInfo.defaultName, deviceName: groupName)
                Button {
                    target = data
                    showSwitch = true
                } label: {
                    ThemeRow(theme: data)
                }
                .disabled(viewModel.watchLayout.syncFromPhone)
            }
            ForEach(themes, id: \.self) { theme in
                Button {
                    target = theme
                    showSwitch = true
                } label: {
                    ThemeRow(theme: theme)
                }
                .disabled(viewModel.watchLayout.syncFromPhone)
            }
        } header: {
            Text(groupName)
        }
        .buttonStyle(.plain)
        .switchAlert(isPresented: $showSwitch, theme: $target, isCurrentDevice: isCurrentDevice)
    }
}

struct ThemeRow: View {
    @Environment(ViewModel.self) private var viewModel
    let theme: ThemeData

    var body: some View {
        Button {
            viewModel.watchLayout ?= theme.theme
        } label: {
            Text(theme.nonNilName)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
    }
}

private struct SwitchAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    @Binding var theme: ThemeData?
    let isCurrentDevice: Bool

    func body(content: Content) -> some View {
        if let theme {
            content
                .alert(Text("SWITCH_TO:\(theme.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.theme = nil }
                    Button("CONFIRM", role: .destructive) {
                        if let newLayout = theme.theme {
                            if isCurrentDevice {
                                viewModel.watchLayout = newLayout
                            } else {
                                viewModel.baseLayout = newLayout.baseLayout
                            }
                        }
                        self.theme = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func switchAlert(isPresented: Binding<Bool>, theme: Binding<ThemeData?>, isCurrentDevice: Bool) -> some View {
        self.modifier(SwitchAlert(isPresented: isPresented, theme: theme, isCurrentDevice: isCurrentDevice))
    }
}

#Preview("Themes", traits: .modifier(SampleData())) {
    ThemesList()
}
