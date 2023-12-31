# -*- coding: utf-8 -*-
"""data_preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mpgHVqqQWqksTX0GONuLgwkZ0qjeJxcX
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import re

"""# 데이터 불러오기"""

# youtube_df 불러오기
youtube_df = pd.read_csv('C:/Users/rnjst/Desktop/DSL/Modeling_Project/Youtube_script_crawling/youtube_df.csv', index_col=0)

"""# 크롤링 데이터 전처리

## 불필요한 열(댓글 수, 좋아요 수) 삭제
"""

# 불필요한 열(댓글 수, 좋아요 수) 삭제
youtube_df = youtube_df.drop(['댓글 수', '좋아요 수'], axis=1)

"""## 조회수 열 전처리"""

# 조회수 전처리 함수(str -> int)
def view(x):
    try:
        y = int(x[4:-1].replace(",", ""))
        return y
    except:
        return None

youtube_df['조회수'] = youtube_df['조회수'].apply(view)

"""## 날짜 열 전처리"""

# 날짜 전처리 함수(str -> datetime)
def date(x):
    try:
        if ":" in x:
            y = pd.to_datetime(x[14:])
        else:
            y = pd.to_datetime(x)
        return y
    except:
        return None

youtube_df['날짜'] = youtube_df['날짜'].apply(date)

# youtube_df 저장
youtube_df.to_csv('C:/Users/rnjst/Desktop/DSL/Modeling_Project/Youtube_script_crawling/youtube_df_fin.csv', encoding='utf-8-sig')

"""# 스크립트 텍스트 전처리"""

data = pd.read_csv('/content/drive/MyDrive/DSL/2023-2/Modeling_Project/data/youtube_df_fin.csv', index_col=0)

"""## 불용어 제거"""

stop_words_list = ['아', '으', '어', '오', '요', '음', '오오오']

def stop_words_remove(text):
  text = str(text)

  # 불용어 제거([음악], [박수], '\n', '*')
  text = text.replace('[음악]', '')
  text = text.replace('[박수]', '')
  text = text.replace('\n', '')
  text = text.replace('*', '')

  # 한 글자 불용어 및 숫자, 알파벳 제거를 위한 단어 토큰화
  tok = text.split(' ')
  tok = [i for i in tok if i != ''] # 공백값 제거
  new_tok = []

  # 한 글자 불용어 및 한 글자 숫자&알파벳 제거
  for temp in tok:
    if temp not in stop_words_list:
      if len(temp) == 1 and (temp.isdecimal() or temp.isalpha()):
        pass
      else:
        new_tok.append(temp)

  return new_tok # 단어 토큰이 든 list return

# 기존 데이터프레임에 단어 토큰이 든 list를 넣을 열 추가
data['script tok'] = ''

# 스크립트 불용어 처리
data['script tok'] = data['스크립트'].apply(stop_words_remove)

"""## 문장 토큰화"""

# 종결어미를 활용한 문장 단위 토큰화(데이터가 너무 많아서 문장분리 알고리즘 사용 불가..시간 이슈..)
endlist = ['지요','게요', '예요', '니다', '이죠', '어요', '구요', '거죠', '아요','네요',
           '겠죠', '봐요', '되죠', '돼요', '되요', '든요', '나요', '해요','가요','이에요',
           '거에요','렇죠', '세요', '하죠', '까요', '구나', '데요', '이다', '에요']

def sentence_tok(tok_list):
  text_list = []
  current_sentence = []

  for tok in tok_list:
    if any(end in tok for end in endlist):
      current_sentence.append(tok)
      text_list.append(' '.join(current_sentence))
      current_sentence = []
    else:
      current_sentence.append(tok)

  if current_sentence:
    text_list.append(' '.join(current_sentence))

  return text_list # 문장 토큰이 든 list return

# 기존 데이터프레임에 문장 토큰이 든 list를 넣을 열 추가
data['script sent tok'] = ''

# 스크립트 문장 토큰화
data['script sent tok'] = data['script tok'].apply(sentence_tok)

# 문장 토큰화 결과 저장
data.to_csv('/content/drive/MyDrive/DSL/2023-2/Modeling_Project/data/youtube_data_for_sent_analysis.csv', encoding='utf-8-sig')