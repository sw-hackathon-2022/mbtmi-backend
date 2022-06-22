from django.urls import path

from users import views

urlpatterns = [
    # 카카오 로그인
    path('users/login/', views.kakao_login, name='카카오 로그인'),
    path('users/login/callback/', views.kakao_callback, name='카카오 로그인 콜백'),
    path('users/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
]
