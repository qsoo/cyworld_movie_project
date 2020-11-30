# 필요한 라이브러리 불러오기
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
import pandas as pd


# 카테고리/최신영화/판매량 순 정렬 base 주소
SEARCH_URL = 'https://series.naver.com/movie/recentList.nhn?orderType=sale&sortingType=&tagCode=&page='

# 네이버 시리즈의 베이스 url
series_base_url = "https://serieson.naver.com"


# 네이버 시리즈 영화 정보 가져오는 코드 => pageno 매개변수 넣고 하기
def get_page_links(page_range:int):
    # page링크들을 저장할 리스트
    links = []

    # 여기서 반복문으로 각각의 영화의 링크 주소만 가져오기
    for page_no in range(1, page_range+1):

        # 공통으로 사용할 거기 때문에 한번만 만들어주기 - html doc
        html_doc = requests.get(SEARCH_URL + str(page_no))

        # bs로 빼오기
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        
        # 시리즈의 영화정보 링크 가져오기 - 여러개
        movie_links = soup.find_all('a', {'class': 'NPI=a:content'})

        # 여기서 페이지 내의 영화들의 상세정보 주소만 가져오기
        for movie_link in movie_links:
            # 쿼리스트링으로 붙는 url 가져오기
            href = movie_link.get('href')
            links.append(series_base_url+href)

    # ------------- 여기까지가 시리즈온 상세정보 링크 가져오기 ---------- #

    # 네이버 영화링크들 리스트
    naver_movie_links = []

    for link in links:
        # 위와 같이 반복
        movie_info_html = requests.get(link)
        # 시리즈의 디테일 페이지 파싱
        soup_movie_info = BeautifulSoup(movie_info_html.text, 'html.parser')
        # 성인인증 - 로그인 필요 피해가자
        try:
            naver_movie_link = soup_movie_info.find('a', {'class': 'NPI=a:info'}).get('href')

            naver_movie_links.append(naver_movie_link)
        except:
            continue
    
    # 길이 비교 - 성인영화 몇개인지
    # print(len(links))
    # print(len(naver_movie_links))

    # --------- 여기까지가 네이버 영화 링크 가져오기 ------------ #

    return naver_movie_links


# 필요한 정보 가져오기
def get_movie_data(links:list):

    # 필요한 정보: 제목, 감독, 개요(장르), 이미지, 줄거리
    titles = []
    directors = []
    genres = []
    nations = []
    posters = []
    contents = []

    # 장르 정보 필터링해줄 정규식 작성
    genre_regex = re.compile('genre')
    # 제작 나라 정보 필터링해 줄 정규식 작성
    nation_regex = re.compile('nation')

    # 각각의 네이버 영화정보 주소로 접근
    for link in links:
        
        naver_movie_info = requests.get(link)
        soup = BeautifulSoup(naver_movie_info.text, 'html.parser')
        title = soup.select_one('div.mv_info > h3.h_movie > a')
        # title 목록에 저장
        titles.append(title.text)

        # director 목록에 저장
        director = soup.select_one('dl.info_spec > dd > p > a')
        directors.append(director.text)

        # 여기서 선택된 태그내에 장르, 국가 정보 포함 
        temps = soup.select('dl.info_spec > dd > p > span > a')
        temp_genres = []
        temp_nations = []

        for temp in temps:
            temp_href = temp.get('href')
            # 장르여부 판단
            is_genre = genre_regex.search(temp_href)
            # 제작국가여부 판단
            is_nation = nation_regex.search(temp_href)

            if is_genre:
                temp_genres.append(temp.text)

            elif is_nation:
                temp_nations.append(temp.text) 

        # 리스트형태로 append 시켜줬기 때문에 국가정보 확인해서 str 바꿔서 저장하기
        genres.append(temp_genres)
        nations.append(temp_nations)

        # 줄거리 가져오기
        content = soup.select_one('div.story_area > p.con_tx')

        # 줄거리가 없는 경우 걸러주기
        if not content:
            contents.append("줄거리 오류")

        # 줄거리 정제
        else:
            content_text = content.text
            # \r(줄바꿈 문자 걸러주기)
            content_text = content_text.replace('\r', '')
            # \xa0: NBSP(non-breaking space), 단어 줄바꿈 걸러주기
            content_text = content_text.replace('\xa0', '')
            contents.append(content_text)
        

        # 이미지 가져오기
        poster = soup.select_one('div.poster > a > img')
        poster_url = poster.get('src')
        # 뒤에 쿼리스트링으로 사이즈가 고정되어있어서 원본 가져오기 위해 정제
        poster_url = re.sub('\?.*', '', poster_url)

        posters.append(poster_url)

        #  --------- 여기까지가 필요한 정보 가져오는 부분 -------- #
        
    # 이를 dictionary 형태로 저장하자 
    # 제목, 감독, 개요(장르), 이미지, 줄거리
    movie_dic = {
        '제목': titles,
        '감독': directors,
        '장르': genres,
        '국가': nations,
        '이미지': posters,
        '줄거리': contents
    }

    # 일단 df로 만들어보자
    movie_df = pd.DataFrame(movie_dic)

    return movie_df

ex1 = get_movie_data(['http://movie.naver.com/movie/bi/mi/basic.nhn?code=150198'])

# # csv 파일로 저장
# def df_to_csv(movie_df): 
#     # 인코딩 utf-8로 하면 오류 발생
#     movie_df.to_csv(('movie_data'+'.csv'), sep=',', na_rep='NaN', encoding='euc-kr')
# # 20 page까지 가져오면 384개정도 된다!

# ----- 여기까지가 크롤링 함수 ----------- #

# 장고 모델에 연결해서 불러오기
import os
# python이 실행될 때 manage.py에 있는 구동환경을 장고 프로젝트와 연결
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')
import django
django.setup()

# 모델 불러오기
from movies.models import Movie


# python 직접 실행할 경우 아래 코드 작동 - 탐색 페이지 숫자만 바꾸자
if __name__=='__main__':
    # 위에서 만든 함수들을 불러와서 실행
    movie_df = get_movie_data(get_page_links(2))

    # 행별로 순회하면서 모델에 넣어주기
    for index, row in movie_df.iterrows():
        Movie(
            title = row['제목'],
            director = row['감독'],
            genres = row['장르'],
            nations = row['국가'],
            poster = row['이미지'],
            content = row['줄거리']
        ).save()
