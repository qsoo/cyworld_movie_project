from django.db import models
from django.conf import settings

from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    title = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    # 평점 범위 설정
    rank = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 스크랩 필드
    scrap_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='scrap_reviews')


class Comment(models.Model):
    content = models.CharField(max_length=255)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
