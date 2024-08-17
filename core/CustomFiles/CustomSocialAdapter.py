from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    super(CustomSocialAccountAdapter).__init__(DefaultSocialAccountAdapter)
    pass