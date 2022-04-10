import os
import math
from pprint import pprint
from prettytable import PrettyTable

os.system('cls' if os.name == 'nt' else 'clear')

# Global variables
docLength = 0

# Membaca file text
def readFiles(filenames):
    docs = []
    for filename in filenames:
        file = open(filename, "r");
        docs.append(file.read());
    return docs

# Memecah text menjadi kata
def getWords(docs, unique = True):
    words = " ".join(str(doc) for doc in docs).split(" ")
    return set(words) if unique else words

# Periksa jumlah kemunculan kata di setiap text
def checkWords(words, docs):
    occurences = dict()
    for word in words:
        occurences[word] = []
        for docIndex, doc in enumerate(docs):
            occurences[word].append(0)
            docWords = getWords([doc], False)
            for docWord in docWords:
                if word in docWord:
                    occurences[word][docIndex] += 1
    return occurences

# Hitung TF
def getTFs(occurences, words, docs):
    tfs = dict()
    for word in words:
        tfs[word] = []
        for docIndex, _ in enumerate(docs):
            occurence = occurences[word][docIndex]
            tfs[word].append(1 + math.log10(occurence) if occurence > 0 else 0)
    return tfs

# Hitung IDF
def getIDFs(occurences, words, docs):
    idfs = dict()
    for word in words:
        idfs[word] = math.log10(len(docs) / sum(occurences[word])) if sum(occurences[word]) > 0 else 0
    return idfs

# Hitung TF-IDF
def getTFIDF(tfs, idfs, words, docs):
    tfidfs = dict()
    for word in words:
        tfidfs[word] = []
        for docIndex, _ in enumerate(docs):
            tfidfs[word].append(0)
            tfidfs[word][docIndex] = tfs[word][docIndex] * idfs[word]
    return tfidfs

# Tampil
def getColumnNames(title):
    columnNames = [title]
    for docIndex in range(1, docLength + 1):
        columnNames.append("D" + str(docIndex))
    return columnNames

def displayStep1(docs):
    for docIndex, doc in enumerate(docs):
        print("D" + str(docIndex + 1))
        print(doc + "\n")

def displayStep2(words):
    pprint(words)

def displayStep3(occurences):
    table = PrettyTable(getColumnNames("Jumlah"))
    sortedOccurences = dict(sorted(occurences.items()))
    for word in sortedOccurences:
        row = sortedOccurences[word].copy()
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep4(tfs):
    table = PrettyTable(getColumnNames("TF"))
    sortedTfs = dict(sorted(tfs.items()))
    for word in sortedTfs:
        row = sortedTfs[word].copy()
        row = ['%0.3f' % x for x in row]
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep5(idfs):
    table = PrettyTable(["", "IDF"])
    sortedIdfs = dict(sorted(idfs.items()))
    for word in sortedIdfs:
        row = [sortedIdfs[word]]
        row = ['%0.3f' % x for x in row]
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep6(tfIdfs):
    table = PrettyTable(getColumnNames("TF-IDF"))
    sortedTfIdfs = dict(sorted(tfIdfs.items()))
    for word in sortedTfIdfs:
        row = sortedTfIdfs[word].copy()
        row = ['%0.3f' % x for x in row]
        row.insert(0, word)
        table.add_row(row)
    print(table)

def display(title, step, data):
    print(title)
    match step:
        case 1: displayStep1(data)
        case 2: displayStep2(data)
        case 3: displayStep3(data)
        case 4: displayStep4(data)
        case 5: displayStep5(data)
        case 6: displayStep6(data)

docs = readFiles(
    [
        "docs/doc1.txt",
        "docs/doc2.txt",
        "docs/doc3.txt",
        "docs/doc4.txt"
    ]
)
docLength = len(docs)
display("\n1. Membaca file text", 1, docs)

words = getWords(docs)
display("\n2. Memecah text menjadi kata", 2, words)

occurences = checkWords(words, docs)
display("\n3. Periksa jumlah kemunculan kata di setiap text", 3, occurences)

tfs = getTFs(occurences, words, docs)
display("\n4. Hitung TF", 4, tfs)

idfs = getIDFs(occurences, words, docs)
display("\n5. Hitung IDF", 5, idfs)

tfidfs = getTFIDF(tfs, idfs, words, docs)
display("\n6. Hitung TF-IDF", 6, tfidfs)

