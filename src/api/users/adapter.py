from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class UserAdapter(DefaultSocialAccountAdapter):
    """Custom Social Account Adapter"""

    def populate_user(self, request, sociallogin, data):
        """Set fields of the user object"""
        response = sociallogin.account.extra_data
        # Naver: if user sign in with naver account
        if sociallogin.account.provider == "kakao":
            uid = response.get("id")
        user = sociallogin.user
        user_field(user, "username", str(uid))
        return user
