//
//  Welcome.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI

struct Welcome: View {
    @Environment(\.dismiss) var dismiss
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(spacing: 20) {
                Spacer(minLength: 10)
                    .frame(maxHeight: 20)
                Icon(watchLayout: viewModel.watchLayout)
                    .frame(width: 120, height: 120)
                Text("CHINENDAR")
                    .font(.largeTitle.bold())
                Spacer(minLength: 10)
                    .frame(maxHeight: 20)
                VStack(spacing: 20) {
                    FeatureRow(imageName: "pencil.circle.fill", title: "WKM_1_TITLE", detail: "WKM_1_DETAIL")
                    FeatureRow(imageName: "gearshape.fill", title: "WKM_2_TITLE", detail: "WKM_2_DETAIL")
                    FeatureRow(imageName: "wand.and.stars", title: "WKM_3_TITLE", detail: "WKM_3_DETAIL")
                }
            }
        }
        .scrollClipDisabled()
        .padding(.horizontal)
        Spacer()
        confirmationButton
            .padding()
    }

    var confirmationButton: some View {
        Button {
            dismiss()
        } label: {
            Text("OK")
                .frame(maxWidth: .infinity)
        }
        .controlSize(.large)
        .buttonStyle(.glass)
        .buttonBorderShape(.capsule)
    }
}

struct FeatureRow: View {
    let imageName: String
    let title: LocalizedStringResource
    let detail: LocalizedStringResource

    var body: some View {
        HStack {
            Image(systemName: imageName)
                .font(.largeTitle)
                .frame(width: 70, height: 70)
                .foregroundStyle(Color.accentColor)
            VStack(alignment: .leading) {
                Text(title)
                    .font(.headline)
                    .padding(.vertical, 5)
                    .padding(.trailing, 20)
                    .frame(maxWidth: .infinity, alignment: .leading)
                Text(detail)
                    .font(.subheadline)
            }
        }
    }
}

#Preview("Welcome", traits: .modifier(SampleData())) {
    Welcome()
}
