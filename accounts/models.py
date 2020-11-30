from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 내 영화목록을 만들기 위해 모델 불러오기
from movies.models import Movie


# 사용자 프로필 파일에 이름을 지어서 저장하자
def profile_img_path(instance, filename):
    # 저장할 주소는 BASE_DIR의 media/user_id/filename
    print(instance)
    return f'user_{instance}/{filename}'

# 사용자 모델에서 필요한 요소 - 아이디, 비밀번호, 닉네임, 이메일
class User(AbstractUser):
    email = models.EmailField(
        # 관리자페이지에서 보여질 부분
        verbose_name = '이메일',
        max_length = 255,
        unique = True,
    )
    nickname = models.CharField(
        verbose_name = '닉네임',
        max_length = 30,
        unique=True,
    )
    greetings = models.CharField(
        verbose_name= '인사말',
        max_length= 50,
        null = True, 
        blank = True,
    )
    # 일촌 필드
    connected = models.ManyToManyField('self', symmetrical=True)
    # 프로필이미지필드 추가 - 빈값으로 생성가능하고, 빈 폼도 제출가능
    # 사진 들어가는 것 확인하고 blank=True로 변경
    profile_img = models.ImageField(
        null = True, 
        blank = True,
        verbose_name = '프로필사진',
        upload_to = profile_img_path
        )

    # 나의 영화리스트
    mymovie = models.ManyToManyField(Movie)
    

# 일촌 신청 테이블 (누가, 누구한테, 신청수락여부)로 구성
class SendConnect(models.Model):
    # 요청을 보낸 사용자 아이디
    give_user = models.CharField(max_length=255)
    # 요청을 받은 사용자 아이디
    take_user = models.CharField(max_length=255)
    # 요청을 수락한다면 테이블에서 지우자 - 생성시 true로
    sure = models.BooleanField(default=True)


# 일촌들의 방명록 작성 
# 내용 작성일, 페이지주인, 작성자, 생성일, 수정일
class VisitorBook(models.Model):
    content = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 일촌평의 주인은 1명 - 게시글은 여러개
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='host_book')
    # 작성자 id 정보를 저장할 것이기 때문에 반대에서는 소유자
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writer_book')
