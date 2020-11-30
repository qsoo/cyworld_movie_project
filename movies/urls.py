from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    # 영화추천 시스템 구축
    path('recommend/', views.recommend, name='recommend'),
]
