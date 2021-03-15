
# Удаляем дублирующиеся символы в слове
# Возвращаем строку из слов
def duble(listWord):
    splitWord = listWord.split(" ")
    newString = ""
    for i in splitWord:
        for j in i:
            if i.count(j) == 1:
                newString += j
        newString += " "

    return newString


def slog(string):
    glas = ["а", "у", "о", "ы", "э", "я", "ю", "ё", "и", "е"]
    zvonSogl = ["б", "в", "г", "д", "ж", "з"]
    gluxSogl = ["к", "п", "с", "т", "ф", "х", "ц", "ч", "ш", "щ"]
    sonarSogl = ["л", "р", "м", "н", "й"]
    temp = ""
    iter = 0
    dlinnaSlova = len(string)
    for i in string:
        if i in zvonSogl:
            temp += i
            if iter+1 < dlinnaSlova:
                if string[iter + 1] in zvonSogl:
                    if iter + 1 != dlinnaSlova:
                        temp += "-"
        elif i in gluxSogl:
            temp += i
        elif i in sonarSogl:
            temp += i
            if iter+2 < dlinnaSlova:
                if (string[iter + 1] in glas) and (string[iter + 2] in sonarSogl):
                    iter += 1
                    continue
                if string[iter + 2] in sonarSogl:
                    if (iter + 2 != dlinnaSlova) and (iter + 1 != dlinnaSlova):
                        temp += "-"
                if string[iter + 1] in zvonSogl:
                    if (iter + 1 != dlinnaSlova):
                        temp += "-"
                if string[iter+1] in gluxSogl:
                    if (iter + 1 != dlinnaSlova):
                        temp += "-"

        elif i in glas:
            temp += i
            if iter+2 < dlinnaSlova:
                if (string[iter + 1] in zvonSogl) and (string[iter + 2] in zvonSogl):
                    iter += 1
                    continue
                if (string[iter + 1] in sonarSogl) and (string[iter + 2] in sonarSogl):
                    iter += 1
                    continue
                if (string[iter + 1] in sonarSogl) and (string[iter + 2] in zvonSogl):
                    iter += 1
                    continue
                if ((string[iter-1] in sonarSogl) and (string[iter+1] in sonarSogl)):
                    iter += 1
                    continue

            if (iter+2 != dlinnaSlova) and (iter+1 != dlinnaSlova):
                temp += "-"
        iter += 1

    return temp


def spletnik(wordOne, wordTwo):
    a = wordOne.split("-")
    b = wordTwo.split("-")
    temp = ""
    temp += b[0]
    iter = 0
    for i in a:
        if iter != 0:
            temp += i
        iter += 1
    iter = 0
    temp += " "+a[0]
    for i in b:
        if iter != 0:
            temp += i
        iter += 1
    return temp


def wordCount(string):
    temp = string.split(" ")
    setString = set(temp)
    for i in setString:
        coun = temp.count(i)
        print(i, "-", coun)


a = "как дела хорошо а у тебя "
b = slog("собака")
c = slog("сплетня")
d = "раз два два три три три четыре четыре четыре четыре"

print(duble(a))
print(slog("слово"))
print(slog("сплетня"))
print(spletnik(b, c))
print(wordCount(d))
