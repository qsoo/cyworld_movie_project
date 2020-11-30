from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import get_user_model

from django.db.models import Count, Max, Min

from accounts.models import User
from .models import Movie



# Create your views here.
@require_GET
def index(request):
    movies = Movie.objects.all()
    # 영화 검색기능
    search_movie = request.GET.get('search_movie')
    # 사용자 정보 넘겨주기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)
    if search_movie:
        search_movie_list = movies.filter(title__icontains=search_movie)

    else:
        search_movie_list = '결과없음'

    context = {
        'search_movie': search_movie,
        'movies': movies,
        'search_movie_list': search_movie_list,
        'host_user': host_user,
    }
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    # 사용자 정보 넘겨주기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)

    context = {
        'movie': movie,
        'host_user': host_user,
    }
    return render(request, 'movies/detail.html', context)


def recommend(request):
    # 현재 로그인된 사용자 정보 가져오기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)

    # 내 일촌 중 일촌평 가장 많이 남긴 사람이 누구인지 가져오기
    who_is_my_best_friend = host_user.host_book.values('writer').annotate(count_book=Count('host')).order_by('-count_book').first()

    # 이를 바탕으로 사용자 인스턴스 가져와서 넘겨주기
    my_best_friend = get_object_or_404(get_user_model(), pk=who_is_my_best_friend['writer'])

    # my_best_friend =''

    context ={
        'my_best_friend': my_best_friend,
        'host_user': host_user,
    }
    '''        
    # 1. 로그인한 유저의 일촌에서 선호 영화 가져오기 - 3개정도만 보여주기

    # 2. 일촌정보 가져와서 일촌평 가장 많이 쓴 사람에서 평점 높은거 

    # 3. 스크랩한 글 가장 많은 작성자 선호영화 => 추천

    # 4. 1&2&3을 종합해서 추천
    '''


    return render(request, 'movies/recommend.html', context)