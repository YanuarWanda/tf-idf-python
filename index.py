import os
import math
from prettytable import PrettyTable
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Hapus layar
os.system('cls' if os.name == 'nt' else 'clear')

# Global variables
decimalNumber = '%0.4f'
filenames = ['docs/document-1.txt', 'docs/document-2.txt']
# filenames = ["docs/doc1.txt", "docs/doc2.txt", "docs/doc3.txt", "docs/doc4.txt"]

# Stem
def stemDocument(filenames):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    docs = []
    for filename in filenames:
        file = open(filename, "r")
        docs.append(stemmer.stem(file.read()))
    return docs

# Membaca file text (Yang sudah berupa token - token)
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

# Hapus stopword
def removeStopword(words):
    file = open("docs/stopwords-id.txt")
    stopwords = file.read().split("\n")
    return getWords([word for word in words if word not in stopwords and not any(w.isdigit() for w in word)])

# Periksa jumlah kemunculan kata di setiap text
def checkWords(words, docs):
    occurences = dict()
    for word in words:
        occurences[word] = []
        for docIndex, doc in enumerate(docs):
            occurences[word].append(0)
            docWords = getWords([doc], False)
            for docWord in docWords:
                if word == docWord:
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
            tfidf = tfs[word][docIndex] * idfs[word]
            tfidfs[word][docIndex] = tfidf if tfidf > 0 else 0
    return tfidfs

# Tampil
def getColumnNames(title):
    columnNames = [title]
    for docIndex in range(1, len(filenames) + 1):
        columnNames.append("D" + str(docIndex))
    return columnNames

def displayStep1(docs):
    for docIndex, doc in enumerate(docs):
        print("D" + str(docIndex + 1))
        print(doc + "\n")

def displayStep2(words):
    print(sorted(words))

def displayStep3(filteredWords):
    print(sorted(filteredWords))

def displayStep4(occurences):
    table = PrettyTable(getColumnNames("Jumlah"))
    sortedOccurences = dict(sorted(occurences.items()))
    for word in sortedOccurences:
        row = sortedOccurences[word].copy()
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep5(tfs):
    table = PrettyTable(getColumnNames("TF"))
    sortedTfs = dict(sorted(tfs.items()))
    for word in sortedTfs:
        row = sortedTfs[word].copy()
        row = [decimalNumber % x for x in row]
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep6(idfs):
    table = PrettyTable(["", "IDF"])
    sortedIdfs = dict(sorted(idfs.items()))
    for word in sortedIdfs:
        row = [sortedIdfs[word]]
        row = [decimalNumber % x for x in row]
        row.insert(0, word)
        table.add_row(row)
    print(table)

def displayStep7(tfIdfs):
    table = PrettyTable(getColumnNames("TF-IDF"))
    sortedTfIdfs = dict(sorted(tfIdfs.items()))
    for word in sortedTfIdfs:
        row = sortedTfIdfs[word].copy()
        row = [decimalNumber % x for x in row]
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
        case 7: displayStep7(data)

# docs = readFiles(filenames)
# display("\n1. Membaca file text", 1, docs)

docs = stemDocument(filenames)
display("1. Stem dokumen", 1, docs)

words = getWords(docs)
display("\n2. Memecah text menjadi kata", 2, words)

filteredWords = removeStopword(words)
display("\n3. Menghapus stopword", 3, filteredWords)

occurences = checkWords(filteredWords, docs)
display("\n4. Periksa jumlah kemunculan kata di setiap text", 4, occurences)

tfs = getTFs(occurences, filteredWords, docs)
display("\n5. Hitung TF", 5, tfs)

idfs = getIDFs(occurences, filteredWords, docs)
display("\n6. Hitung IDF", 6, idfs)

tfidfs = getTFIDF(tfs, idfs, filteredWords, docs)
display("\n7. Hitung TF-IDF", 7, tfidfs)

