import requests
from bs4 import BeautifulSoup
from ckonlpy.tag import Twitter
from soynlp.noun import LRNounExtractor_v2
import re

def get_article(url):
    r = requests.get(url, headers={'User-Agent': 'Chrome/86.0.4240.111'})
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    news_title = soup.find(attrs={'id': 'articleTitle'}).text
    news_sub_title = soup.find(attrs={'id': 'articleBodyContents'}).b.text
    news_content = soup.find(attrs={'id': 'articleBodyContents'}).text.strip().split('▶')[0].split("기자]")[1].strip()

    return news_title, news_sub_title, news_content


def get_sentences(text):
    sentences = re.split(r'[\.\?\!]\s+', text)
    return sentences


news_title, news_sub_title, news_content = get_article(
    'http://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=277&aid=0004164498')

f = open('bitcoin_news.txt', mode='w', encoding='utf-8')
f.write('%s\n' % news_title)
f.write('%s\n' % news_sub_title)
f.write('%s' % news_content)
f.close()

f_read = open('bitcoin_news.txt', mode='r', encoding='utf-8')
title, sub_title, content = f_read.read().split("\n")

# 기호 제거
filtered_content = content.replace('.', ' ').replace(',', ' ').replace("'", "").replace('·', ' ').replace(
    '=', ' ').replace('"', '').replace('(', ' ').replace(')', ' ').replace('?', ' ')

twitter = Twitter()

# Dictionary 추가
sents = get_sentences(content)
noun_extractor = LRNounExtractor_v2(verbose=True)
nouns = noun_extractor.train_extract(sents)

for noun in nouns:
    twitter.add_dictionary(noun, 'Noun')

# 명사 추출
Noun_words = twitter.nouns(filtered_content)

# 불용어 제거
stopwords = ['기자', '김철현']  # 기자와 관련된 내용으로 기사 내용과 무관하므로 제거

unique_Noun_words = set(Noun_words)

for word in unique_Noun_words:
    if word in stopwords:
        while word in Noun_words: Noun_words.remove(word)

print(Noun_words)
