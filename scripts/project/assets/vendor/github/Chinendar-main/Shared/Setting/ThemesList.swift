//
//  ThemesList.swift
//  Chinendar
//
//  Created by Leo Liu on 6/16/23.
//

import SwiftUI
import SwiftData
import UniformTypeIdentifiers

struct ThemesList: View {
    @Query(filter: ThemeData.predicate, sort: \ThemeData.modifiedDate, order: .reverse) private var dataStack: [ThemeData]
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext
    private let currentDeviceName = AppInfo.deviceName
    private var themes: [String: [ThemeData]] {
        loadThemes(data: dataStack)
    }
    private var deviceNames: [String] {
        [currentDeviceName] + themes.keys.filter { $0 != currentDeviceName }.sorted()
    }

    @State private var showSaveNew = false
#if os(iOS) || os(visionOS)
    @State private var showImport = false
#endif

    var body: some View {
        Form {
            ForEach(deviceNames, id: \.self) { groupName in
                if themes[groupName] != nil || groupName == currentDeviceName {
                    let group = themes[groupName] ?? []
                    ThemeGroup(groupName: groupName, themes: group, isCurrentDevice: groupName == currentDeviceName)
                }
            }
        }
        .formStyle(.grouped)
        .errorAlert()
        .saveNewAlert(isPresented: $showSaveNew, existingNames: themes[currentDeviceName]?.compactMap(\.name) ?? [])
#if os(iOS) || os(visionOS)
        .importAlert(isPresented: $showImport, existingNames: themes[currentDeviceName]?.compactMap(\.name) ?? [])
#endif
        .onAppear {
            cleanup()
        }
        .navigationTitle("THEME_LIST")
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
                    let newName = validName(name, existingNames: Set(themes[currentDeviceName]?.compactMap(\.name) ?? []))
                    let layout = try WatchLayout(fromData: data)
                    let theme = try ThemeData(layout, name: newName, deviceName: currentDeviceName)
                    modelContext.insert(theme)
                }
            }
#else
            showImport = true
#endif
        } label: {
            Label("IMPORT", systemImage: "square.and.arrow.down")
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
}

struct ThemeGroup: View {
    @Query(filter: ThemeData.predicate, sort: \ThemeData.modifiedDate, order: .reverse) private var dataStack: [ThemeData]
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext

    let groupName: String
    let themes: [ThemeData]
    let isCurrentDevice: Bool

    @State private var target: ThemeData?
    @State private var showSwitch = false
    @State private var showUpdate = false
    @State private var showDelete = false
    @State private var showRename = false
#if os(iOS) || os(visionOS)
    @State private var showExport = false
#endif

    var body: some View {
        Section {
            if isCurrentDevice {
                let data = try! ThemeData(WatchLayout.defaultLayout, name: AppInfo.defaultName, deviceName: groupName)
                HighlightButton {
                    target = data
                    showSwitch = true
                } label: {
                    ThemeRow(theme: data, showTime: false)
                }
            }
            ForEach(themes, id: \.self) { theme in
                HighlightButton {
                    target = theme
                    showSwitch = true
                } label: {
                    ThemeRow(theme: theme, showTime: true)
                }
                .contextMenu {
                    contextMenu(theme: theme)
                        .labelStyle(.titleAndIcon)
                } preview: {
                    if let layout = theme.theme {
                        Icon(watchLayout: layout, preview: true)
                            .frame(width: 120, height: 120)
                    }
                }
            }
        } header: {
            Text(groupName)
        }
        .switchAlert(isPresented: $showSwitch, theme: $target, isCurrentDevice: isCurrentDevice)
        .updateAlert(isPresented: $showUpdate, theme: $target)
        .deleteAlert(isPresented: $showDelete, theme: $target)
        .renameAlert(isPresented: $showRename, theme: $target, existingNames: themes.compactMap { $0.name })
#if os(iOS) || os(visionOS)
        .exportAlert(isPresented: $showExport, theme: $target)
#endif
    }

    @ViewBuilder func contextMenu(theme: ThemeData) -> some View {
        if isCurrentDevice {
            Button {
                target = theme
                showUpdate = true
            } label: {
                Label("UPDATE", systemImage: "arrow.clockwise")
            }
        }
        Button {
            target = theme
            showRename = true
        } label: {
            Label("RENAME", systemImage: "rectangle.and.pencil.and.ellipsis")
        }
        Button {
#if os(iOS) || os(visionOS)
            target = theme
            showExport = true
#else
            if let data = try? theme.theme?.encode() {
                writeFile(viewModel: viewModel, name: theme.nonNilName, data: data)
            } else {
                print("Writing to file failed")
            }
#endif
        } label: {
            Label("EXPORT", systemImage: "square.and.arrow.up")
        }
        Button(role: .destructive) {
            target = theme
            showDelete = true
        } label: {
            Label("DELETE", systemImage: "trash")
        }
    }
}

struct ThemeRow: View {
    let theme: ThemeData
    let showTime: Bool

    var body: some View {
        HStack {
            Text(theme.nonNilName)
            Spacer()
            if showTime {
                Text(.currentDate, format: .reference(to: theme.nonNilModifiedDate))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

// MARK: Utilities

#if os(macOS)
struct DynamicButtonStyle: ButtonStyle {
    var prominent: Bool
    @Environment(\.isEnabled) var isEnabled
    @ScaledMetric(relativeTo: .body) var size: CGFloat = 4

    func makeBody(configuration: Configuration) -> some View {
        let color = isEnabled ? Color.primary : Color.secondary
        configuration.label
            .padding(size)
            .overlay(
                RoundedRectangle(cornerRadius: size * 1.5)
                    .stroke(color.opacity(prominent ? 1 : 0), lineWidth: 1)
                    .fill(color.opacity(prominent ? 0.1 : 0))
            )
            .scaleEffect(configuration.isPressed && isEnabled ? 0.99 : 1.0)
            .animation(.easeInOut(duration: 0.2), value: prominent)
            .animation(.easeInOut(duration: 0.1), value: configuration.isPressed)
    }
}
#endif

struct HighlightButton<Label: View>: View {
    let action: () -> Void
    @ViewBuilder let label: () -> Label
    @State var hover = false

    var body: some View {
        Button {
            action()
        } label: {
            label()
        }
#if os(macOS)
        .onHover { over in
            hover = over
        }
        .buttonStyle(DynamicButtonStyle(prominent: hover))
#elseif os(visionOS)
        .buttonStyle(.automatic)
#else
        .buttonStyle(.borderless)
        .tint(.primary)
#endif
    }
}

struct TextDocument: FileDocument {
    static let readableContentTypes: [UTType] = [.json]
    var data: Data

    init(configuration: ReadConfiguration) {
        if let content = configuration.file.regularFileContents {
            self.data = content
        } else {
            self.data = Data()
        }
    }

    init?(_ data: ThemeData) {
        guard let theme = data.theme, let data = try? theme.encode() else { return nil }
        self.data = data
    }

    init?(_ data: ConfigData) {
        guard let config = data.config, let data = try? config.encode() else { return nil }
        self.data = data
    }

    init?(_ data: RemindersData) {
        guard let list = data.list, let data = try? list.encode() else { return nil }
        self.data = data
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        return FileWrapper(regularFileWithContents: data)
    }
}

func validName(_ name: String, existingNames: Set<String>) -> String {
    var (baseName, i) = reverseNumberedName(name)
    while existingNames.contains(numberedName(baseName, number: i)) {
        i += 1
    }
    return numberedName(baseName, number: i)

    func numberedName(_ baseName: String, number: Int) -> String {
        if number <= 1 {
            return baseName
        } else {
            return "\(baseName) \(number)"
        }
    }

    func reverseNumberedName(_ name: String) -> (String, Int) {
        let namePattern = /^(.*) (\d+)$/
        if let match = try? namePattern.firstMatch(in: name) {
            return (String(match.output.1), Int(match.output.2)!)
        } else {
            return (name, 1)
        }
    }
}

#if os(macOS)
@MainActor
func writeFile(viewModel: ViewModel, name: String, data: Data) {
    let panel = NSSavePanel()
    panel.level = NSWindow.Level.floating
    panel.title = String(localized: LocalizedStringResource(stringLiteral: "EXPORT"))
    panel.allowedContentTypes = [.json]
    panel.canCreateDirectories = true
    panel.isExtensionHidden = false
    panel.allowsOtherFileTypes = false
    panel.message = String(localized: LocalizedStringResource(stringLiteral: "EXPORT_MSG"))
    panel.nameFieldLabel = String(localized: LocalizedStringResource(stringLiteral: "FILENAME"))
    panel.nameFieldStringValue = "\(name).json"
    panel.begin { result in
        Task { @MainActor in
            if result == .OK, let file = panel.url {
                do {
                    try data.write(to: file, options: .atomicWrite)
                } catch {
                    viewModel.error = error
                }
            }
        }
    }
}

@MainActor
func readFile(viewModel: ViewModel, handler: @Sendable @escaping (Data, String) throws -> Void) {
    let panel = NSOpenPanel()
    panel.level = NSWindow.Level.floating
    panel.allowsMultipleSelection = false
    panel.canChooseDirectories = false
    panel.canChooseFiles = true
    panel.allowedContentTypes = [.json]
    panel.title = String(localized: LocalizedStringResource(stringLiteral: "IMPORT"))
    panel.message = String(localized: LocalizedStringResource(stringLiteral: "IMPORT_MSG"))
    panel.begin { result in
        Task { @MainActor in
            if result == .OK, let file = panel.url {
                do {
                    let data = try Data(contentsOf: file)
                    let name = file.lastPathComponent
                    let namePattern = /^([^\.]+)\.?.*$/
                    let prefixName = (try? namePattern.firstMatch(in: name)?.output.1).map { String($0) }
                    try handler(data, prefixName ?? name)
                } catch {
                    viewModel.error = error
                }
            }
        }
    }
}
#else
func read(file: URL) throws -> (name: String, data: Data) {
    let accessing = file.startAccessingSecurityScopedResource()
    defer {
        if accessing {
            file.stopAccessingSecurityScopedResource()
        }
    }
    let data = try Data(contentsOf: file)
    let nameComponent = file.lastPathComponent
    let namePattern = /^([^\.]+)\.?.*$/
    let name = try namePattern.firstMatch(in: nameComponent)?.output.1
    let actualName = if let name {
        String(name)
    } else {
        nameComponent
    }
    return (name: actualName, data: data)
}
#endif

struct ErrorAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel

    func body(content: Content) -> some View {
        content
            .alert("ERROR", isPresented: viewModel.binding(\.hasError)) {
                Button("OK", role: .cancel) { viewModel.error = nil }
            } message: {
                Text(viewModel.error?.localizedDescription ?? "")
            }
    }
}

extension View {
    func errorAlert() -> some View {
        self.modifier(ErrorAlert())
    }
}

// MARK: Modifiers - Private

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

private struct UpdateAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    @Binding var theme: ThemeData?

    func body(content: Content) -> some View {
        if let theme {
            content
                .alert(Text("UPDATE:\(theme.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.theme = nil }
                    Button("CONFIRM", role: .destructive) {
                        theme.theme = viewModel.watchLayout
                        self.theme = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func updateAlert(isPresented: Binding<Bool>, theme: Binding<ThemeData?>) -> some View {
        self.modifier(UpdateAlert(isPresented: isPresented, theme: theme))
    }
}

private struct DeleteAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var theme: ThemeData?

    func body(content: Content) -> some View {
        if let theme {
            content
                .alert(Text("DELETE:\(theme.nonNilName)"), isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) { self.theme = nil }
                    Button("CONFIRM", role: .destructive) {
                        modelContext.delete(theme)
                        self.theme = nil
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func deleteAlert(isPresented: Binding<Bool>, theme: Binding<ThemeData?>) -> some View {
        self.modifier(DeleteAlert(isPresented: isPresented, theme: theme))
    }
}

private struct RenameAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var theme: ThemeData?
    let existingNames: Set<String>
    @State private var newName = String(localized: "UNNAMED")

    func body(content: Content) -> some View {
        if let theme {
            content
                .onChange(of: isPresented, initial: true) {
                    if isPresented {
                        newName = validName(theme.name ?? newName, existingNames: existingNames)
                    }
                }
                .alert(Text("RENAME:\(theme.nonNilName)"), isPresented: $isPresented) {
                    TextField("NEW_NAME", text: $newName)
                        .labelsHidden()
                    Button("CANCEL", role: .cancel) { self.theme = nil }
                    Button("CONFIRM_NAME", role: .destructive) {
                        theme.name = newName
                        self.theme = nil
                    }
                    .disabled(existingNames.contains(newName))
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func renameAlert(isPresented: Binding<Bool>, theme: Binding<ThemeData?>, existingNames: [String]) -> some View {
        self.modifier(RenameAlert(isPresented: isPresented, theme: theme, existingNames: Set(existingNames)))
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
                        let newTheme = try ThemeData(viewModel.watchLayout, name: newName, deviceName: AppInfo.deviceName)
                        modelContext.insert(newTheme)
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
                        let layout = try WatchLayout(fromData: data)
                        let newName = validName(name, existingNames: existingNames)
                        let theme = try ThemeData(layout, name: newName, deviceName: AppInfo.deviceName)
                        modelContext.insert(theme)
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
    @Binding var theme: ThemeData?

    func body(content: Content) -> some View {
        if let theme {
            content
                .fileExporter(isPresented: $isPresented,
                              document: TextDocument(theme),
                              contentType: .json,
                              defaultFilename: "\(theme.nonNilName).json") { result in
                    if case .failure(let error) = result {
                        viewModel.error = error
                    }
                    self.theme = nil
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func exportAlert(isPresented: Binding<Bool>, theme: Binding<ThemeData?>) -> some View {
        self.modifier(ExportAlert(isPresented: isPresented, theme: theme))
    }
}
#endif

// MARK: Preview

#Preview("Themes", traits: .modifier(SampleData())) {
    NavigationStack {
        ThemesList()
    }
}
