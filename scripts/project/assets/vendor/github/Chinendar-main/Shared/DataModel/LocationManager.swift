//
//  LocationManager.swift
//  Chinendar
//
//  Created by Leo Liu on 5/9/23.
//

import CoreLocation

struct GeoLocation: Equatable, Codable {
    let lat: Double
    let lon: Double
}

enum LocationError: Error {
    case authorizationDenied, authorizationDeniedGlobally, authorizationRestricted, locationUnavailable, updateError
}

actor LocationManager {
    static let shared = LocationManager()

    private var lastUpdateTime = Date.distantPast
    private var _lastUpdate: CLLocationUpdate?
    private var lastUpdate: CLLocationUpdate? {
        get {
            _lastUpdate
        } set {
            _lastUpdate = newValue
            if let newValue, newValue.location != nil {
                lastUpdateTime = .now
            } else {
                lastUpdateTime = .distantPast
            }
        }
    }
    private var location: GeoLocation? {
        if let loc = lastUpdate?.location {
            GeoLocation(lat: loc.coordinate.latitude, lon: loc.coordinate.longitude)
        } else {
            nil
        }
    }

    private init () {}

    @discardableResult
    func getLocation(wait duration: Duration = .seconds(5)) async throws(LocationError) -> GeoLocation? {
        if lastUpdateTime.distance(to: .now) > 3600 {
            let updates = CLLocationUpdate.liveUpdates()
            let timeoutTask = Task {
                try await Task.sleep(for: duration)
                return location
            }
            defer {
                timeoutTask.cancel()
            }
            do {
                for try await update in updates {
                    if update.location != nil {
                        lastUpdate = update
                        return location
                    } else if update.authorizationDeniedGlobally {
                        throw LocationError.authorizationDeniedGlobally
                    } else if update.authorizationDenied {
                        throw LocationError.authorizationDenied
                    } else if update.authorizationRestricted {
                        throw LocationError.authorizationRestricted
                    } else if update.locationUnavailable {
                        throw LocationError.locationUnavailable
                    } else if update.authorizationRequestInProgress {
                        let manager = CLLocationManager()
                        manager.requestWhenInUseAuthorization()
                    }
                }
            } catch let error as LocationError {
                throw error
            } catch {
                throw LocationError.updateError
            }
        }
        return location
    }

    func clearLocation() {
        lastUpdate = nil
    }
}
