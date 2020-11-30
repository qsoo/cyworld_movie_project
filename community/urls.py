from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # 전체 페이지 조회
    path('reviews/', views.index, name='index'),
    # 리뷰 생성하기
    path('reviews/create/', views.create, name='create'),
    # 리뷰 자세히 보기
    path('reviews/<int:review_pk>/', views.detail, name='detail'),
    # 리뷰 수정하기
    path('reviews/<int:review_pk>/update/', views.update, name='update'),
    # 리뷰 삭제
    path('reviews/<int:review_pk>/delete/', views.delete, name='delete'),

    # 리뷰에 댓글 달기
    path('reviews/<int:review_pk>/comments/', views.create_comment, name='create_comment'),
    # 댓글 삭제
    path('reviews/<int:review_pk>/comments/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    
    
    
    # 스크랩 요청 보내기
    path('reviews/<int:review_pk>/my_scrap_reviews/', views.user_scraped_reviews, name="user_scraped_reviews"),
]
