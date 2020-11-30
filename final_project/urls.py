"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# static 등록을 위해 사용
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),
    # 홈 화면 - 로그인 화면 로그인 후 넘어갈 화면 연결
    path('accounts/', include('accounts.urls')),
    path('community/', include('community.urls')),
    path('movies/', include('movies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
