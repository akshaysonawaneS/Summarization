import urllib
from urllib.request import urlopen
import PyPDF2
from bs4 import BeautifulSoup, Comment
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize



text = []

def create_frequency_table(text_string):

    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary



def find_average_score(sentenceValue):
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

def score_sentences(sentences, freqTable):
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue

def main():
    txt = pdfExtractor()
    freq_table = create_frequency_table(txt)
    sentences = sent_tokenize(txt)
    sentence_scores = score_sentences(sentences, freq_table)
    threshold = find_average_score(sentence_scores)
    summary = generate_summary(sentences, sentence_scores, 1.5 * threshold)
    print(summary)

def pdfExtractor(path):
    summary = ''
    text1 = ''
    text=[]
    path = "uploads/" + path
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    pgno = pdfReader.numPages
    for i in range(pgno):
        pageObj = pdfReader.getPage(i)
        text.append(pageObj.extractText())

    text1 = ''.join(text)

    freq_table = create_frequency_table(text1)                                  # Creating frequency table
    sentences = sent_tokenize(text1)                                            # Tokenize Sentence
    sentence_scores = score_sentences(sentences, freq_table)
    threshold = find_average_score(sentence_scores)
    summary = generate_summary(sentences, sentence_scores, 1.5 * threshold)
    print(text1)
    print("----------------------------After Summurize---------------------------------------")
    print(summary)

    pdfFileObj.close()
    return (summary,text1)

if __name__ == "__main__":
     main()
