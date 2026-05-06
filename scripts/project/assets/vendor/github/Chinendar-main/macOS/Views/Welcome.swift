//
//  Welcome.swift
//  Chinendar
//
//  Created by Leo Liu on 8/4/23.
//

import SwiftUI

struct Welcome: View {
    @Environment(\.dismiss) var dismiss
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(spacing: 20) {
                Icon(watchLayout: viewModel.watchLayout)
                    .frame(width: 120, height: 120)
                Text("CHINENDAR")
                    .font(.largeTitle.bold())
                    .padding(.bottom, 5)
                FeatureRow(imageName: "menubar.rectangle", title: "WKM_1_TITLE", detail: "WKM_1_DETAIL")
                FeatureRow(imageName: "pencil.and.outline", title: "WKM_2_TITLE", detail: "WKM_2_DETAIL")
                FeatureRow(imageName: "wand.and.stars", title: "WKM_3_TITLE", detail: "WKM_3_DETAIL")
            }
            .padding(20)
        }
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
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .font(.headline)
                    .padding(.vertical, 5)
                    .padding(.trailing, 5)
                Text(detail)
            }
        }
    }
}

#Preview("Welcome", traits: .modifier(SampleData())) {
    Welcome()
        .frame(minWidth: 300, idealWidth: 350, maxWidth: 400, minHeight: 400, idealHeight: 600, maxHeight: 700, alignment: .center)
}
