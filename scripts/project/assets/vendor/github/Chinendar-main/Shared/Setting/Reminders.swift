//
//  Reminders.swift
//  Chinendar
//
//  Created by Leo Liu on 12/25/24.
//

import SwiftUI
import SwiftData

struct RemindersSetting: View {
    @Query(filter: RemindersData.predicate, sort: \RemindersData.modifiedDate, order: .reverse) private var dataStack: [RemindersData]
    @Environment(\.modelContext) private var modelContext
    @Environment(ViewModel.self) private var viewModel
    private let notificationManager = NotificationManager.shared
    private var hasError: Binding<Bool> {
        Binding<Bool>(get: { errorMsg != nil }, set: { if !$0 { errorMsg = nil } })
    }
    @State private var errorMsg: Error?
    @State private var notificationEnabled = false
    @State private var showSaveNew = false
    @State private var showDelete = false
    @State private var showRename = false
#if os(iOS) || os(visionOS)
    @State private var showImport = false
    @State private var showExport = false
#endif
    @State private var target: RemindersData?

    var body: some View {
        Form {
            if !notificationEnabled {
                Section {
                    enableNotificationButton
                }
            }
            Section {
                if dataStack.isEmpty {
                    Text("EMPTY_LIST")
                        .foregroundStyle(.secondary)
                } else {
                    ForEach(dataStack) { group in
                        if group.list != nil {
                            NavigationLink(value: group) {
                                ReminderListRow(remindersData: group)
                            }
                            .contextMenu {
                                contextMenu(remindersData: group)
                                    .labelStyle(.titleAndIcon)
                            }
                        }
                    }
                }
            }
        }
        .formStyle(.grouped)
        .errorAlert()
        .newListAlert(isPresented: $showSaveNew, existingNames: dataStack.compactMap { $0.list?.name })
        .deleteListAlert(isPresented: $showDelete, target: $target)
        .renameListAlert(isPresented: $showRename, target: $target, existingNames: dataStack.compactMap { $0.list?.name })
#if os(iOS) || os(visionOS)
        .importAlert(isPresented: $showImport, existingNames: dataStack.compactMap { $0.list?.name })
        .exportAlert(isPresented: $showExport, reminders: $target)
#endif
        .task {
            notificationEnabled = await notificationManager.enabled
        }
        .alert("ERROR", isPresented: hasError) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMsg?.localizedDescription ?? "")
        }
        .onAppear {
            cleanup()
        }
        .toolbar {
#if os(macOS) || os(visionOS)
            ToolbarItemGroup {
                if dataStack.isEmpty {
                    addDefaultButton
                }
                importButton
                newListButton
            }
#else
            Menu {
                importButton
                newListButton
                if dataStack.isEmpty {
                    addDefaultButton
                }
            } label: {
                Label("MANAGE_LIST", systemImage: "ellipsis")
            }
#endif
        }
        .navigationDestination(for: RemindersData.self) { reminderData in
            ReminderGroup(remindersData: reminderData)
        }
        .navigationTitle("REMINDERS_LIST")
#if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
#endif
    }

    var newListButton: some View {
        Button {
            showSaveNew = true
        } label: {
            Label("SAVE_NEW", systemImage: "plus")
        }
    }

    var importButton: some View {
        Button {
#if os(macOS)
            readFile(viewModel: viewModel) { data, _ in
                Task { @MainActor in
                    var list = try ReminderList(fromData: data)
                    list.name = validName(list.name, existingNames: Set(dataStack.compactMap({ $0.list?.name })))
                    let remindersData = try RemindersData(list)
                    modelContext.insert(remindersData)
                }
            }
#else
            showImport = true
#endif
        } label: {
            Label("IMPORT", systemImage: "square.and.arrow.down")
        }
    }

    var addDefaultButton: some View {
        Button { addDefault() } label: {
            Label("ADD_DEFAULT", systemImage: "rectangle.stack.badge.plus")
        }
    }

    var enableNotificationButton: some View {
        Button("ENABLE_NOTIFICATIONS") {
            Task {
                do {
                    notificationEnabled = try await notificationManager.requestAuthorization()
                } catch {
                    errorMsg = error
                }
            }
            addDefault()
        }
        .frame(maxWidth: .infinity, alignment: .center)
#if os(iOS) || os(macOS)
        .buttonStyle(.plain)
#elseif os(visionOS)
        .buttonStyle(.automatic)
#endif
    }

    private func addDefault() {
        if dataStack.isEmpty {
            let data = try! RemindersData(.defaultValue)
            data.modifiedDate = .distantPast
            modelContext.insert(data)
        }
    }

    private func cleanup() {
        var records = Set<String>()
        for data in dataStack {
            if data.isNil {
                modelContext.delete(data)
            } else {
                if records.contains(data.list!.name) {
                    modelContext.delete(data)
                } else {
                    records.insert(data.list!.name)
                }
            }
        }
    }

    @ViewBuilder func contextMenu(remindersData: RemindersData) -> some View {
        Button {
            target = remindersData
            showRename = true
        } label: {
            Label("RENAME", systemImage: "rectangle.and.pencil.and.ellipsis")
        }
        Button {
#if os(iOS) || os(visionOS)
            target = remindersData
            showExport = true
#else
            if let data = try? remindersData.list?.encode(), let name = remindersData.list?.name {
                writeFile(viewModel: viewModel, name: name, data: data)
            } else {
                print("Writing to file failed")
            }
#endif
        } label: {
            Label("EXPORT", systemImage: "square.and.arrow.up")
        }
        Button(role: .destructive) {
            target = remindersData
            showDelete = true
        } label: {
            Label("DELETE_GROUP", systemImage: "trash")
        }
    }
}

struct ReminderGroup: View {
    var remindersData: RemindersData
    @Environment(\.modelContext) private var modelContext
    @Environment(ViewModel.self) private var viewModel
#if os(iOS) || os(visionOS)
    @Environment(\.editMode) private var editMode
#else
    @State private var editing = false
#endif
    @State private var selectedReminder = Set<UUID>()
    @State private var showGroupDeletion = false
    @State private var showSelectionDeletion = false
    @State private var targetIDs = Set<UUID>()
    @State private var showSelectionMove = false
    @State private var showBulkEdit = false
    @State private var showNewReminder = false
    @State private var showRename = false
    @State private var showExport = false

    @ViewBuilder var editingView: some View {
        if let list = remindersData.list {
            List(selection: $selectedReminder) {
                ForEach(list.reminders) { reminder in
                    ReminderRow(reminder: reminder)
#if os(macOS)
                    .padding(.vertical, 5)
#endif
                }
                .onMove { from, to in
                    remindersData.list?.reminders.move(fromOffsets: from, toOffset: to)
                }
                .onDelete { index in
                    targetIDs = Set(list.reminders.find(indices: index).map(\.id))
                    showSelectionDeletion = true
                }
            }
            .toolbar {
#if os(macOS) || os(visionOS)
                ToolbarItem(placement: .primaryAction) {
                    deleteSelectedButton
                }
                ToolbarItemGroup(placement: .primaryAction) {
                    editButton
                    moveSelectedButton
                }
#else
                ToolbarItem(placement: .primaryAction) {
                    editButton
                }
                ToolbarItem(placement: .primaryAction) {
                    Menu {
                        moveSelectedButton
                        deleteSelectedButton
                    } label: {
                        Label("MANAGE_LIST", systemImage: "ellipsis")
                    }
                }
#endif
            }
            .deleteReminderAlert(isPresented: $showSelectionDeletion, remindersID: $targetIDs, in: remindersData)
            .listSelector(isPresent: $showSelectionMove, reminderIDs: $targetIDs, in: remindersData)
            .navigationTitle(list.name)
        }
    }

    @ViewBuilder var navigationView: some View {
        if let list = remindersData.list {
            Form {
                Section {
                    TextField("REMINDER_NAME", text: remindersData.binding(\RemindersData.nonNilList.name))
                    Toggle("ENABLED", isOn: remindersData.binding(\RemindersData.nonNilList.enabled))
                } header: {
                    Text("GENERAL_REMINDER_INFO")
                }
                Section {
                    ForEach(list.reminders) { reminder in
                        NavigationLink(value: reminder) {
                            ReminderRow(reminder: reminder)
                        }
                        .contextMenu {
                            contextMenu(reminder: reminder)
                                .labelStyle(.titleAndIcon)
                        }
                    }
                } header: {
                    Text("REMINDERS:\(list.reminders.count)ITEMS")
                }
            }
            .formStyle(.grouped)
            .deleteListAlert(isPresented: $showGroupDeletion, target: Binding<RemindersData?>(get: { remindersData }, set: {_ in })) {
                if !viewModel.settings.path.isEmpty {
                    viewModel.settings.path.removeLast()
                }
            }
            .bulkEdit(isPresented: $showBulkEdit, for: remindersData)
            .deleteReminderAlert(isPresented: $showSelectionDeletion, remindersID: $targetIDs, in: remindersData)
            .listSelector(isPresent: $showSelectionMove, reminderIDs: $targetIDs, in: remindersData)
            .renameReminderAlert(isPresented: $showRename, remindersData: remindersData, targetIDs: $targetIDs)
            .newReminderAlert(isPresented: $showNewReminder, in: remindersData, existingNames: remindersData.list?.reminders.map(\.name) ?? [])
#if os(iOS) || os(visionOS)
            .exportAlert(isPresented: $showExport, reminders: Binding(get: { remindersData }, set: {_ in }))
#endif
            .toolbar {
#if os(macOS) || os(visionOS)
                ToolbarItem(placement: .primaryAction) {
                    deleteGroupButton
                }
                ToolbarItemGroup(placement: .primaryAction) {
                    exportButton
                    bulkEditButton
                    editButton
                }
                ToolbarItem(placement: .primaryAction) {
                    newButton
                }
#else
                ToolbarItem(placement: .primaryAction) {
                    editButton
                }
                ToolbarItem(placement: .primaryAction) {
                    Menu {
                        newButton
                        bulkEditButton
                        exportButton
                        deleteGroupButton
                    } label: {
                        Label("MANAGE_LIST", systemImage: "ellipsis")
                    }
                }
#endif
            }
            .navigationTitle(list.name)
        }
    }

    var body: some View {
#if os(iOS) || os(visionOS)
        let editing = editMode?.wrappedValue.isEditing ?? false
#endif

        if editing {
#if os(macOS)
            Form {
                editingView
            }
            .formStyle(.grouped)
#else
            editingView
#endif
        } else {
            navigationView
                .navigationDestination(for: Reminder.self) { reminder in
                    ReminderConfig(remindersData: remindersData, reminderID: reminder.id)
                }
        }
    }

    var editButton: some View {
#if os(iOS) || os(visionOS)
        EditButton()
#else
        Button {
            editing.toggle()
        } label: {
            if editing {
                Label("DONE_EDITING", systemImage: "checklist.unchecked")
            } else {
                Label("EDIT", systemImage: "checklist")
            }
        }
#endif
    }

    var newButton: some View {
        Button {
            showNewReminder = true
        } label: {
            Label("CREATE_NEW", systemImage: "plus")
        }
    }

    var moveSelectedButton: some View {
        Button {
            targetIDs = selectedReminder
            showSelectionMove = true
        } label: {
            Label("MOVE_TO", systemImage: "folder")
        }
        .disabled(selectedReminder.isEmpty)
    }

    var bulkEditButton: some View {
        Button {
            showBulkEdit = true
        } label: {
            Label("BULK_EDIT", systemImage: "checkmark.rectangle.stack")
        }
    }

    var deleteGroupButton: some View {
        Button(role: .destructive) {
            showGroupDeletion = true
        } label: {
            Label("DELETE_GROUP", systemImage: "trash")
        }
    }

    var deleteSelectedButton: some View {
        Button(role: .destructive) {
            targetIDs = selectedReminder
            showSelectionDeletion = true
        } label: {
            Label("DELETE_SELECTED", systemImage: "trash")
        }
        .disabled(selectedReminder.isEmpty)
    }

    var exportButton: some View {
        Button {
#if os(iOS) || os(visionOS)
            showExport = true
#else
            if let data = try? remindersData.list?.encode(), let name = remindersData.list?.name {
                writeFile(viewModel: viewModel, name: name, data: data)
            } else {
                print("Writing to file failed")
            }
#endif
        } label: {
            Label("EXPORT", systemImage: "square.and.arrow.up")
        }
    }

    @ViewBuilder func contextMenu(reminder: Reminder) -> some View {
        Button {
            targetIDs = [reminder.id]
            showRename = true
        } label: {
            Label("RENAME", systemImage: "rectangle.and.pencil.and.ellipsis")
        }
        Button {
            targetIDs = [reminder.id]
            showSelectionMove = true
        } label: {
            Label("MOVE_TO", systemImage: "folder")
        }
        Button(role: .destructive) {
            targetIDs = [reminder.id]
            showSelectionDeletion = true
        } label: {
            Label("DELETE", systemImage: "trash")
        }
    }
}

struct ReminderConfig: View {
    let remindersData: RemindersData
    let reminderID: UUID
    @Environment(ViewModel.self) private var viewModel
    @State private var showDelete = false
    @State private var showMove = false

    var body: some View {
        if let reminderIndex = remindersData.list?.reminders.firstIndex(where: { $0.id == reminderID }) {
            let reminder = remindersData.list!.reminders[reminderIndex]
            let reminderModel = ReminderModel(reminder: remindersData.binding(\.nonNilList.reminders[reminderIndex]), chineseCalendar: viewModel.chineseCalendar)
            Form {
                Section {
                    TextField("REMINDER_NAME", text: remindersData.binding(\.nonNilList.reminders[reminderIndex].name))
                    Toggle("ENABLED", isOn: remindersData.binding(\.nonNilList.reminders[reminderIndex].enabled))
                } header: {
                    Text("GENERAL_REMINDER_INFO")
                }

                Section {
                    EventTypeSetting(reminderModel: reminderModel)
                } header: {
                    if let nextTime = reminder.nextEvent(in: viewModel.chineseCalendar) {
                        Text("EVENT_TIME: \(Text(nextTime, format: .relative(presentation: .named, unitsStyle: .abbreviated)))")
                    } else {
                        Text("EVENT_TIME")
                    }
                }

                Section {
                    RemindTypeSetting(reminderModel: reminderModel)
                } header: {
                    if let nextTime = reminder.nextReminder(in: viewModel.chineseCalendar) {
                        Text("REMIND_TIME: \(Text(nextTime, format: .relative(presentation: .named, unitsStyle: .abbreviated)))")
                    } else {
                        Text("REMIND_TIME")
                    }
                }
            }
            .formStyle(.grouped)
            .listSelector(isPresent: $showMove, reminderIDs: Binding(get: { Set([reminderID]) }, set: {_ in }), in: remindersData)
            .deleteReminderAlert(isPresented: $showDelete, remindersID: Binding(get: { Set([reminderID]) }, set: {_ in }), in: remindersData) {
                if !viewModel.settings.path.isEmpty {
                    viewModel.settings.path.removeLast()
                }
            }
            .toolbar {
#if os(macOS) || os(visionOS)
                ToolbarItem(placement: .primaryAction) {
                    deleteButton
                }
                ToolbarItem(placement: .primaryAction) {
                    moveButton
                }
#else
                ToolbarItem(placement: .primaryAction) {
                    Menu {
                        moveButton
                        deleteButton
                    } label: {
                        Label("MANAGE_LIST", systemImage: "ellipsis")
                    }
                }
#endif
            }
            .navigationTitle(reminder.name)
        }
    }

    var deleteButton: some View {
        Button(role: .destructive) {
            showDelete = true
        } label: {
            Label("DELETE", systemImage: "trash")
        }
    }

    var moveButton: some View {
        Button {
            showMove = true
        } label: {
            Label("MOVE_TO", systemImage: "folder")
        }
    }
}

struct ReminderRow: View {
    @Environment(ViewModel.self) private var viewModel
    let reminder: Reminder

    var body: some View {
        HStack {
            Text(reminder.name)
                .lineLimit(1)
                .foregroundStyle(reminder.enabled ? .primary : .secondary)
            Spacer()
            if let notifyTime = reminder.nextReminder(in: viewModel.chineseCalendar) {
                Text(notifyTime, format: .offset(to: .now, allowedFields: [.day]))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

struct ReminderListRow: View {
    @Environment(ViewModel.self) private var viewModel
    let remindersData: RemindersData

    var body: some View {
        if let list = remindersData.list {
            HStack {
                Text(list.name)
                    .lineLimit(1)
                    .foregroundStyle(list.enabled ? .primary : .secondary)
                Spacer()
                Text("\(list.reminders.count)ITEMS")
                    .foregroundStyle(.secondary)
            }
        }
    }
}

// MARK: Modifiers - Private

private struct ReminderListSelector: ViewModifier {
    @Query(filter: RemindersData.predicate, sort: \RemindersData.modifiedDate, order: .reverse) private var dataStack: [RemindersData]
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresent: Bool
    let remindersData: RemindersData
    @Binding var reminderIDs: Set<UUID>
    @State private var showConfirmation = false
    @State private var showNewConfirmation = false
    @State private var targetData: RemindersData?
    @State private var newName: String = ""

    func body(content: Content) -> some View {
        content
            .sheet(isPresented: $isPresent) {
                body
                    .presentationSizing(.form)
            }
    }

    @ViewBuilder var body: some View {
#if os(macOS)
        let content = Form {
            selectionPanel
                .buttonStyle(.plain)
        }
        .formStyle(.grouped)
#else
        let content = List {
            selectionPanel
        }
            .navigationBarTitleDisplayMode(.inline)
#endif
        NavigationStack {
            content
                .toolbar {
                    cancelButton
                }
                .navigationTitle("MOVE_TO")
        }
    }

    @ViewBuilder var selectionPanel: some View {
        ForEach(dataStack) { group in
            if let list = group.list {
                Button {
                    targetData = group
                    showConfirmation = true
                } label: {
                    HStack {
                        Text(list.name)
                            .lineLimit(1)
                        Spacer()
                        Text("\(list.reminders.count)ITEMS")
                            .foregroundStyle(.secondary)
                    }
                }
                .disabled(group.persistentModelID == remindersData.persistentModelID)
            }
        }
        .alert("MOVE_TO", isPresented: $showConfirmation) {
            Button("CANCEL", role: .cancel) {
                targetData = nil
            }
            Button("CONFIRM", role: .destructive) {
                targetData?.list?.reminders.append(contentsOf: move())
                isPresent = false
                targetData = nil
            }
        } message: {
            if let data = targetData?.list {
                Text("MOVE:\(reminderIDs.count)TO:\(data.name)")
            } else {
                Text("ERROR")
            }
        }
        Button {
            newName = validName(String(localized: "UNNAMED"), existingNames: Set(dataStack.compactMap { $0.list?.name }))
            showNewConfirmation = true
        } label: {
            Label("CREATE_NEW", systemImage: "plus")
                .frame(maxWidth: .infinity, alignment: .center)
        }
        .alert("MOVE_TO", isPresented: $showNewConfirmation) {
            TextField("NEW_NAME", text: $newName)
                .labelsHidden()
            Button("CANCEL", role: .cancel) {
                targetData = nil
            }
            Button("CONFIRM", role: .destructive) {
                let movedReminders = move()
                if !movedReminders.isEmpty {
                    do {
                        let newList = ReminderList(name: newName, enabled: false, reminders: movedReminders)
                        let newData = try RemindersData(newList)
                        modelContext.insert(newData)
                    } catch {
                        viewModel.error = error
                    }
                }
                isPresent = false
                targetData = nil
            }
        } message: {
            Text("MOVE:\(reminderIDs.count)TO:\(newName)")
        }
    }

    var cancelButton: some View {
        Button {
            isPresent = false
            reminderIDs = []
        } label: {
            Text("CANCEL")
        }
    }

    func move() -> [Reminder] {
        if let list = remindersData.list {
            let movedIndicies = IndexSet(list.reminders.enumerated().filter { _, element in
                reminderIDs.contains(element.id)
            }.map { $0.offset })
            let movedReminders = list.reminders.find(indices: movedIndicies)
            remindersData.list?.reminders.remove(atOffsets: movedIndicies)
            return Array(movedReminders)
        } else {
            return []
        }
    }
}

fileprivate extension View {
    func listSelector(isPresent: Binding<Bool>, reminderIDs: Binding<Set<UUID>>, in remindersData: RemindersData) -> some View {
        self.modifier(ReminderListSelector(isPresent: isPresent, remindersData: remindersData, reminderIDs: reminderIDs))
    }
}

private struct ReminderListBulkEdit: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    let remindersData: RemindersData

    @State private var showConfirmation = false
    @State private var reminder = Reminder(name: "", enabled: false, targetTime: .event(.solarTerm(0)), remindTime: .exact)
    private var reminderModel: ReminderModel {
        ReminderModel(reminder: $reminder, chineseCalendar: viewModel.chineseCalendar)
    }

    func body(content: Content) -> some View {
        content
            .sheet(isPresented: $isPresented) {
                body
                    .presentationSizing(.form)
            }
    }

    var cancelButton: some View {
        Button {
            isPresented = false
        } label: {
            Text("CANCEL")
        }
    }

    @ViewBuilder var body: some View {
        if let list = remindersData.list {
            NavigationStack {
                Form {
                    Section {
                        RemindTypeSetting(reminderModel: reminderModel)
                    } header: {
                        Text("REMIND_TIME")
                    }

                    Section {
                        Button {
                            showConfirmation = true
                        } label: {
                            Label("APPLY_TO_ALL", systemImage: "checkmark.rectangle.stack.fill")
                        }
                        .frame(maxWidth: .infinity, alignment: .center)
                    }
                }
#if os(macOS)
                .formStyle(.grouped)
#else
                .navigationBarTitleDisplayMode(.inline)
#endif
                .alert("APPLY_TO_ALL", isPresented: $showConfirmation) {
                    Button("CANCEL", role: .cancel) {}
                    Button("CONFIRM", role: .destructive) {
                        for index in 0..<list.reminders.count {
                            remindersData.list?.reminders[index].remindTime = reminder.remindTime
                        }
                        isPresented = false
                    }
                } message: {
                    Text("APPLY_TO\(list.reminders.count)ITEMS_IN\(list.name)")
                }
                .toolbar {
                    cancelButton
                }
                .navigationTitle("BULK_EDIT")
            }
        }
    }
}

fileprivate extension View {
    func bulkEdit(isPresented: Binding<Bool>, for remindersData: RemindersData) -> some View {
        self.modifier(ReminderListBulkEdit(isPresented: isPresented, remindersData: remindersData))
    }
}

private struct DeleteReminderAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var targets: Set<UUID>
    let remindersData: RemindersData
    let postAction: (() -> Void)?

    func body(content: Content) -> some View {
        if let indices = remindersData.list?.reminders.enumerated().filter({ _, element in
            targets.contains(element.id)
        }).map({ $0.offset }), !indices.isEmpty {
            content
                .alert("DELETE_FROM:\(remindersData.list!.name)", isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) {
                        self.targets = []
                    }
                    Button("CONFIRM", role: .destructive) {
                        remindersData.list!.reminders.remove(atOffsets: IndexSet(indices))
                        self.targets = []
                        if let postAction {
                            postAction()
                        }
                    }
                } message: {
                    if indices.count == 1 {
                        Text("DELETE:\(remindersData.list!.reminders[indices.first!].name)")
                    } else {
                        Text("DELETE\(indices.count)ITEMS")
                    }
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func deleteReminderAlert(isPresented: Binding<Bool>, remindersID: Binding<Set<UUID>>, in remindersData: RemindersData, postAction: (() -> Void)? = nil) -> some View {
        self.modifier(DeleteReminderAlert(isPresented: isPresented, targets: remindersID, remindersData: remindersData, postAction: postAction))
    }
}

private struct NewReminderAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Binding var isPresented: Bool
    let remindersData: RemindersData
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
                    let newReminder = Reminder(
                        name: newName, enabled: false,
                        targetTime: .chinendar(viewModel.chineseCalendar.chineseDateTime),
                        remindTime: .exact
                    )
                    remindersData.list?.reminders.insert(newReminder, at: 0)
                }
                .disabled(existingNames.contains(newName))
            }
    }
}

fileprivate extension View {
    func newReminderAlert(isPresented: Binding<Bool>, in remindersData: RemindersData, existingNames: [String]) -> some View {
        self.modifier(NewReminderAlert(isPresented: isPresented, remindersData: remindersData, existingNames: Set(existingNames)))
    }
}

private struct RenameReminderAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    let remindersData: RemindersData
    @Binding var targetIDs: Set<UUID>
    @State private var newName = String(localized: "UNNAMED")

    func body(content: Content) -> some View {
        if let list = remindersData.list, !targetIDs.isEmpty {
            let indices = list.reminders.enumerated().filter({ targetIDs.contains($0.element.id) }).map({ $0.offset })
            let title = if indices.count == 1 {
                Text("RENAME:\(list.reminders[indices[0]].name)")
            } else {
                Text("RENAME\(indices.count)ITEMS")
            }
            content
                .onChange(of: isPresented, initial: true) {
                    if isPresented {
                        let name = if indices.count == 1 {
                            list.reminders[indices[0]].name
                        } else {
                            newName
                        }
                        newName = validName(name, existingNames: Set(list.reminders.map(\.name)))
                    }
                }
                .alert(title, isPresented: $isPresented) {
                    TextField("NEW_NAME", text: $newName)
                        .labelsHidden()
                    Button("CANCEL", role: .cancel) {
                        self.targetIDs = []
                    }
                    Button("CONFIRM_NAME", role: .destructive) {
                        for index in indices {
                            remindersData.list?.reminders[index].name = newName
                        }
                        self.targetIDs = []
                    }
                    .disabled(Set(list.reminders.map(\.name)).contains(newName))
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func renameReminderAlert(isPresented: Binding<Bool>, remindersData: RemindersData, targetIDs: Binding<Set<UUID>>) -> some View {
        self.modifier(RenameReminderAlert(isPresented: isPresented, remindersData: remindersData, targetIDs: targetIDs))
    }
}

private struct DeleteListAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var target: RemindersData?
    let postAction: (() -> Void)?

    func body(content: Content) -> some View {
        if let list = target?.list {
            content
                .alert("DELETE:\(list.name)", isPresented: $isPresented) {
                    Button("CANCEL", role: .cancel) {
                        self.target = nil
                    }
                    Button("CONFIRM", role: .destructive) {
                        modelContext.delete(target!)
                        self.target = nil
                        if let postAction {
                            postAction()
                        }
                    }
                } message: {
                    Text("DELETE\(list.reminders.count)ITEMS")
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func deleteListAlert(isPresented: Binding<Bool>, target: Binding<RemindersData?>, postAction: (() -> Void)? = nil) -> some View {
        self.modifier(DeleteListAlert(isPresented: isPresented, target: target, postAction: postAction))
    }
}

private struct NewListAlert: ViewModifier {
    @Environment(ViewModel.self) private var viewModel
    @Environment(\.modelContext) private var modelContext
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
                        let newReminderList = ReminderList(name: newName, enabled: false, reminders: [])
                        let newRemindersData = try RemindersData(newReminderList)
                        modelContext.insert(newRemindersData)
                    } catch {
                        viewModel.error = error
                    }
                }
                .disabled(existingNames.contains(newName))
            }
    }
}

fileprivate extension View {
    func newListAlert(isPresented: Binding<Bool>, existingNames: [String]) -> some View {
        self.modifier(NewListAlert(isPresented: isPresented, existingNames: Set(existingNames)))
    }
}

private struct RenameListAlert: ViewModifier {
    @Environment(\.modelContext) private var modelContext
    @Binding var isPresented: Bool
    @Binding var target: RemindersData?
    let existingNames: Set<String>
    @State private var newName = String(localized: "UNNAMED")

    func body(content: Content) -> some View {
        if let list = target?.list {
            content
                .onChange(of: isPresented, initial: true) {
                    if isPresented {
                        newName = validName(target?.list?.name ?? newName, existingNames: existingNames)
                    }
                }
                .alert(Text("RENAME:\(list.name)"), isPresented: $isPresented) {
                    TextField("NEW_NAME", text: $newName)
                        .labelsHidden()
                    Button("CANCEL", role: .cancel) {}
                    Button("CONFIRM_NAME", role: .destructive) {
                        target?.list?.name = newName
                    }
                    .disabled(existingNames.contains(newName))
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func renameListAlert(isPresented: Binding<Bool>, target: Binding<RemindersData?>, existingNames: [String]) -> some View {
        self.modifier(RenameListAlert(isPresented: isPresented, target: target, existingNames: Set(existingNames)))
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
                        var reminderList = try ReminderList(fromData: data)
                        reminderList.name = validName(name, existingNames: existingNames)
                        let remindersData = try RemindersData(reminderList)
                        modelContext.insert(remindersData)
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
    @Binding var remindersData: RemindersData?

    func body(content: Content) -> some View {
        if let remindersData {
            content
                .fileExporter(isPresented: $isPresented,
                              document: TextDocument(remindersData),
                              contentType: .json,
                              defaultFilename: "\(remindersData.nonNilList.name).json") { result in
                    if case .failure(let error) = result {
                        viewModel.error = error
                    }
                    self.remindersData = nil
                }
        } else {
            content
        }
    }
}

fileprivate extension View {
    func exportAlert(isPresented: Binding<Bool>, reminders: Binding<RemindersData?>) -> some View {
        self.modifier(ExportAlert(isPresented: isPresented, remindersData: reminders))
    }
}
#endif

// MARK: Internal Model and Views - Private

private enum TargetType: CaseIterable {
    case chinendar, event
}
private enum RemindType: CaseIterable {
    case exact, timeInDay, quarterOffset
}

@MainActor
private final class ReminderModel: Bindable {
    var reminder: Binding<Reminder>
    var chineseCalendar: ChineseCalendar
    var chineseDate: ChineseCalendar.ChineseDateTime {
        didSet {
            reminder.wrappedValue.targetTime = .chinendar(chineseDate)
        }
    }
    var solarTerm: Int {
        didSet {
            reminder.wrappedValue.targetTime = .event(.solarTerm(solarTerm))
        }
    }
    var dayOffset: Int {
        didSet {
            reminder.wrappedValue.remindTime = .timeInDay(-dayOffset, timeInDay)
        }
    }
    var timeInDay: ChineseCalendar.ChineseTime {
        didSet {
            reminder.wrappedValue.remindTime = .timeInDay(-dayOffset, timeInDay)
        }
    }
    var quarterOffset: Int {
        didSet {
            reminder.wrappedValue.remindTime = .quarterOffset(-quarterOffset)
        }
    }

    var targetType: TargetType {
        get {
            switch reminder.wrappedValue.targetTime {
            case .chinendar:
                TargetType.chinendar
            case .event:
                TargetType.event
            }
        } set {
            switch newValue {
            case .chinendar:
                reminder.wrappedValue.targetTime = .chinendar(chineseDate)
            case .event:
                reminder.wrappedValue.targetTime = .event(.solarTerm(solarTerm))
            }
        }
    }

    var remindType: RemindType {
        get {
            switch reminder.wrappedValue.remindTime {
            case .exact:
                RemindType.exact
            case .timeInDay:
                RemindType.timeInDay
            case .quarterOffset:
                RemindType.quarterOffset
            }
        } set {
            switch newValue {
            case .exact:
                reminder.wrappedValue.remindTime = .exact
            case .timeInDay:
                reminder.wrappedValue.remindTime = .timeInDay(-dayOffset, timeInDay)
            case .quarterOffset:
                reminder.wrappedValue.remindTime = .quarterOffset(-quarterOffset)
            }
        }
    }

    var targetCalendar: ChineseCalendar {
        get {
            var calendar = chineseCalendar
            if let newDate = calendar.findNext(chineseDateTime: chineseDate) {
                calendar.update(time: newDate)
            }
            return calendar
        } set {
            chineseDate = newValue.chineseDateTime
        }
    }

    var timeInDayCalendar: ChineseCalendar {
        get {
            var calendar = chineseCalendar
            if let newDate = calendar.find(chineseTime: timeInDay) {
                calendar.update(time: newDate)
            }
            return calendar
        } set {
            timeInDay = newValue.chineseTime
        }
    }

    init(reminder: Binding<Reminder>, chineseCalendar: ChineseCalendar) {
        switch reminder.wrappedValue.targetTime {
        case .chinendar(let date):
            chineseDate = date
            solarTerm = 0
        case .event(.solarTerm(let term)):
            chineseDate = chineseCalendar.chineseDateTime
            solarTerm = term
        }

        switch reminder.wrappedValue.remindTime {
        case .exact:
            self.dayOffset = 0
            self.timeInDay = .init()
            self.quarterOffset = 0
        case .timeInDay(let dayOffset, let time):
            self.dayOffset = -dayOffset
            self.timeInDay = time
            self.quarterOffset = 0
        case .quarterOffset(let quarterOffset):
            self.dayOffset = 0
            self.timeInDay = .init()
            self.quarterOffset = -quarterOffset
        }

        self.reminder = reminder
        self.chineseCalendar = chineseCalendar
    }
}

private struct RemindTypeSetting: View {
    let reminderModel: ReminderModel

    var body: some View {
        Picker("REMIND_TYPE", selection: reminderModel.binding(\.remindType)) {
            ForEach(RemindType.allCases, id: \.self) { type in
                switch type {
                case .exact:
                    Text("REMIND_EXACT")
                case .timeInDay:
                    Text("REMIND_SPECIFIC_TIME")
                case .quarterOffset:
                    Text("REMIND_QUARTER_OFFSET")
                }
            }
        }
        switch reminderModel.remindType {
        case .exact:
            EmptyView()
        case .timeInDay:
            HStack {
                Stepper("REMINDER_DAY_OFFSET", value: reminderModel.binding(\.dayOffset), in: 0...15, step: 1)
                Text("\(reminderModel.dayOffset)DAYS")
            }
            HStack {
                Text("TIME")
                    .lineLimit(1)
                ChinendarTimePicker(chineseCalendar: reminderModel.binding(\.timeInDayCalendar))
                    .buttonStyle(.bordered)
            }
        case .quarterOffset:
            HStack {
                Stepper("REMINDER_QUARTER_OFFSET", value: reminderModel.binding(\.quarterOffset), in: 0...100, step: 1)
                Text("\(reminderModel.quarterOffset)QUARTERS")
            }
        }
    }
}

private struct EventTypeSetting: View {
    let reminderModel: ReminderModel

    var body: some View {
        Picker("EVENT_TYPE", selection: reminderModel.binding(\.targetType)) {
            ForEach(TargetType.allCases, id: \.self) { type in
                switch type {
                case .chinendar:
                    Text("CHINENDAR_DATETIME")
                case .event:
                    Text("ST")
                }
            }
        }
        switch reminderModel.targetType {
        case .chinendar:
            HStack {
                Text("DATE")
                    .lineLimit(1)
                ChinendarDatePicker(chineseCalendar: reminderModel.binding(\.targetCalendar))
                Spacer(minLength: 0)
                    .frame(idealWidth: 10, maxWidth: 20)
                Text("TIME")
                    .lineLimit(1)
                ChinendarTimePicker(chineseCalendar: reminderModel.binding(\.targetCalendar))
            }
            .buttonStyle(.bordered)
        case .event:
            Picker("ST", selection: reminderModel.binding(\.solarTerm)) {
                ForEach(0..<24, id: \.self) { solarterm in
                    Text(ChineseCalendar.solarTermName(for: solarterm)!)
                }
            }
        }
    }
}

#if os(macOS)
private struct BackButton: View {
    @Environment(ViewModel.self) private var viewModel

    var body: some View {
        Button {
            if !viewModel.settings.path.isEmpty {
                viewModel.settings.path.removeLast()
            }
        } label: {
            Image(systemName: "chevron.left")
        }
    }
}
#endif

// MARK: Preview

#Preview("Reminders", traits: .modifier(SampleData())) {
    NavigationStack {
        RemindersSetting()
    }
}
