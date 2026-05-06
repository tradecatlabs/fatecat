import re

def main(searchText):
    # searchTxt = input('your search txt: ')
    charExp = r"(?<=^\*)\w{1}"
    wordExp = r"(?<=^\…)\w+(?=\＠)"
    with open('modern-chinese-dic.txt', 'r', encoding='utf-8') as f:
        modernDic = f.read()
        testExpression = r'.*' + searchText + r'.*\n'
        results = re.findall(testExpression, modernDic)
        relatedWordsDic = {}
        relatedCharactersDic = {}
        for result in results:
            matchedWord = re.search(wordExp, result)
            if (matchedWord):
                matchedWord = matchedWord.group()
                if len(matchedWord) <= 2:
                    relatedWordsDic[matchedWord] = result
            matchedCharacter = re.search(charExp, result)
            if (matchedCharacter):
                matchedCharacter = matchedCharacter.group()
                relatedCharactersDic[matchedCharacter] = result
                print(matchedCharacter)
                print(relatedCharactersDic[matchedCharacter])
    print(relatedCharactersDic)
    return relatedCharactersDic

if __name__ == '__main__':
    searchText = input('your search txt: ')
    main(searchText)

# r"：\S*?。"懒惰匹配去除所有例句