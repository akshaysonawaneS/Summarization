import PyPDF2
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np

text =[]

def main():
    pdfExtractor()

def summ(text1):
    sentence = list(text1.split("."))
    sentences = []
    for i in sentence:
        sentences.append(i.replace("[^a-zA-Z]", " ").split(" "))

    sentences.pop()
    print(sentences)

def pdfExtractor():
    pdfFileObj = open('sample.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    pgno = pdfReader.numPages
    for i in range(pgno):
        pageObj = pdfReader.getPage(i)
        text.append(pageObj.extractText())

    text1 = ''.join(text)
    summ(text1)
    pdfFileObj.close()


if __name__ == "__main__":
    main()

