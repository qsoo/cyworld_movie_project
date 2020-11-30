from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

from .models import Review, Comment
from .forms import ReviewForm, CommentForm

from django.db.models import Q


# 전체 리뷰 조회
@login_required
def index(request):
    reviews = Review.objects.order_by('-pk')

    # 리뷰 검색기능
    search_review = request.GET.get('search_review')

    # 사용자 정보 넘겨주기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)

    # 제목, 영화제목, 내용 포함해서 검색
    if search_review:
        search_review_list = reviews.filter(Q(title__icontains=search_review) | Q(content__icontains=search_review) | Q(movie_title__icontains=search_review))

    else:
        search_review_list = '결과없음'

    context = {
        'reviews': reviews,
        'search_review': search_review,
        'search_review_list': search_review_list,
        'host_user': host_user,
    }
    return render(request, 'community/index.html', context)


# 리뷰 작성
@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('community:detail', review.pk)
    else:
        form = ReviewForm()

    # 사용자 정보 넘기기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)

    context = {
        'form': form,
        'host_user': host_user,
    }
    return render(request, 'community/create.html', context)


# 세부 페이지 조회
@login_required
def detail(request, review_pk):
    
    review = get_object_or_404(Review, pk=review_pk)
    comments = review.comment_set.all()
    comment_form = CommentForm()
    # 사용자 정보 넘기기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
        'host_user': host_user,
    }
    return render(request, 'community/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('community:detail', review_pk)

    else:
        form = ReviewForm(instance=review)

    # 사용자 정보 넘기기
    host_user = get_object_or_404(get_user_model(), pk=request.user.pk)

    context = {
        'form': form,
        'review': review,
        'host_user': host_user,
    }

    return render(request, 'community/update.html', context)


@login_required
def delete(request, review_pk):
    # 로그인한 유저이면
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
    
    return redirect('community:index')


@login_required
def user_scraped_reviews(request, review_pk):
    
    # 인증된 유저인지 확인
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        
        # 이미 스크랩했다면 제거
        if review.scrap_users.filter(pk=user.pk).exists():
            review.scrap_users.remove(user)

        else:
            review.scrap_users.add(user)

        return redirect('community:detail', review_pk)


# 댓글 생성
@login_required
@require_http_methods(['GET', 'POST'])
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        return redirect('community:detail', review_pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


# 댓글 삭제
@login_required
def delete_comment(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('community:detail', review_pk)