from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 로그인 페이지가 첫 페이지
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    # 로그인 후 처음 마주친는 첫 개인 페이지 - 닉네임으로 바꾸자
    path('<str:username>/', views.firstpage, name="firstpage"),

    # 여기부터는 내 정보 페이지
    path('<str:username>/mypage/', views.mypage, name="mypage"),
    # 회원정보수정
    path('<str:username>/mypage/myinfo_change/', views.myinfo_change, name="myinfo_change"),
    # 스크랩한 글 목록 조회
    path('<str:username>/mylist/', views.scrap, name="scrap"),
    
    # 내가 본 영화목록 조회 - 검색기능 탑재
    path('<str:username>/my_movie_list/', views.my_movie_list, name='my_movie_list'),

    # 내 영화 목록에 추가
    path('<str:username>/my_movie_list/add/<int:movie_pk>/', views.add_mymovie_list, name='add_mymovie_list'),

    # 내 영화 목록에서 제거
    path('<str:username>/my_movie_list/remove/<int:movie_pk>/', views.remove_mymovie_list, name='remove_mymovie_list'),

    # 일촌 목록 조회
    path('<str:username>/my_connection_list/', views.linkedin, name="linkedin"),

    # 여기부터는 일촌관련 내용

    # 일촌신청 메세지 보내기
    path('<str:username>/send_connected/', views.send_connected, name="send_connected"),
    # 일촌 수락하기 : to - page 주인 from - 신청한 사람
    path('<str:to_username>/connected/<str:from_username>/<int:send_connect_pk>/', views.connected_complete, name="connected_complete"),
    # 일촌평 작성
    path('visitor_book/<str:host>/<str:writer>/', views.visitor_book_create, name='visitor_book_create'),

]
