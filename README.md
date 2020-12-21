## 🎫SSAFY world

목차

[0.Intro](#프로젝트-목표)

[1.페이지 소개](#페이지-소개)



### 프로젝트 목표

> 취미로 개발을 하는 그날을 위해 프로젝트를 진행



#### 1. 주제

> SSAFY world

```
싸이월드의 감성을 이어서 B급 웹페이지를 제작해보자 (Kitsch Web Page)
```

* `키치(Kitsch)`라는 단어는 독일어로 '저속품, 유치한 예술 작품'등을 뜻함

----

#### 2. 프로젝트 실행

1. 가상환경 생성 및 활성화

```bash
$ python -m venv venv

# window
$ source venv/Scripts/activate
# Mac / Linux
$ source venv/bin/activate
```

2. 필요한 라이브러리 설치

```bash
$ pip install -r requirements.txt
```

3. 데이터 베이스 적용(현재는 예시 DB가 저장된 상태이기 때문에 생략)

```bash
$ python manage.py makemigrations

$ python manage.py migrate

# (참고) 영화데이터 가져오기
$ python parser_movie.py
```

4. 서버 실행

```bash
$ python manage.py runserver
```



#### 3. 프로젝트 구조

```
│  .gitignore
│  db.sqlite3
│  github_사용법.md
│  manage.py
│  parser_movie.py
│  README.md
│  requirements.txt
│  tree.txt
│      
├─accounts
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │      
│  └─templates
│      └─accounts
│              connection_list.html
│              left_profile.html
│              login.html
│              modify_member_info.html
│              mypage.html
│              my_movie_list.html
│              my_scrap.html
│              profile.html
│              signup.html
│              _left_profile.html
│              _login_background.html
│              _middle_reviews_and_ad.html
│              _right_bgm.html
│              
├─community
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │      
│  └─templates
│      └─community
│              create.html
│              detail.html
│              index.html
│              update.html
│              user_comments.html
│              user_liked_reviews.html
│              user_reviews.html
│              _user_comments.html
│              _user_liked_reviews.html
│              _user_reviews.html
│              
├─final_project
│  │  asgi.py
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │  
│  └─templates
│      │  base.html
│      │  footer.html
│      │  pjt.css
│      │  _menubar.html
│      │  
│      └─images
│              back.jpg
│              back1.jpg
│              back2.jpg
│              
├─media
│          
├─movies
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │      
│  └─templates
│      └─movies
│              detail.html
│              index.html
│              recommend.html
│      
├─static
│          
├─venv
│
└─프로젝트캡쳐
```



#### 4. 모델 소개

![img](README.assets/%EB%AA%A8%EB%8D%B8%EB%A7%81.png)

> accounts app내의 모델은 User, SendConnect, VisitorBook
>
> movie app내의 모델은 Movie
>
> community app내의 모델은 Review, Comment
>
> 로 구성되어 있습니다.

**accounts**

1. User
   - connected: User 모델의 M:N 관계로 일촌 여부를 확인할 수 있는 필드
   - mymovie: 내 찜한 영화목록을 생성하기 위한 Movie 모델과 M:N 관계
2. SendConnect
   - 일촌 신청을 보낸 상태 및 수락을 위해 만든 필드로 일촌 관계가 형성되게 되면 자동적으로 삭제가 됩니다
3. VisitorBook
   - 방명록 작성을 위한 모델로 작성자와 해당 프로필의 주인이 1:M 관계로 User 모델과 연결

**movie**

영화정보를 저장한 모델

**community**

1. Review
   - user:  작성자, User 모델과 1:M 연결
   - scrap_user: 스크랩한 유저들, User 모델과 1:M 연결
2. Comment
   - review: 어느 리뷰의 댓글인지 연결, Review 모델과 1:M 연결
   - user: 댓글 작성자, User 모델과 1:M 연결



### 페이지 소개

1. 로그인 페이지 접속

![img](README.assets/%EB%A1%9C%EA%B7%B8%EC%9D%B8.png)

> 작동 예시를 위한 사용자 데이터로 접속

```
URL: http://127.0.0.1:8000/accounts
위의 URL이 로그인 페이지 접속을 위한 URL입니다.

해당 URL로 이동한 후 
ID: qsoo
PW: !12341234
입력하여 접속
```



2. 내 미니홈피 확인

![img](README.assets/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80.png)

![img](README.assets/%EB%A9%94%EC%9D%B8%ED%8E%98%EC%9D%B4%EC%A7%80_%EC%9D%BC%EC%B4%8C%ED%8F%89.png)

> 로그인 후에는 내 미니홈피로 이동하며 일촌평 및 사용자와 관련된 정보들을 사이드바를 통해 접근가능합니다.

3. 영화목록 페이지 확인

![img](README.assets/%EC%98%81%ED%99%94%EB%AA%A9%EB%A1%9D%ED%8E%98%EC%9D%B4%EC%A7%80.png)

> 영화 목록 페이지에서 크롤링한 영화정보들을 확인할 수  있으며 영화 추천을 받을 수 있는 버튼이 존재

- **영화 추천 시스템 Logic**
  1. 내 일촌들 중 가장 많은 일촌평을 작성한 사용자를 조회
  2. 해당 사용자의 찜 영화 목록으로 접근하여 이를 보여줍니다.

![img](README.assets/%EC%98%81%ED%99%94%EC%B6%94%EC%B2%9C%ED%8E%98%EC%9D%B4%EC%A7%80JPG.JPG)

- 영화검색 기능, 리뷰 검색 기능, 내 찜 목록 영화 검색 기능 구현

![img](README.assets/%EA%B2%8C%EC%9E%84%ED%82%A4%EC%9B%8C%EB%93%9C%EB%A1%9C%EA%B2%80%EC%83%89%ED%95%9C%EC%98%81%ED%99%94%EB%AA%A9%EB%A1%9D%ED%8E%98%EC%9D%B4%EC%A7%80.png)

<center><게임 키워드로 영화 검색></center>

4. 내 프로필 관련 정보

![img](README.assets/%EB%82%B4%ED%94%84%EB%A1%9C%ED%95%84%ED%8E%98%EC%9D%B4%EC%A7%80.png)

<center><내 프로필 요약 정보></center>

![img](README.assets/%EB%82%B4%EC%B0%9C%EB%AA%A9%EB%A1%9D%EB%A6%AC%EC%8A%A4%ED%8A%B8.png)

<center><내가 찜한 영화 목록 리스트></center>

![img](README.assets/%EC%9D%BC%EC%B4%8C%ED%8F%89%ED%8E%98%EC%9D%B4%EC%A7%80.png)

<center><일촌평 페이지></center>

