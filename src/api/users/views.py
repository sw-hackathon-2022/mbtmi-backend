import time

from dj_rest_auth.serializers import JWTSerializer
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import api_view, action

import users
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from django.shortcuts import redirect
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from users.models import User
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status, serializers

BASE_URL = f"http://{settings.API_HOST}:8000"


@extend_schema(
    tags=["/users"],
    operation_id="카카오 로그인",
    methods=["get"],
    responses={
        302: OpenApiResponse(
            response={}, description="Redirect to kakao"
        )
    },
)
@api_view(["GET"])
def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}"
        f"&redirect_uri={settings.KAKAO_REDIRECT_URL}&response_type=code"
    )


@extend_schema(
    tags=["/users"],
    operation_id="카카오 로그인 (callback)",
    methods=["get"],
    parameters=[
        OpenApiParameter(
            name="code",
            description="인가 코드",
            type=str,
            location=OpenApiParameter.QUERY,
            response=True,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=JWTSerializer, description="카카오 로그인 성공"
        )
    },
)
@api_view(["GET"])
def kakao_callback(request):
    rest_api_key = settings.KAKAO_REST_API_KEY
    code = request.GET.get("code")
    redirect_uri = settings.KAKAO_REDIRECT_URL
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}"
        f"&redirect_uri={redirect_uri}&code={code}",
        headers={"Content-type": "application/json;charset=utf-8"},
    )

    token_req_json = token_req.json()
    token_req.close()

    access_token = token_req_json.get("access_token")
    """
    Profile Request
    """
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    profile_request = session.get("https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/json;charset=utf-8"
                },
    )
    profile_json = profile_request.json()
    session.close()
    username = profile_json.get("id")
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
        accept.close()
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}/users/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)


@extend_schema(
    tags=["/users"],
    operation_id="카카오 회원가입",
    request=inline_serializer(
        name="KakaoSignUpSerializer",
        fields={
            "accessToken": serializers.CharField(),
            "code": serializers.CharField(),
        }
    ),
    responses={
        200: OpenApiResponse(
            response=JWTSerializer, description="카카오 회원가입 성공"
        )
    },
)
class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = settings.KAKAO_REDIRECT_URL
