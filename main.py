from nltk import *
from collections import defaultdict

fileNames = ["./Reviews-9-products/Canon PowerShot SD500.txt",
"./Reviews-9-products/Canon S100.txt",
"./Reviews-9-products/Diaper Champ.txt",
"./Reviews-9-products/Hitachi router.txt",
"./Reviews-9-products/ipod.txt",
"./Reviews-9-products/Linksys Router.txt",
"./Reviews-9-products/MicroMP3.txt",
"./Reviews-9-products/Nokia 6600.txt",
"./Reviews-9-products/norton.txt" ]

outputTop = open("top20.csv", "w")
outputPart = open("part.csv", "w")

i = 0

for fileName in fileNames:
    print i
    i += 1
    reviewFile = open(fileName)
    predefinedAspects = set()
    map(
        lambda meaningfullLine: map(
            lambda lineWithAspect: predefinedAspects.add((lineWithAspect[:lineWithAspect.find('[')]).strip()), 
            filter(
                lambda line: len(line) > 0 and line[0] != '[',  
                meaningfullLine.split("##")[0].split(',')
                )
            ), 
        filter(
            lambda line: len(line) > 0 and line.find("##") > 0, 
            reviewFile.read().splitlines()
            )
        )

    reviewFile = open(fileName)
    topNouns = defaultdict(int)
    map(
        lambda meaningfullLine: map(
            lambda token: topNouns.update([(token[0], topNouns[token[0]] + 1)]),
            filter(
                lambda line: line[1] == "NN",
                pos_tag(word_tokenize(meaningfullLine.split("##")[1]))
                )
            ),
        filter(
            lambda line: len(line) > 0 and line.find("##") > 0, 
            reviewFile.read().splitlines()
            )
        )

    foundedAspects = set([pair[0] for pair in sorted(topNouns.iteritems(), key=lambda (k,v): (v,k), reverse=True)[:20]])

    precision = float(len(foundedAspects.intersection(predefinedAspects))) / len(foundedAspects)
    recall = float(len(foundedAspects.intersection(predefinedAspects))) / len(predefinedAspects)
    outputTop.write(str(fileName) + ',' + str(precision) + ',' + str(recall) + '\n')

    positiveWordsSet = set()
    positiveWordsFile = open("./opinion-lexicon-English/positive-words.txt")

    negativeWordsSet = set()
    negativeWordsFile = open("./opinion-lexicon-English/negative-words.txt")

    map(
        lambda word: positiveWordsSet.add(word), 
        filter(
            lambda line: len(line) > 0 and line[0] != ';', 
            positiveWordsFile.read().splitlines()
            )
        )

    map(
        lambda word: negativeWordsSet.add(word), 
        filter(
            lambda line: len(line) > 0 and line[0] != ';', 
            negativeWordsFile.read().splitlines()
            )
        )


    reviewFile = open(fileName)
    foundedAspects = set()
    map(
        lambda meaningfullLine: map(
            lambda ((w1, t1), (w2, t2)): foundedAspects.add(w1),
            filter(
                lambda ((w1, t1), (w2, t2)): w2 in positiveWordsSet.union(negativeWordsSet) and (simplify_wsj_tag(t2) in ["V", "ADJ"]) and simplify_wsj_tag(t1) == "N",
                ibigrams(pos_tag(word_tokenize(meaningfullLine.split("##")[1])))
                )
            ),
        filter(
            lambda line: len(line) > 0 and line.find("##") > 0, 
            reviewFile.read().splitlines()
            )
        )

    reviewFile = open(fileName)
    map(
        lambda meaningfullLine: map(
            lambda ((w1, t1), (w2, t2)): foundedAspects.add(w2),
            filter(
                lambda ((w1, t1), (w2, t2)): w1 in foundedAspects.intersection(predefinedAspects) and simplify_wsj_tag(t1) == "ADJ" and simplify_wsj_tag(t2) == "N",
                ibigrams(pos_tag(word_tokenize(meaningfullLine.split("##")[1])))
                )
            ),
        filter(
            lambda line: len(line) > 0 and line.find("##") > 0, 
            reviewFile.read().splitlines()
            )
        )


    reviewFile = open(fileName)
    map(
        lambda meaningfullLine: map(
            lambda ((w1, t1), (w2, t2), (w3, t3)): foundedAspects.add(w1),
            filter(
                lambda ((w1, t1), (w2, t2), (w3, t3)): w3 in positiveWordsSet.union(negativeWordsSet) and simplify_wsj_tag(t1) == "N" and simplify_wsj_tag(t2) == "V" and simplify_wsj_tag(t3) == "ADJ",
                itrigrams(pos_tag(word_tokenize(meaningfullLine.split("##")[1])))
                )
            ),
        filter(
            lambda line: len(line) > 0 and line.find("##") > 0, 
            reviewFile.read().splitlines()
            )
        )



    precision = float(len(foundedAspects.intersection(predefinedAspects))) / len(foundedAspects)
    recall = float(len(foundedAspects.intersection(predefinedAspects))) / len(predefinedAspects)
    outputPart.write(str(fileName) + ',' + str(precision) + ',' + str(recall) + '\n')

outputTop.close()
outputPart.close()




