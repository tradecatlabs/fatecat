//
//  CalendarConfig.swift
//  Chinendar
//
//  Created by Leo Liu on 3/29/24.
//

import SwiftUI
import SwiftData

struct ConfigList: View {
    @Query(filter: ConfigData.predicate, sort: \ConfigData.modifiedDate, order: .reverse) private var configs: [ConfigData]
    @Environment(\.modelContext) private var modelContext
    @Environment(ViewModel.self) var viewModel

    @State private var target: ConfigData?
    @State private var showSwitch = false
    @State private var showUpdate = false
    @State private var showRename = false
    @State private var showSaveNew = false
    @State private var showDelete = false
#if os(iOS) || os(visionOS)
    @State private var showImport = false
    @State private var showExport = false
#endif

    var body: some View {
        Form {
            Section {
                let data = try! ConfigData(CalendarConfigure(), name: AppInfo.defaultName)
                HighlightButton {
                    target = data
                    showSwitch = true
                } label: {
                    ConfigRow(configData: data, showTime: false)
                }
            }
            Section {
                ForEach(configs, id: \.self) { config in
                    HighlightButton {
                        target = config
                        showSwitch = true
                    } label: {
                        ConfigRow(configData: config, showTime: true)
                    }
                    .contextMenu {
                        contextMenu(config: config)
                            .labelStyle(.titleAndIcon)
                    }
                }
            }
        }
        .formStyle(.grouped)
        .errorAlert()
        .switchAlert(isPresented: $showSwitch, config: $target)
        .updateAlert(isPresented: $showUpdate, config: $target)
        .renameAlert(isPresented: $showRename, config: $target, existingNames: configs.compactMap(\.name))
        .deleteAlert(isPresented: $showDelete, config: $target)
        .saveNewAlert(isPresented: $showSaveNew, existingNames: configs.compactMap(\.name))
#if os(iOS) || os(visionOS)
        .exportAlert(isPresented: $showExport, config: $target)
        .importAlert(isPresented: $showImport, existingNames: configs.compactMap(\.name))
#endif
        .onAppear {
            cleanup()
        }
        .navigationTitle("CALENDAR_LIST")
        .toolbar {
#if os(macOS) || os(visionOS)
            ToolbarItemGroup {
                importButton
                saveNewButton
            }
#else
            Menu {
                importButton
                saveNewButton
            } label: {
                Label("MANAGE_LIST", systemImage: "ellipsis")
            }
#endif
        }
#if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
#endif
    }

    var saveNewButton: some View {
        Button { showSaveNew = true } label: {
            Label("SAVE_NEW", systemImage: "plus")
        }
    }

    var importButton: some View {
        Button {
#if os(macOS)
            readFile(viewModel: viewModel) { data, name in
                Task { @MainActor in
                    let newName = validName(name, existingNames: Set(configs.compactMap(\.name)))
                    let config = try CalendarConfigure(fromData: data)
                    let configData = try ConfigData(config, name: newName)
                    modelContext.insert(configData)
                }
            }
#else
            showImport = true
#endif
        } label: {
            Label("IMPORT", systemImage: "square.and.arrow.down")
        }
    }

    @ViewBuilder func contextMenu(config: ConfigData) -> some View {
        Button {
            target = config
            showUpdate = true
        } label: {
            Label("UPDATE", systemImage: "arrow.clockwise")
        }
        Button {
            target = config
            showRename = true
        } label: {
            Label("RENAME", systemImage: "rectangle.and.pencil.and.ellipsis")
        }
        Button {
#if os(iOS) || os(visionOS)
            target = config
            showExport = true
#else
            if let data = try? config.config?.encode() {
                writeFile(viewModel: viewModel, name: config.nonNilName, data: data)
            } else {
                print("Writing to file failed")
            }
#endif
        } label: {
            Label("EXPORT", systemImage: "square.and.arrow.up")
        }
        Button(role: .destructive) {
            target = config
            showDelete = true
        } label: {
            Label("DELETE", systemImage: "trash")
        }
    }

    private func cleanup() {
        var records = Set<String>()
        for data in configs {
            if data.isNil {
                modelContext.delete(data)
            } else {
                if records.contains(data.name!) {
                    modelContext.delete(data)
                } else {
                    records.insert(data.name!)
                }
            }
        }
    }
}

struct ConfigRow: View {
    @Environment(ViewModel.self) private var viewModel
    let configData: ConfigData
    let showTime: Bool

    var chineseDate: String {
        guard let config = configData.config else { return "" }
        let location = config.locationEnabled ? viewModel.gpsLocation ?? config.customLocation : config.customLocation
        let calendar = ChineseCalendar(time: viewModel.chineseCalendar.time,
                                       timezone: config.effectiveTimezone,
                                       location: location,
                                       globalMonth: config.globalMonth, apparentTime: config.apparentTime,
                                       largeHour: config.largeHour)
        var displayText = [String]()
        displayText.append(calendar.dateString)
        let holidays = calendar.holidays
        displayText.append(contentsOf: holidays[..<min(holidays.count, 1)])
        displayText.append(calendar.hourString + calendar.quarterString)
        return displayText.joined(separator: " ")
    }

    var body: some View {
        HStack {
            Text(configData.nonNilName)
            Spacer()
            if showTime {
                Text(String(chineseDate.reversed()))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

// MARK: Modifiers - Private

private struct SwitchAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    @Binding var configData: ConfigData?

    func body(content: Content) -> some View {
        if let configData {
            content
                .alert(Text("SWITCH_TO:\(configData.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.configData = nil }
                    Button("CONFIRM", role: .destructive) {
                        if let newConfig = configData.config {
                            viewModel.config = newConfig
                        }
                        self.configData = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func switchAlert(isPresented: Binding<Bool>, config: Binding<ConfigData?>) -> some View {
        self.modifier(SwitchAlert(isPresented: isPresented, configData: config))
    }
}

private struct UpdateAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    @Binding var configData: ConfigData?

    func body(content: Content) -> some View {
        if let configData {
            content
                .alert(Text("UPDATE:\(configData.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.configData = nil }
                    Button("CONFIRM", role: .destructive) {
                        configData.config = viewModel.config
                        self.configData = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func updateAlert(isPresented: Binding<Bool>, config: Binding<ConfigData?>) -> some View {
        self.modifier(UpdateAlert(isPresented: isPresented, configData: config))
    }
}

private struct DeleteAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var configData: ConfigData?

    func body(content: Content) -> some View {
        if let configData {
            content
                .alert(Text("DELETE:\(configData.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.configData = nil }
                    Button("CONFIRM", role: .destructive) {
                        modelContext.delete(configData)
                        self.configData = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func deleteAlert(isPresented: Binding<Bool>, config: Binding<ConfigData?>) -> some View {
        self.modifier(DeleteAlert(isPresented: isPresented, configData: config))
    }
}

private struct RenameAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var configData: ConfigData?
    let existingNames: Set<String>
    @State private var newName = String(localized: "UNNAMED")

    func body(content: Content) -> some View {
        if let configData {
            content
                .onChange(of: isPresented, initial: true) {
                    if isPresented {
                        newName = validName(configData.name ?? newName, existingNames: existingNames)
                    }
                }
                .alert(Text("RENAME:\(configData.nonNilName)"), isPresented: $isPresented) {
                    TextField("NEW_NAME", text: $newName)
                        .labelsHidden()
                    Button("CANCEL", role: .cancel) { self.configData = nil }
                    Button("CONFIRM_NAME", role: .destructive) {
                        configData.name = newName
                        self.configData = nil
                    }
                    .disabled(existingNames.contains(newName))
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func renameAlert(isPresented: Binding<Bool>, config: Binding<ConfigData?>, existingNames: [String]) -> some View {
        self.modifier(RenameAlert(isPresented: isPresented, configData: config, existingNames: Set(existingNames)))
    }
}

private struct SaveNewAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    let existingNames: Set<String>

    @State private var newName = String(localized: "UNNAMED")

    func body(content: Content) -> some View {
        content
            .onChange(of: isPresented, initial: true) {
                if isPresented {
                    newName = validName(newName, existingNames: existingNames)
                }
            }
            .alert(Text("SAVE_NEW"), isPresented: $isPresented) {
                TextField("NEW_NAME", text: $newName)
                    .labelsHidden()
                Button("CANCEL", role: .cancel) {}
                Button("CONFIRM_NAME", role: .destructive) {
                    do {
                        let newConfig = try ConfigData(viewModel.config, name: newName)
                        modelContext.insert(newConfig)
                    } catch {
                        viewModel.error = error
                    }
                }
                .disabled(existingNames.contains(newName))
            }
    }
}

fileprivate extension View {
    func saveNewAlert(isPresented: Binding<Bool>, existingNames: [String]) -> some View {
        self.modifier(SaveNewAlert(isPresented: isPresented, existingNames: Set(existingNames)))
    }
}

#if os(iOS) || os(visionOS)
private struct ImportAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    let existingNames: Set<String>

    func body(content: Content) -> some View {
        content
            .fileImporter(isPresented: $isPresented, allowedContentTypes: [.json]) { result in
                switch result {
                case .success(let file):
                    do {
                        let (name, data) = try read(file: file)
                        let config = try CalendarConfigure(fromData: data)
                        let newName = validName(name, existingNames: existingNames)
                        let configData = try ConfigData(config, name: newName)
                        modelContext.insert(configData)
                    } catch {
                        viewModel.error = error
                    }
                case .failure(let error):
                    viewModel.error = error
                }
            }
    }
}

fileprivate extension View {
    func importAlert(isPresented: Binding<Bool>, existingNames: [String]) -> some View {
        self.modifier(ImportAlert(isPresented: isPresented, existingNames: Set(existingNames)))
    }
}

private struct ExportAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    @Binding var configData: ConfigData?

    func body(content: Content) -> some View {
        if let configData {
            content
                .fileExporter(isPresented: $isPresented,
                              document: TextDocument(configData),
                              contentType: .json,
                              defaultFilename: "\(configData.nonNilName).json") { result in
                    if case .failure(let error) = result {
                        viewModel.error = error
                    }
                    self.configData = nil
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func exportAlert(isPresented: Binding<Bool>, config: Binding<ConfigData?>) -> some View {
        self.modifier(ExportAlert(isPresented: isPresented, configData: config))
    }
}
#endif

#Preview("Configs", traits: .modifier(SampleData())) {
    NavigationStack {
        ConfigList()
    }
}
