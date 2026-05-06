//
//  Documentation.swift
//  Chinendar
//
//  Created by Leo Liu on 6/23/23.
//

import SwiftUI

struct Documentation: View {
    let helpString: String = String(localized: "HELP_DOC")
    private let parser = MarkdownParser()
    @State fileprivate var articles: [Paragraph] = []
    @Environment(ViewModel.self) var viewModel

    var body: some View {
        Form {
            ForEach(articles) { article in
                ParagraphView(article: article)
            }
        }
        .formStyle(.grouped)
#if os(iOS) || os(visionOS)
        .listSectionSpacing(.compact)
#endif
        .task {
            prepareArticle(markdown: helpString)
        }
        .navigationTitle("Q&A")
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

    func prepareArticle(markdown: String) {
        let elements = parser.parse(markdown)
        var articleInWork = [Paragraph]()
        var title = AttributedString()
        for element in elements {
            switch element {
            case .heading(let text):
                title = text.mergingAttributes(element.attributeContainer)
            case .paragraph(text: var text):
                for i in 0..<text.count {
                    text[i] = text[i].mergingAttributes(element.attributeContainer)
                }
                articleInWork.append(Paragraph(title: title, body: text))
            }
        }
        articles = articleInWork
    }
}

struct ParagraphView: View {
    @State fileprivate var article: Paragraph

    var body: some View {
        Section {
            Button {
                withAnimation {
                    article.show.toggle()
                }
            } label: {
                HStack {
                    Text(article.title)
                        .frame(maxWidth: .infinity, alignment: .leading)
                    Image(systemName: article.show ? "chevron.up" : "chevron.down")
                        .transition(.scale)
#if os(iOS) || os(macOS)
                        .foregroundStyle(Color.accentColor)
#endif
                }
            }
#if os(iOS) || os(macOS)
            .buttonStyle(.plain)
#elseif os(visionOS)
            .buttonStyle(.automatic)
#endif
            if article.show {
                VStack(spacing: 10) {
                    ForEach(0..<article.body.count, id: \.self) { index in
                        Text(article.body[index])
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .lineSpacing(1.4)
                    }
                }
            }
        }
    }
}

private enum MarkdownElement {
    case heading(_: AttributedString)
    case paragraph(_: [AttributedString])
}

private struct MarkdownParser {
    func parse(_ markdownString: String) -> [MarkdownElement] {
        var elements: [MarkdownElement] = []
        var currentParagraph: [AttributedString] = []
        let scanner = Scanner(string: markdownString)
        while !scanner.isAtEnd {
            if let line = scanner.scanUpToCharacters(from: .newlines), let attrLine = try? AttributedString(markdown: line) {
                if headingLevel(for: line) > 0 {
                    if !currentParagraph.isEmpty {
                        elements.append(.paragraph(currentParagraph))
                        currentParagraph = []
                    }
                    elements.append(.heading(attrLine))
                } else {
                    currentParagraph.append(attrLine)
                }
            }
        }

        if !currentParagraph.isEmpty {
            elements.append(.paragraph(currentParagraph))
        }

        return elements
    }

    private func headingLevel(for line: String) -> Int {
        let trimmedLine = line.trimmingCharacters(in: .whitespacesAndNewlines)
        guard trimmedLine.count > 0 else { return 0 }
        var index = trimmedLine.startIndex
        var count = 0
        while index < trimmedLine.endIndex && trimmedLine[index] == "#" {
            count += 1
            index = trimmedLine.index(after: index)
        }
        return min(count, 6)
    }
}

private extension MarkdownElement {

    var attributeContainer: AttributeContainer {
        var container = AttributeContainer()
        switch self {
        case .heading:
            container.font = .headline
        case .paragraph:
            container.font = .body
        }
        return container
    }
}

private struct Paragraph: Identifiable {
    var id = UUID()
    let title: AttributedString
    let body: [AttributedString]
    var show: Bool = false
}

#Preview("Documentation", traits: .modifier(SampleData())) {
    NavigationStack {
        Documentation()
    }
}
