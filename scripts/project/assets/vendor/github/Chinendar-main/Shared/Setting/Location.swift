//
//  Location.swift
//  Chinendar
//
//  Created by Leo Liu on 6/24/23.
//

import SwiftUI

struct Location: View {
    @State fileprivate var locationData = LocationData()
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            Section {
                Toggle("LOCATION", isOn: locationData.binding(\.locationEnabled))
                Toggle("HERE", isOn: locationData.binding(\.gpsEnabled))
                    .disabled(!locationData.locationEnabled)
            }
            if locationData.locationEnabled {
                if locationData.gpsEnabled {
                    Section(header: Text("LAT&LON")) {
                        if let location = viewModel.location {
                            let locationString = coordinateDesp(coordinate: location)
                            Text("LAT\(locationString.lat),LON:\(locationString.lon)")
                                .frame(maxWidth: .infinity, alignment: .center)
                                .privacySensitive()
                        } else {
                            Text("INVALID_LOCATION")
                                .frame(maxWidth: .infinity, alignment: .center)
                        }
                    }
                } else {
                    let manualLocationDesp = locationData.manualLocation.map { coordinateDesp(coordinate: $0) }
                    let latitudeTitle = if let manualLocationDesp {
                        Text("LAT:\(manualLocationDesp.lat)")
                    } else {
                        Text("LAT")
                    }
                    Section(header: latitudeTitle) {
                        LocationInput(locationSelection: locationData.binding(\.latitudeSelection), maxDegree: 89, signLabel: "LAT_NS", positiveLabel: "LAT_N", negativeLabel: "LAT_S")
                    }

                    let longitudeTitle = if let manualLocationDesp {
                        Text("LON:\(manualLocationDesp.lon)")
                    } else {
                        Text("LON")
                    }
                    Section(header: longitudeTitle) {
                        HStack(spacing: 10) {
                            LocationInput(locationSelection: locationData.binding(\.longitudeSelection), maxDegree: 179, signLabel: "LON_EW", positiveLabel: "LON_E", negativeLabel: "LON_W")
                        }
#if os(iOS)
                        .pickerStyle(.wheel)
                        .frame(maxHeight: 125)
#elseif os(macOS)
                        .pickerStyle(.menu)
#endif
                    }
                }
            }
        }
        .formStyle(.grouped)
        .alert("LOCATION_FAILED", isPresented: locationData.binding(\.presentError)) {
            Button("OK", role: .cancel) {}
        } message: {
            let errorMessage = switch locationData.error {
            case .authorizationDenied:
                Text("APP_LOC_OFF")
            case .authorizationDeniedGlobally:
                Text("DEVICE_LOC_OFF")
            case .authorizationRestricted:
                Text("LOC_RESTRICTED")
            case .locationUnavailable:
                Text("LOC_UNAVAILABLE")
            case .updateError:
                Text("LOC_FAILED_OTHER", comment: "location update error")
            case .none:
                Text("")
            }
            errorMessage
        }
        .task {
            locationData.setup(viewModel: viewModel)
        }
        .navigationTitle("LAT&LON")
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

struct LocationInput: View {
    @Binding fileprivate var locationSelection: LocationSelection
    let maxDegree: Int
    let signLabel: LocalizedStringKey
    let positiveLabel: LocalizedStringKey
    let negativeLabel: LocalizedStringKey

    var body: some View {
        HStack(spacing: 10) {
#if os(iOS)
            Picker("DEGREE", selection: $locationSelection.degree) {
                ForEach(0...maxDegree, id: \.self) { value in
                    Text("\(value)")
                }
            }
            .animation(.default, value: locationSelection)
            Picker("GEO_MINUTE", selection: $locationSelection.minute) {
                ForEach(0...59, id: \.self) { value in
                    Text("\(value)")
                }
            }
            .animation(.default, value: locationSelection)
            Picker("GEO_SECOND", selection: $locationSelection.second) {
                ForEach(0...60, id: \.self) { value in
                    Text("\(value)")
                }
            }
            .animation(.default, value: locationSelection)
#elseif os(macOS) || os(visionOS)
            OnSubmitTextField("DEGREE", value: $locationSelection.degree, formatter: {
                let formatter = NumberFormatter()
                formatter.maximumFractionDigits = 0
                formatter.maximum = NSNumber(value: maxDegree)
                formatter.minimum = 0
                return formatter
            }())
            Divider()
            OnSubmitTextField("GEO_MINUTE", value: $locationSelection.minute, formatter: {
                let formatter = NumberFormatter()
                formatter.maximumFractionDigits = 0
                formatter.maximum = 59
                formatter.minimum = 0
                return formatter
            }())
            Divider()
            OnSubmitTextField("GEO_SECOND", value: $locationSelection.second, formatter: {
                let formatter = NumberFormatter()
                formatter.maximumFractionDigits = 0
                formatter.maximum = 60
                formatter.minimum = 0
                return formatter
            }())
            Divider()
#endif
            Picker(signLabel, selection: $locationSelection.positive) {
                ForEach([true, false], id: \.self) { value in
                    value ? Text(positiveLabel) : Text(negativeLabel)
                }
            }
            .animation(.default, value: locationSelection)
        }
#if os(iOS)
        .pickerStyle(.wheel)
        .frame(maxHeight: 125)
#elseif os(macOS)
        .pickerStyle(.menu)
#endif
    }
}

#if os(macOS) || os(visionOS)
struct OnSubmitTextField<V: Numeric>: View {
    let title: LocalizedStringKey
    let formatter: NumberFormatter
    @Binding var value: V
    @State var tempValue: V
    @FocusState var isFocused: Bool

    init(_ title: LocalizedStringKey, value: Binding<V>, formatter: NumberFormatter) {
        self.title = title
        self.formatter = formatter
        self._value = value
        self._tempValue = State(initialValue: value.wrappedValue)
    }

    var body: some View {
        HStack {
            Text(title)
                .lineLimit(1)
                .frame(maxWidth: .infinity, alignment: .leading)
            TextField("", value: $tempValue, formatter: formatter)
                .labelsHidden()
#if os(iOS) || os(visionOS)
                .keyboardType(.decimalPad)
#endif
                .focused($isFocused)
                .autocorrectionDisabled()
                .onSubmit(of: .text) {
                    value = tempValue
                }
                .onChange(of: isFocused) {
                    if !isFocused {
                        value = tempValue
                    }
                }
#if os(macOS)
                .frame(height: 20)
#elseif os(visionOS)
                .frame(height: 40)
#endif
                .padding(.leading, 15)
#if os(visionOS)
                .background(.thickMaterial, in: RoundedRectangle(cornerRadius: 10))
                .contentShape(.hoverEffect, .rect(cornerRadius: 10, style: .continuous))
                .hoverEffect()
#elseif os(macOS)
                .background(in: RoundedRectangle(cornerRadius: 10))
#endif
        }
    }
}
#endif

@MainActor
@Observable private final class LocationData: Bindable {
    var viewModel: ViewModel?
    var error: LocationError?
    var presentError: Bool {
        get {
           error != nil
        } set {
           if !newValue {
               error = nil
           }
       }
    }

    func setup(viewModel: ViewModel) {
        self.viewModel = viewModel
    }

    var timezoneLongitude: CGFloat {
        let timezone = viewModel?.config.timezone ?? Calendar.current.timeZone
        let logitude = (CGFloat(timezone.secondsFromGMT()) - timezone.daylightSavingTimeOffset()) / 240
        return ((logitude + 180) %% 360) - 180
    }

    var locationEnabled: Bool {
        get {
            viewModel?.location != nil
        } set {
            if newValue {
                viewModel?.config.customLocation = viewModel?.config.customLocation ?? GeoLocation(lat: 0.0, lon: timezoneLongitude)
            } else {
                viewModel?.config.locationEnabled = false
                viewModel?.config.customLocation = nil
                viewModel?.clearLocation()
            }
        }
    }

    var gpsEnabled: Bool {
        get {
            viewModel?.gpsLocationAvailable ?? false
        } set {
            if newValue {
                Task {
                    do throws(LocationError) {
                        try await viewModel?.locationManager.getLocation(wait: .seconds(5))
                        viewModel?.config.locationEnabled = true
                    } catch {
                        self.error = error
                    }
                }
            } else {
                viewModel?.config.locationEnabled = false
                viewModel?.config.customLocation = viewModel?.config.customLocation ?? viewModel?.location ?? GeoLocation(lat: 0.0, lon: timezoneLongitude)
                viewModel?.clearLocation()
            }
        }
    }

    var manualLocation: GeoLocation? {
        viewModel?.config.customLocation
    }

    var latitudeSelection: LocationSelection {
        get {
            LocationSelection.from(value: manualLocation?.lat ?? 0)
        } set {
            viewModel?.config.customLocation = GeoLocation(lat: newValue.value, lon: viewModel?.config.customLocation?.lon ?? 0)
        }
    }

    var longitudeSelection: LocationSelection {
        get {
            LocationSelection.from(value: manualLocation?.lon ?? CGFloat(Calendar.current.timeZone.secondsFromGMT()) / 240)
        } set {
            viewModel?.config.customLocation = GeoLocation(lat: viewModel?.config.customLocation?.lat ?? 0, lon: newValue.value)
        }
    }

    var location: GeoLocation? {
        viewModel?.location
    }
}

private func coordinateDesp(coordinate: GeoLocation) -> (lat: Text, lon: Text) {
    let latitudeLabel = if coordinate.lat > 0 {
        Text("LAT_N")
    } else if coordinate.lat < 0 {
        Text("LAT_S")
    } else {
        Text("")
    }
    let latitude = Int(round(abs(coordinate.lat) * 3600))
    let latitudeValue = "\(latitude / 3600)°\((latitude % 3600) / 60)\'\(latitude % 60)\""
    let latitudeString = Text("N/S:\(latitudeLabel),VALUE:\(latitudeValue)")

    let longitudeLabel = if coordinate.lon > 0 {
        Text("LON_E")
    } else if coordinate.lon < 0 {
        Text("LON_W")
    } else {
        Text("")
    }
    let longitude = Int(round(abs(coordinate.lon) * 3600))
    let longitudeValue = "\(longitude / 3600)°\((longitude % 3600) / 60)\'\(longitude % 60)\""
    let longitudeString = Text("E/W:\(longitudeLabel),VALUE:\(longitudeValue)")

    return (latitudeString, longitudeString)
}

private struct LocationSelection: Equatable {
    var positive = true
    var degree: Int = 0
    var minute: Int = 0
    var second: Int = 0

    var value: CGFloat {
        var locationValue = CGFloat(degree)
        locationValue += CGFloat(minute) / 60
        locationValue += CGFloat(second) / 3600
        locationValue *= positive ? 1.0 : -1.0
        return locationValue
    }

    static func from(value: CGFloat) -> Self {
        var values: [Int] = [0, 0, 0]
        let tempValue = Int(round(abs(value) * 3600))
        values[0] = tempValue / 3600
        values[1] = (tempValue % 3600) / 60
        values[2] = tempValue % 60
        return LocationSelection(positive: value >= 0, degree: values[0], minute: values[1], second: values[2])
    }
}

#Preview("Location", traits: .modifier(SampleData())) {
    NavigationStack {
        Location()
    }
}
