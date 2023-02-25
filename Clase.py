import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator


translator = Translator()

#nltk.download()

cadena = """The Moscow Metro[a] is a metro system serving the Russian capital of Moscow as well as the neighbouring cities of Krasnogorsk, Reutov, Lyubertsy and Kotelniki in Moscow Oblast. 
Opened in 1935 with one 11-kilometre (6.8 mi) line and 13 stations, it was the first underground railway system in the Soviet Union.
As of 2021, the Moscow Metro, excluding the Moscow Central Circle, the Moscow Central Diameters and the Moscow Monorail, 
had 250 stations (287 with Moscow Central Circle) and its route length was 435.7 km (270.7 mi),[1] 
making it the fifth-longest in the world and the longest outside China. 
The system is mostly underground, with the deepest section 84 metres (276 ft) underground at the Park Pobedy station, one of the world's deepest underground stations. 
It is the busiest metro system in Europe, and is considered a tourist attraction in itself."""

#enlace = "https://es.wikipedia.org/wiki/Python"
#html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = get_text(cadena)

print("############################################")

#Removing square brackets and extra spaces
formatted_article_text = re.sub('[^a-zA-z]', ' ', text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(text)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#CALCULA LA FRASE QUE MAS SE REPITE
sentence_scores ={}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 50:
                if sent not in  sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#REALIZA EL RESUMEN CON LAS MEJORES FRASES
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

summary = translator.translate(summary, dest='es').text
print(summary)