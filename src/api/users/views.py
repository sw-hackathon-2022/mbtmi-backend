import time

from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from requests.adapters import HTTPAdapter
from rest_framework.generics import UpdateAPIView, get_object_or_404
from urllib3 import Retry

from users.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status

from users.serializers import ProfileSerializer

BASE_URL = f"http://{settings.API_HOST}:80"


def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={settings.KAKAO_REDIRECT_URL}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = settings.KAKAO_REST_API_KEY
    code = request.GET.get("code")
    print(code)
    redirect_uri = settings.KAKAO_REDIRECT_URL
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}"
        f"&redirect_uri={redirect_uri}&code={code}",
        verify=False
    )

    token_req_json = token_req.json()
    access_token = token_req_json.get("access_token")
    """
    Profile Request
    """
    session = requests.Session()
    retry = Retry(connect=10, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    profile_request = session.get("https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
                verify=False
    )
    profile_json = profile_request.json()
    # print(kakao_account)
    # email = kakao_account.get('email', None)

    username = profile_json.get("id")
    mbti = "XXXX"
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(username=username)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'kakao':
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}/users/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}/users/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        print(accept_json)
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.KAKAO_REDIRECT_URL


@extend_schema(
    tags=["/users"],
    operation_id="프로필 등록",
)
class ProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = "patch"

    def get_object(self):
        """Get request user"""
        # Get login user
        obj = get_object_or_404(self.get_queryset(), id=self.request.user.id)
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
