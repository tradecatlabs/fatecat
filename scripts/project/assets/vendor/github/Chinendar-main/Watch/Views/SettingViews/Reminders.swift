//
//  Reminders.swift
//  Chinendar
//
//  Created by Leo Liu on 12/30/24.
//

import SwiftUI
import SwiftData

struct RemindersSetting: View {
    @Query(filter: RemindersData.predicate, sort: \RemindersData.modifiedDate, order: .reverse) private var dataStack: [RemindersData]
    @Environment(\.modelContext) private var modelContext
    @Environment(ViewModel.self) private var viewModel
    @State private var errorMsg: Error?
    @State private var notificationEnabled: Bool = false
    let notificationManager = NotificationManager.shared

    private var hasError: Binding<Bool> {
        Binding<Bool>(get: { errorMsg != nil }, set: { if !$0 { errorMsg = nil } })
    }

    var body: some View {
        List {
            if !notificationEnabled {
                Section {
                    enableNotificationButton
                }
            }
            Section {
                ForEach(dataStack) { data in
                    if let list = data.list {
                        NavigationLink(value: data) {
                            ReminderListRow(list: list)
                        }
                    }
                }
            }
        }
        .alert("ERROR", isPresented: hasError) {
            Button("OK", role: .cancel) {}
        } message: {
            Text(errorMsg?.localizedDescription ?? "")
        }
        .task {
            notificationEnabled = await notificationManager.enabled
        }
        .onAppear {
            cleanup()
        }
        .navigationDestination(for: RemindersData.self) { reminderData in
            ReminderGroup(remindersData: reminderData)
        }
        .navigationTitle("REMINDERS_LIST")
    }

    var enableNotificationButton: some View {
        Button("ENABLE_NOTIFICATIONS") {
            Task {
                do {
                    notificationEnabled = try await notificationManager.requestAuthorization()
                    addDefault()
                    try await notificationManager.addNotifications(chineseCalendar: viewModel.chineseCalendar)
                } catch {
                    errorMsg = error
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .center)
    }

    private func addDefault() {
        let data = try! RemindersData(.defaultValue)
        modelContext.insert(data)
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
}

struct ReminderGroup: View {
    let remindersData: RemindersData

    var body: some View {
        Form {
            Section {
                Toggle("ENABLED", isOn: remindersData.binding(\.nonNilList.enabled))
            } header: {
                Text("GENERAL_REMINDER_INFO")
            }

            Section {
                ForEach(remindersData.binding(\.nonNilList.reminders)) { $reminder in
                    Toggle(isOn: $reminder.enabled) {
                        ReminderRow(reminder: reminder)
                    }
                    .toggleStyle(.button)
                    .buttonStyle(.plain)
                }
            } header: {
                Text("REMINDERS:\(remindersData.nonNilList.reminders.count)ITEMS")
            }
        }
        .navigationTitle(remindersData.nonNilList.name)
    }
}

struct ReminderListRow: View {
    let list: ReminderList

    var body: some View {
        HStack {
            Text(list.name)
                .lineLimit(2)
                .foregroundStyle(list.enabled ? .primary : .secondary)
            Spacer()
            Text("\(list.reminders.count)ITEMS")
                .foregroundStyle(.secondary)
        }
    }
}

struct ReminderRow: View {
    @Environment(ViewModel.self) private var viewModel
    let reminder: Reminder

    var body: some View {
        HStack {
            Text(reminder.name)
                .lineLimit(2)
                .foregroundStyle(reminder.enabled ? .primary : .secondary)
            Spacer()
            if let notifyTime = reminder.nextReminder(in: viewModel.chineseCalendar) {
                Text(notifyTime, format: .offset(to: .now, allowedFields: [.day]))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

#Preview("Reminders", traits: .modifier(SampleData())) {
    NavigationStack {
        RemindersSetting()
    }
}
