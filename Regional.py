from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

def create_frequency_table(text_string):
    mr_stopwords = []
    punctuation = [",", ".", "?", "!", "\"", "\'", ":", ";"]
    with open("res/marathiStopwords.txt", encoding="utf-8-sig") as fd:
        mr_stopwords = fd.read().split("\n")
    mr_stopwords = mr_stopwords
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        if(word != '\n'):
            word = ps.stem(word)
            if word in mr_stopwords and word in punctuation:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1
    return freqTable

def score_sentences(sentences, freqTable)->dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence:
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue

def find_average_score(sentenceValue)->int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))
    return average

def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

def starter():
    txt = """आयुष्यात माणसाला मागितलेलं सगळंच मिळतं का?
जगातला बहुतेक एकही माणूस या प्रश्नाचं उत्तर 'हो' असं देणार नाही.
आणि
दिलंच जर हो असे उत्तर, तर मग मनातल्या मनात तो स्वतःलाच हा प्रश्न पुन्हा पुन्हा विचारत बसेल की,
खरंच आयुष्यात माणसाला मागितलेलं सगळंच मिळतं का?

अजिबात काहीच मिळालं नाही असं म्हणता येत नाही. मागितलेलं मिळतंही.
पण कधी वेळ चुकलेली असते तर कधी मागितलेलंच चुकलेलं असतं.

आयुष्यात कितीही समाधानी झालो, तरी समाधानाच्या शेवटच्या एका टोकाला कुठेतरी एक अपुरी इच्छा जिवंत असते.
ती ज्याची त्यालाच माहित असते. ज्याची त्यालाच लक्षात राहते.

'वाटणं' आणि 'असणं' यातला फरक म्हणजे आयुष्य.
    
    """
    freq_table = create_frequency_table(txt)
    sentences = sent_tokenize(txt)
    sentence_scores = score_sentences(sentences, freq_table)
    threshold = find_average_score(sentence_scores)
    summary = generate_summary(sentences, sentence_scores, threshold)
    print(summary)


if __name__ == "__main__":
    starter()