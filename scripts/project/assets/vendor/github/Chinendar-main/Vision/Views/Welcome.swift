//
//  Welcome.swift
//  Chinendar
//
//  Created by Leo Liu on 11/17/23.
//

import SwiftUI

struct Welcome: View {
    let size: CGSize
    @Environment(\.dismiss) var dismiss
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        let baseLength = min(size.width, size.height)
        VStack {
            ScrollView(showsIndicators: false) {
                VStack(spacing: baseLength / 25) {
                    Spacer(minLength: baseLength / 50)
                        .frame(maxHeight: baseLength / 25)
                    Icon(watchLayout: viewModel.watchLayout)
                        .frame(width: baseLength / 4, height: baseLength / 4)
                    Text("CHINENDAR")
                        .font(.largeTitle.bold())
                    Spacer(minLength: baseLength / 50)
                        .frame(maxHeight: baseLength / 25)
                    VStack(spacing: baseLength / 25) {
                        FeatureRow(imageName: "pencil.circle.fill", title: "WKM_1_TITLE", detail: "WKM_1_DETAIL", baseLength: baseLength)
                        FeatureRow(imageName: "gearshape.fill", title: "WKM_2_TITLE", detail: "WKM_2_DETAIL", baseLength: baseLength)
                        FeatureRow(imageName: "wand.and.stars", title: "WKM_3_TITLE", detail: "WKM_3_DETAIL", baseLength: baseLength)
                    }
                }
            }
            Spacer(minLength: baseLength / 50)
                .frame(maxHeight: baseLength / 25)
            Button {
                dismiss()
            } label: {
                Text("OK")
                    .frame(maxWidth: .infinity)
            }
            .controlSize(.large)
#if os(visionOS)
            .buttonStyle(.automatic)
#else
            .buttonStyle(.glass)
#endif
        }
        .padding(.horizontal)
        .frame(width: size.width, height: size.height)
    }
}

struct FeatureRow: View {
    let imageName: String
    let title: LocalizedStringResource
    let detail: LocalizedStringResource
    let baseLength: CGFloat

    var body: some View {
        HStack {
            Image(systemName: imageName)
                .font(.largeTitle)
                .frame(width: baseLength / 6, height: baseLength / 6)
                .foregroundStyle(Color.accentColor)
            VStack(alignment: .leading) {
                Text(title)
                    .font(.title3)
                    .padding(.vertical, baseLength / 100)
                    .padding(.trailing, baseLength / 25)
                    .frame(maxWidth: .infinity, alignment: .leading)
                Text(detail)
                    .font(.body)
            }
        }
    }
}

#Preview("Welcome", traits: .modifier(SampleData())) {
    Welcome(size: CGSize(width: 396, height: 484))
}
