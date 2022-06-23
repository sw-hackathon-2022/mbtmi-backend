from django.urls import path

from users import views

urlpatterns = [
    # 카카오 로그인
    path('login/', views.kakao_login, name='카카오 로그인'),
    path('login/callback/', views.kakao_callback, name='카카오 로그인 콜백'),
    path('login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
]
