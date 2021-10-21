import spacy
import en_core_web_sm
from newsapi import NewsApiClient
import pickle
import pandas as pd

nlp_eng = en_core_web_sm.load()

def get_keywords_eng(content):
    doc = nlp_eng(content)
    result = []
    pos_tag = ['VERB','NOUN','PROPN']
    for token in doc:
        if (token.text in nlp_eng.Defaults.stop_words or token.pos_ == 'PUNCT'):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return result

newsapi = NewsApiClient (api_key='dcdcd9de70564105a8f40c6a32566d98')

articles = []
for i in range(5):
    temp = newsapi.get_everything(q='coronavirus', language='en', from_param='2021-09-21',
                                  to='2021-10-21', sort_by='relevancy',page=i+1)
    articles.append(temp)

filename = 'articlesCOVID.pckl'
pickle.dump(articles, open(filename, 'wb'))

# filename = 'articlesCOVID.pckl'
# articles = pickle.load(open(filename, 'rb'))

dados = []
for i, article in enumerate(articles):
    for x in article['articles']:
        title = x['title']
        date = x['publishedAt'][:10]
        description = x['description']
        content = x['content']
        dados.append({'title':title, 'date':date, 'desc':description, 'content':content})
df = pd.DataFrame(dados)
df = df.dropna()
df.head()

from collections import Counter
results = []
for content in df.content.values:
    results.append([('#' + x[0]) for x in Counter(get_keywords_eng(content)).most_common(5)])
df['keywords'] = results

filename = 'articlesCOVID_df.pckl'
pickle.dump(df, open(filename, 'wb'))

import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = str(results)
wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
