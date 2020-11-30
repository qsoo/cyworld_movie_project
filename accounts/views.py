from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

from .models import User, SendConnect, VisitorBook
from .forms import CustomUserCreationForm, CustomUserChangeForm, VisitorBookForm, CustomAuthenticationForm

# 영화목록에 이용할 모델 불러오기
from movies.models import Movie
from community.models import Review


def signup(request):
    # 로그인 유저가 회원가입 접근했을 때
    if request.user.is_authenticated:
        # 리다이렉트 시키려면 데이터 넘겨줘야 한다
        return redirect('accounts:firstpage', request.user.username)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # 로그인 완료시켜주면 회원가입한 뒤 회원가입 누르면 이동됨 이를 막기 위해 제거
            # auth_login(request, user)
            return redirect('accounts:login') # 일단 이렇게 둠 
    else: 
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 로그인이 첫 페이지
def login(request):

    # 로그인 상태로 접근하면 되돌려주기
    if request.user.is_authenticated:
        # 리다이렉트 시키려면 데이터 넘겨줘야 한다
        return redirect('accounts:firstpage', request.user.username)

    else:
        #  POST 요청일 때
        if request.method == 'POST':
            form = CustomAuthenticationForm(request, request.POST)

            if form.is_valid():
                auth_login(request, form.get_user())
                # form에 저장된 user 정보를 꺼내서
                user = form.get_user()
                # 같이 넘겨준 다음 첫 화면을 띄운다
                return redirect('accounts:firstpage', user)
        else:
            form = AuthenticationForm()
            
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)

    return redirect('accounts:login')


# 로그인 후 처음으로 만나는 화면
@login_required
def firstpage(request, username):
    # 사용자 정보 가져오기
    host_user = get_object_or_404(get_user_model(), username=username)
    # 사용자 정보를 바탕으로 방명록 글 가져오기
    visitorbooks = VisitorBook.objects.filter(host=host_user.pk).order_by('-pk')
    
    # 스크랩, 영화목록/댓글/작성한글 가져오기

    # 영화리뷰들 가져오기 - 5개만
    reviews = Review.objects.order_by('-pk')[:5]

    # 나와 관련된 정보 불러오기
    # 프로필을 띄운 화면이 메인 페이지가 될 테니까 
    context = {
        'host_user': host_user,
        'visitorbooks': visitorbooks,
        'reviews': reviews,
    }

    return render(request, 'accounts/profile.html', context)


# 내 프로필 정보
@login_required
def mypage(request, username):
    # 해당 페이지의 주인의 정보를 가져와야 한다
    host_user = get_object_or_404(User, username=username)

    # 1. 찜한 영화목록 출력을 위해
    my_movie_list = host_user.mymovie.all()
    # 2. 일촌목록 출력을 위해
    my_friend_list = host_user.connected.all()
    # 3. 내가 스크랩한 글 목록
    my_scrap_list = host_user.scrap_reviews.all()
    
    context = {
        'host_user': host_user,
        'my_movie_list': my_movie_list,
        'my_friend_list': my_friend_list,
        'my_scrap_list': my_scrap_list,
    }

    return render(request, 'accounts/mypage.html', context)



# 내 정보 수정(회원정보 수정)
@login_required
@require_http_methods(['GET', 'POST'])
def myinfo_change(request, username):
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('accounts:mypage', request.user.username)
        else:
            form = CustomUserChangeForm(instance=request.user)
        
        context ={
            'form': form,
        }
        return render(request, 'accounts/modify_member_info.html', context)


# 스크랩한 글 목록
@login_required
def scrap(request, username):
    # 현재 미니홈피 주인
    host_user = get_object_or_404(User, username=username)
    # 지금 로그인한 사람
    context ={
        'host_user': host_user,
    }
    return render(request, 'accounts/my_scrap.html', context)


# 일촌 목록
@login_required
def linkedin(request, username):
    host_user = get_object_or_404(User, username=username)
    # 조회하는 사람과 프로필 페이지 주인 
    from_user = request.user

    # 전체 신청 중에서 현재 페이지 주인이 take_user에 있으면서 로그인한 사용자가 give_user에 있으면 신청 보낸 상태
    # 이 개수가 존재하면 일촌 신청을 보낸 상태이다
    send_num = SendConnect.objects.filter(give_user=from_user, take_user=host_user).count()
    if send_num:
        is_send = True
    else:
        is_send =False

    # 일촌목록을 보여주려면 전체 리스트를 가져와야한다
    # 1. 신청이 들어온 요청들
    sending_connect = SendConnect.objects.filter(take_user=host_user)

    # 일촌평 작성 폼
    visitorbook_form = VisitorBookForm()
    visitorbooks = VisitorBook.objects.filter(host=host_user).order_by('-pk')
    
    context = {
                'from_user': from_user,
                'host_user': host_user,
                # 요청 보냈는지 여부 확인
                'is_send': is_send,
                # 요청 받은 것 확인
                'sending_connects': sending_connect,
                # 일촌평 작성부분
                'visitorbook_form': visitorbook_form,
                # 작성된 일촌평들
                'visitorbooks': visitorbooks,
    }
    
    return render(request, 'accounts/connection_list.html', context)


# 일촌 신청 보내기
@login_required
def send_connected(request, username):
    # 로그인한 유저인지 확인
    if request.user.is_authenticated:
        # 1. 현재 로그인된 사용자 정보를 가져온다(from)
        from_user = request.user
        # 2. 현재 접속한 페이지의 주인 정보를 가져온다(to)
        host_user = get_object_or_404(User, username=username)

        # 2-1. 요청자 != 나일 때
        if from_user != host_user:

            # 3. 요청을 보내고 연결해준다(POST)
            send_connecting = SendConnect(
                give_user = from_user,
                take_user = host_user, 
                )
            # 모델에 저장
            send_connecting.save()

            # 요청을 보냈으니 불리안을 True로
            is_send = True


            # 넘겨줄 데이터
            context = {
                'from_user': from_user,
                'host_user': host_user,
                'is_send': is_send,
            }

        return render(request, 'accounts/connection_list.html', context)
    
    else:
        return render(request, 'accounts/login.html')


# 일촌 수락하기 - 수락할(take) 사람, 일촌 신청 테이블에서 삭제(pk)
# 신청당한사람/연결/신청보낸사람
@login_required
def connected_complete(request, to_username, from_username, send_connect_pk):
    # POST
    # 1. 일촌 수락버튼을 클릭한다 => connected 필드 True로 변경
    give_user = get_object_or_404(get_user_model(), username=from_username)
    take_user = get_object_or_404(get_user_model(), username=to_username)

    take_user.connected.add(give_user)

    # 2. 일촌 신청 테이블에서 삭제한다.
    send_connect = get_object_or_404(SendConnect, pk=send_connect_pk)
    send_connect.delete()

    return redirect('accounts:linkedin', take_user.username)


# 일촌평 작성 - 페이지 주인(아이디) / 사용자(아이디)
@login_required
@require_http_methods(['GET', 'POST'])
def visitor_book_create(request, host, writer):
    # POST 요청일 때
    host_user = get_object_or_404(get_user_model(), username=host)

    if request.method == 'POST':
        form = VisitorBookForm(request.POST)

        if form.is_valid():
            # 외래키 연결
            visitor_book = form.save(commit=False)
            visitor_book.host = host_user
            visitor_book.writer = request.user
            visitor_book.save()

            return redirect('accounts:linkedin', host)

    else:
        linkedin(request, host)


# 내 영화목록 조회 - 추가한 영화 목록과 검색기능(DB)
@login_required
def my_movie_list(request, username):
    # 1. 영화 전체 리스트를 가져온다
    movies = Movie.objects.all()
    # 2. 검색어가 있을 때는 해당 쿼리셋도 가져온다
    search_movie = request.GET.get('search_movie')
    
    host = get_object_or_404(User, username=username)
    # 5. 나의 영화리스트 정보 가져오기
    
    # 검색한 뒤인지 검색안했는지 판별할 bool
    is_search = False

    if search_movie:
        search_movie_list = movies.filter(title__icontains=search_movie)
        is_search = True

    else:
        search_movie_list = '결과없음'
    # 4. 검색 결과에서 클릭을 하면 내가본영화 모델에 들어간다

    # 3. 담아서 넘겨준다. -username (내 영화리스트에 넣기 위해 필요)
    context = {
        'search_movie': search_movie,
        'search_movie_list': search_movie_list,
        'username': username,
        'host': host,

    }
    return render(request, 'accounts/my_movie_list.html', context)


# 내 영화목록에 추가
@login_required
def add_mymovie_list(request, username, movie_pk):
    # 넘겨받은 데이터를 바탕으로 모델에 저장 - 존재하지 않을 때
    user = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if not user.mymovie.filter(pk=movie_pk).exists():  
        user.mymovie.add(movie)
    return redirect('accounts:my_movie_list', username)


# 내 영화목록에서 제거
@login_required
def remove_mymovie_list(request, username, movie_pk):
    user = get_object_or_404(User, username=username)
    movie = get_object_or_404(Movie, pk=movie_pk)
    # 존재하면 빼주자
    if user.mymovie.filter(pk=movie_pk).exists():  
        user.mymovie.remove(movie)
    return redirect('accounts:my_movie_list', username)