//
//  Notification.swift
//  Chinendar
//
//  Created by Leo Liu on 1/5/25.
//

import UserNotifications

private struct NotificationTemplate {
    let id: String
    let title: String
    let body: String
    let time: Date
}

actor NotificationManager {
    static let shared = NotificationManager()

    func requestAuthorization() async throws -> Bool {
        let center = UNUserNotificationCenter.current()
        return try await center.requestAuthorization(options: [.alert, .sound])
    }

    var enabled: Bool {
        get async {
            let center = UNUserNotificationCenter.current()
            let settings = await center.notificationSettings()
            switch settings.authorizationStatus {
            case .denied, .notDetermined:
                return false
            case .authorized, .provisional, .ephemeral:
                return true
            @unknown default:
                return false
            }
        }
    }

    func addNotifications(chineseCalendar: ChineseCalendar) async throws {
        guard await enabled else { return }
        let center = UNUserNotificationCenter.current()
        let deleveredNotifications = await center.deliveredNotifications()
        let pendingNotifications = await center.pendingNotificationRequests()
        if !deleveredNotifications.isEmpty {
            center.removeAllDeliveredNotifications()
        }
        if !pendingNotifications.isEmpty {
            center.removeAllPendingNotificationRequests()
        }

        let modelContext = DataModel.shared.modelExecutor.modelContext
        let remindersList = try RemindersData.load(context: modelContext)

        var reminders: [Reminder] = []
        for list in remindersList where list.enabled {
            for reminder in list.reminders where reminder.enabled {
                reminders.append(reminder)
            }
        }

        var notifications: [NotificationTemplate] = []
        await withTaskGroup { (group: inout TaskGroup<NotificationTemplate?>) in
            for reminder in reminders {
                guard !group.isCancelled else { break }
                group.addTask {
                    if let eventTime = reminder.nextEvent(in: chineseCalendar), let triggerTime = reminder.nextReminder(in: chineseCalendar) {
                        let formatter = RelativeDateTimeFormatter()
                        formatter.dateTimeStyle = .named
                        let timeLeft = formatter.localizedString(for: eventTime, relativeTo: triggerTime)

                        let title = reminder.name
                        let body = if eventTime > .now {
                            String(localized: "EVENT\(reminder.name)HAPPEN_IN\(timeLeft)")
                        } else {
                            String(localized: "EVENT\(reminder.name)HAPPENED_ON\(timeLeft)")
                        }
                        if triggerTime.timeIntervalSinceNow > 14.4 {
                            return NotificationTemplate(id: reminder.id.uuidString, title: title, body: body, time: triggerTime)
                        }
                    }
                    return nil
                }
            }

            for await result in group {
                if let result {
                    notifications.append(result)
                }
            }
        }

        notifications.sort { $0.time < $1.time }
        var count = 0
        for notification in notifications {
            guard count < 64 else { break }
            do {
                let trigger = UNTimeIntervalNotificationTrigger(timeInterval: notification.time.timeIntervalSinceNow, repeats: false)
                let content = UNMutableNotificationContent()
                content.title = notification.title
                content.body = notification.body
                content.sound = .default
                let request = UNNotificationRequest(identifier: notification.id, content: content, trigger: trigger)
                try await center.add(request)
                count += 1
            } catch {
                print("Error when adding notification: \(error)")
                continue
            }
        }
    }

    private init() {}
}
