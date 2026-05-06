import readDic
import characters
import metaphysic
import random

def main():
    print("main")
    wuxingCharacters = set(metaphysic.main())
    print("Characters got by your shenchenbazi: ")
    print(wuxingCharacters)
    searchText = input('your search txt: ')
    desiredCharacters = set(list(readDic.main(searchText)))
    print("Characters got by your wish: ")
    print(desiredCharacters)

    gender = input("Male or female? Input 1 to represent male, input 2 to represent female: ")
    if gender == 1:
        genderCharacters = set(characters.male)
    else:
        genderCharacters =set(characters.female)
    print("Characters got by gender: ")
    print(genderCharacters)
    finalResult = desiredCharacters & desiredCharacters & genderCharacters
    print('Final result: ')
    print(finalResult)
    finalResultList = list(finalResult)
    print(finalResultList)
    finalName = finalResultList[random.randint(0, len(finalResultList)-1)] + finalResultList[random.randint(0, len(finalResultList)-1)]
    print('Test name: ')
    print(finalName)

if __name__ == '__main__':
    main()
