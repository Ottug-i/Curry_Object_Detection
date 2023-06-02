# -*- coding: utf-8 -*-
"""Data_Crawling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jZ0h4kmKtzarWxNkrOHRjZwlfgyC_x3X

# 공공 데이터 가져오기
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np

# 만개의 레시피 공공 데이터 불러오기
recipe = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/크롤링/recipe.csv', encoding='cp949')

# 인덱스 설정
recipe.set_index('id', inplace = True)

# 추가 정보 열 추가
recipe['thumbanil'] = ''
recipe['time'] = ''
recipe['orders'] = ''
recipe['photo'] = ''

# 레시피 id 리스트
id_list = recipe.index.to_list()

recipe

"""# 공공 데이터에 크롤링 정보 추가하기"""

!pip install BeautifulSoup4

import requests
from bs4 import BeautifulSoup
import re

!pip install pyOpenSSL
import ssl

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 레시피 id로 레시피 추가 정보 크롤링
def RecipeCrawler(recipeId):
    
    url = f'https://www.10000recipe.com/recipe/{recipeId}'

    response = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, verify=False)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 레시피 썸네일
    try:
        thumbnail = soup.select_one('#contents_area > div.view2_pic > div.centeredcrop img')['src']
        recipe.loc[recipeId,'thumbanil'] = thumbnail
    except TypeError:
        recipe.loc[recipeId,'thumbanil'] = ''
    pass

    # 레시피 시간
    try:
        time = soup.select_one('#contents_area > div.view2_summary.st3 > div.view2_summary_info > span.view2_summary_info2').get_text()
        recipe.loc[recipeId,'time'] = time
    except AttributeError:
        recipe.loc[recipeId,'time'] = ''
    pass

    # 레시피 조리 순서
    try:
        elements = soup.find_all('div', 'view_step_cont')
        tmp = ''
        for i, element in enumerate(elements, start=1):
            order = element.find('div', 'media-body')
            order = ''.join(order.findAll(string=True, recursive=False)).strip() # 조리 순서에서 설명, 주방 도구 제외
            tmp = tmp + ('|' + str(i) + '. ' + order)
        recipe.loc[recipeId,'orders'] = tmp
    except AttributeError:
        recipe.loc[recipeId,'orders'] = ''
    pass

    # 레시피 조리 사진
    try:
        elements = soup.find_all('div', 'view_step_cont')
        tmp = ''
        for i, element in enumerate(elements, start=1):
            try:
                photo = element.find('img')['src']
                tmp = tmp + ('|' + photo)
            except TypeError:
                tmp = tmp + ('|' + ' ')
            pass
        recipe.loc[recipeId,'photo'] = tmp
    except AttributeError:
        recipe.loc[recipeId,'photo'] = ''
    pass

for i, id in enumerate(id_list, start=1):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

# 끊긴 레시피부터 다시
for i, id in enumerate(id_list[832:], start=833):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

# 끊긴 레시피부터 다시
for i, id in enumerate(id_list[1677:], start=1678):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

# 끊긴 레시피부터 다시
for i, id in enumerate(id_list[2212:], start=2213):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

# 끊긴 레시피부터 다시
for i, id in enumerate(id_list[2907:], start=2908):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

# 끊긴 레시피부터 다시
for i, id in enumerate(id_list[3667:], start=3668):
    print(str(i) + "번째 크롤링 id: " + str(id))
    RecipeCrawler(id)

recipe

"""# CSV 파일 내보내기"""

# csv 파일 내보내기
recipe.to_csv('curry_recipe.csv', encoding='utf-8-sig')