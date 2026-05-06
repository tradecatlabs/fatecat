//
//  DataModel.swift
//  Chinendar
//
//  Created by Leo Liu on 7/7/23.
//
//

import Foundation
import SwiftData
import CoreData
#if os(macOS)
import SystemConfiguration
#elseif os(iOS)
import UIKit
#elseif os(watchOS)
import WatchKit
#elseif os(visionOS)
import VisionKit
#endif

private func intVersion(_ version: Schema.Version) -> Int {
    version.major * 100_0000 + version.minor * 1_0000 + version.patch * 100 + 1
}

private func createContainer(schema: Schema, migrationPlan: SchemaMigrationPlan.Type? = nil, configurations: [ModelConfiguration]) -> ModelContainer {
    do {
        return try ModelContainer(for: schema, migrationPlan: migrationPlan, configurations: configurations)
    } catch {
        print(error.localizedDescription)
        do {
            return try ModelContainer(for: schema, configurations: configurations)
        } catch {
            fatalError(error.localizedDescription)
        }
    }
}

struct AppInfo {
#if os(macOS)
    static let deviceName = SCDynamicStoreCopyComputerName(nil, nil).map { String($0) } ?? "Mac"
#elseif os(iOS) || os(visionOS)
    @MainActor static let deviceName = UIDevice.current.name
#elseif os(watchOS)
    static let deviceName = WKInterfaceDevice.current().name
#endif
    static let defaultName = String(localized: "__factory_default_name__")
}

@ModelActor
actor DataModel {
    static let shared = DataModel(modelContainer: DataSchema.container)
}

typealias DataSchema = DataSchemaV7
extension DataSchema {
    static let container = {
        let fullSchema = Schema(versionedSchema: DataSchema.self)
#if DEBUG
        let modelConfig = ModelConfiguration("MainData-debug", schema: fullSchema, groupContainer: .automatic, cloudKitDatabase: .none)
#else
        let modelConfig = ModelConfiguration("MainData", schema: fullSchema, groupContainer: .automatic, cloudKitDatabase: .automatic)
#endif
        return createContainer(schema: fullSchema, migrationPlan: DataMigrationPlan.self, configurations: [modelConfig])
    }()
}

typealias ThemeData = DataSchema.Theme
extension ThemeData {
    static let version = intVersion(DataSchema.versionIdentifier)
    static let predicate = #Predicate<ThemeData> { entry in
        entry.data != nil
    }

    var isNil: Bool {
        return data == nil || name == nil || deviceName == nil || modifiedDate == nil
    }

    var theme: WatchLayout? {
        get {
            let decoder = JSONDecoder()
            do {
                if let data {
                    return try decoder.decode(WatchLayout.self, from: data)
                } else {
                    return nil
                }
            } catch {
                print("Unable to decode watch layout \(error)")
                return nil
            }
        } set {
            do {
                let encoder = JSONEncoder()
                data = try encoder.encode(newValue)
                modifiedDate = .now
                if (self.version ?? 0) < Self.version {
                    self.version = Self.version
                }
            } catch {
                print("Unable to encode watch layout from update \(error)")
                data = nil
            }
        }
    }

    var nonNilName: String { name ?? String(localized: "UNKWOWN_NAME") }
    var nonNilModifiedDate: Date { modifiedDate ?? Date.distantPast }
}

typealias ConfigData = DataSchema.CalendarConfig
extension ConfigData {
    static let version = intVersion(DataSchema.versionIdentifier)
    static let predicate = #Predicate<ConfigData> { entry in
        entry.data != nil
    }

    var isNil: Bool {
        return data == nil || name == nil || modifiedDate == nil
    }

    var config: CalendarConfigure? {
        get {
            let decoder = JSONDecoder()
            do {
                if let data {
                    return try decoder.decode(CalendarConfigure.self, from: data)
                } else {
                    return nil
                }
            } catch {
                print("Unable to decode calendar config \(error)")
                return nil
            }
        } set {
            do {
                let encoder = JSONEncoder()
                data = try encoder.encode(newValue)
                modifiedDate = .now
                if (self.version ?? 0) < Self.version {
                    self.version = Self.version
                }
            } catch {
                print("Unable to encode calendar config from update \(error)")
                data = nil
            }
        }
    }

    var nonNilName: String { name ?? String(localized: "UNKWOWN_NAME") }
    var nonNilModifiedDate: Date { modifiedDate ?? Date.distantPast }
}

typealias RemindersData = DataSchema.RemindersList
extension RemindersData: Bindable {
    static let version = intVersion(DataSchema.versionIdentifier)
    static let predicate = #Predicate<RemindersData> { entry in
        entry.data != nil
    }

    static func load(context: ModelContext) throws -> [ReminderList] {
        let descriptor = FetchDescriptor(predicate: Self.predicate, sortBy: [SortDescriptor(\.modifiedDate, order: .reverse)])
        if try context.fetchCount(descriptor) > 0 {
            let reminders = try context.fetch(descriptor).compactMap { $0.list }
            return reminders
        } else {
            return []
        }
    }

    var list: ReminderList? {
        get {
            let decoder = JSONDecoder()
            do {
                if let data {
                    return try decoder.decode(ReminderList.self, from: data)
                } else {
                    return nil
                }
            } catch {
                print("Unable to decode reminder list \(error)")
                return nil
            }
        } set {
            do {
                let encoder = JSONEncoder()
                data = try encoder.encode(newValue)
                modifiedDate = .now
                if (self.version ?? 0) < Self.version {
                    self.version = Self.version
                }
            } catch {
                print("Unable to encode reminder list from update \(error)")
                data = nil
            }
        }
    }

    var nonNilList: ReminderList {
        get {
            list ?? .init(name: String(localized: "UNNAMED"), enabled: false, reminders: [])
        } set {
            list = newValue
        }
    }

    var isNil: Bool {
        return data == nil || modifiedDate == nil
    }

    var nonNilModifiedDate: Date { modifiedDate ?? Date.distantPast }
}

enum DataSchemaV7: VersionedSchema {
    static var versionIdentifier: Schema.Version {
        .init(4, 0, 0)
    }
    static var models: [any PersistentModel.Type] {
        [Theme.self, CalendarConfig.self, RemindersList.self]
    }

    @Model final class CalendarConfig {
        @Attribute(.allowsCloudEncryption) fileprivate var data: Data?
        @Attribute(.allowsCloudEncryption) var name: String?
        var modifiedDate: Date?
        var version: Int?

        init(_ config: CalendarConfigure, name: String) throws {
            let encoder = JSONEncoder()
            self.data = try encoder.encode(config)
            self.name = name
            self.modifiedDate = .now
            self.version = intVersion(DataSchemaV7.versionIdentifier)
        }
    }

    @Model final class Theme {
        @Attribute(.allowsCloudEncryption) fileprivate var data: Data?
        @Attribute(.allowsCloudEncryption) var name: String?
        @Attribute(.allowsCloudEncryption) var deviceName: String?
        var modifiedDate: Date?
        var version: Int?

        init(_ layout: WatchLayout, name: String, deviceName: String) throws {
            let encoder = JSONEncoder()
            self.data = try encoder.encode(layout)
            self.name = name
            self.deviceName = deviceName
            self.modifiedDate = .now
            self.version = intVersion(DataSchemaV7.versionIdentifier)
        }
    }

    @Model final class RemindersList {
        @Attribute(.allowsCloudEncryption) fileprivate var data: Data?
        var modifiedDate: Date?
        var version: Int?

        init(_ reminderList: ReminderList) throws {
            let encoder = JSONEncoder()
            self.data = try encoder.encode(reminderList)
            self.version = intVersion(DataSchemaV7.versionIdentifier)
            self.modifiedDate = .now
        }
    }
}

enum DataMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [DataSchemaV7.self]
    }

    static var stages: [MigrationStage] { [] }
}

@ModelActor
actor LocalDataModel {
    static let shared = LocalDataModel(modelContainer: LocalSchema.container)
}

typealias LocalSchema = LocalSchemaV4
extension LocalSchema {
    static let container = {
        let localSchema = Schema(versionedSchema: LocalSchema.self)
#if DEBUG
        let modelConfig = ModelConfiguration("LocalData-debug", schema: localSchema, groupContainer: .automatic, cloudKitDatabase: .none)
#else
        let modelConfig = ModelConfiguration("LocalData", schema: localSchema, groupContainer: .automatic, cloudKitDatabase: .none)
#endif
        return createContainer(schema: localSchema, migrationPlan: LocalDataMigrationPlan.self, configurations: [modelConfig])
    }()
}

protocol LocalDataModelType: PersistentModel {}

extension LocalDataModelType {
    static fileprivate func _load(context: ModelContext) throws -> Self? {
        var descriptor = FetchDescriptor<Self>()
        descriptor.fetchLimit = 1
        return try context.fetch(descriptor).first
    }
}

typealias LocalStats = LocalSchema.LocalStats
extension LocalStats: Identifiable, Hashable, LocalDataModelType {
    static let version = intVersion(LocalSchema.versionIdentifier) + 1
    @MainActor static func notLatest() -> Bool {
        let modelContext = LocalSchema.container.mainContext
        if let localStats = try? _load(context: modelContext) {
            if localStats.version < Self.version {
                localStats.version = Self.version
                return true
            } else {
                return false
            }
        } else {
            modelContext.insert(LocalStats(version: Self.version))
            return true
        }
    }

    @MainActor static func experienced() -> Bool {
        let modelContext = LocalSchema.container.mainContext
        if let localStats = try? _load(context: modelContext) {
            localStats.launchCount += 1
            if localStats.creationTime.distance(to: .now) > 3600 * 24 * 5 && localStats.launchCount >= 5 {
                return true
            } else {
                return false
            }
        } else {
            modelContext.insert(LocalStats(version: Self.version))
            return false
        }
    }
}

typealias LocalTheme = LocalSchema.LocalTheme
extension LocalTheme: Identifiable, Hashable, LocalDataModelType {
    static let version = intVersion(LocalSchema.versionIdentifier)
    var theme: WatchLayout {
        get {
            let decoder = JSONDecoder()
            do {
                return try decoder.decode(WatchLayout.self, from: data)
            } catch {
                print("Cannot decode watch layout from local storage: \(error)")
                return .init()
            }
        } set {
            do {
                let encoder = JSONEncoder()
                data = try encoder.encode(newValue)
                modifiedDate = .now
                if version < Self.version {
                    version = Self.version
                }
            } catch {
                print("Cannot encode watch layout new value: \(error)")
            }
        }
    }

    static func load(context: ModelContext) -> Self {
        if let themeData = try? _load(context: context) {
            return themeData
        } else {
            let themeData = try! Self.init(.defaultLayout)
            context.insert(themeData)
            return themeData
        }
    }
}

typealias LocalConfig = LocalSchema.LocalCalendarConfig
extension LocalConfig: Identifiable, Hashable, LocalDataModelType {
    static let version = intVersion(LocalSchema.versionIdentifier)
    var config: CalendarConfigure {
        get {
            let decoder = JSONDecoder()
            do {
                return try decoder.decode(CalendarConfigure.self, from: data)
            } catch {
                print("Cannot decode calendar config from local storage: \(error)")
                return .init()
            }
        } set {
            do {
                let encoder = JSONEncoder()
                data = try encoder.encode(newValue)
                modifiedDate = .now
                if version < Self.version {
                    version = Self.version
                }
            } catch {
                print("Cannot encode calendar config new value: \(error)")
            }
        }
    }

    static func load(context: ModelContext) -> Self {
        if let configData = try? _load(context: context) {
            return configData
        } else {
            let configData = try! Self.init(.init())
            context.insert(configData)
            return configData
        }
    }
}

enum LocalSchemaV4: VersionedSchema {
    static var versionIdentifier: Schema.Version {
        .init(4, 0, 0)
    }
    static var models: [any PersistentModel.Type] {
        [LocalStats.self, LocalTheme.self, LocalCalendarConfig.self]
    }

    @Model final class LocalStats {
        #Unique<LocalStats>([\.name])

        var name = "__local_stats__"
        var creationTime = Date.now
        var launchCount = 0
        var version: Int

        init(version: Int) {
            self.version = version
        }
    }

    @Model final class LocalCalendarConfig {
        #Unique<LocalCalendarConfig>([\.name])

        var name = "__local_calendar_config__"
        private var data: Data
        var modifiedDate: Date
        var version: Int

        init(_ config: CalendarConfigure) throws {
            let encoder = JSONEncoder()
            self.data = try encoder.encode(config)
            self.modifiedDate = .now
            self.version = intVersion(LocalSchemaV4.versionIdentifier)
        }
    }

    @Model final class LocalTheme {
        #Unique<LocalTheme>([\.name])

        var name = "__local_watch_layout__"
        private var data: Data
        var modifiedDate: Date
        var version: Int

        init(_ layout: WatchLayout) throws {
            let encoder = JSONEncoder()
            self.data = try encoder.encode(layout)
            self.modifiedDate = .now
            self.version = intVersion(LocalSchemaV4.versionIdentifier)
        }
    }
}

enum LocalDataMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [LocalSchemaV4.self]
    }

    static var stages: [MigrationStage] { [] }
}
