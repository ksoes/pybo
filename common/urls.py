from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'), # django.contrib.auth 앱의 LoginView를 사용
    # LoginView가 common 디렉터리의 템플릿을 참조할 수 있도록 common/urls.py 파일을 다음과 같이 수정
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup')
]