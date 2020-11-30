from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms

from .models import VisitorBook, User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('email', 'nickname', 'profile_img')


# 회원정보 수정에 필요한 필드 구성
class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = ('nickname', 'email', 'greetings', 'profile_img')
        excludes = ('password',)

# 일촌평 작성에 필요한 필드
class VisitorBookForm(forms.ModelForm):
    
    class Meta:
        model = VisitorBook
        fields = ['content']


class CustomAuthenticationForm(AuthenticationForm):
    # 현재 라벨 적용안됨 => 불러오는게 잘못된 것 같기도 함
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '아이디를 입력해주세요'
            }),
            'password': forms.TextInput(attrs={
                'placeholder': '비밀번호를 입력해주세요'
            }),
        },
        labels = {
            'username': '아이디',
            'password': '비밀번호',
        }