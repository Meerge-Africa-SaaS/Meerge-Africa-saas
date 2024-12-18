# ruff: noqa: F403,F405

###################################################
############    ALLAUTH SETTINGS     ##############
###################################################

SITE_ID = 1
MOBILE_APP_SCHEME = "app://localhost:5000/"
WEB_APP_SCHEME = "http://localhost:8000/"



ACCOUNT_ADAPTER = "core.CustomFiles.CustomAdapterFile.CustomAccountAdapter"
SOCIALACCOUNT_ADAPTER = "core.CustomFiles.CustomSocialAdapter.MyCustomSocialAccountAdapter"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Meerge Africa"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_CONFIRMATION_URL = (
        WEB_APP_SCHEME + "api/authenticate/auth-api/confirm-email/"
)
ACCOUNT_AUTHENTICATION_METHOD = "email"
INVITATIONS_INVITATION_MODEL = "restaurants.StaffInvitation"
INVITATIONS_SIGNUP_REDIRECT = "actor_redirect"
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
INVITATIONS_INVITATION_EXPIRY = 7
INVITATIONS_ADAPTER = "core.CustomFiles.CustomAdapterFile.CustomAccountAdapter"
INVITATIONS_CONFIRMATION_URL_NAME = "restaurant_accept_invite"

# ACCOUNT_FORMS = {
# #     "login": "core.forms.UserSigninForm",
#     "signup": "restaurants.registration.RegistrationForm",
# }

# ACCOUNT_SIGNUP_FORM_CLASS = "restaurants.registration.RegistrationForm"



ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
######### ALL-AUTH PROVIDERS   ########
# Google provider details
client_id = ""
client_secret = ""

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
# Facebook provider details

# Provider settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
        "EMAIL_AUTHENTICATION": True,
        "FETCH_USERINFO": True,
        "REDIRECT_URI": "http://localhost:8000/accounts/google/login/callback/",
    },
    "facebook": {
        "METHOD": "oauth2",  # Set to 'js_sdk' to use the Facebook connect SDK
        "SDK_URL": "//connect.facebook.net/{locale}/sdk.js",
        "SCOPE": ["email", "public_profile"],
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "INIT_PARAMS": {"cookie": True},
        "FIELDS": [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "name",
            "name_format",
            "picture",
            "short_name",
        ],
        "EXCHANGE_TOKEN": True,
        #'LOCALE_FUNC': 'path.to.callable',
        "VERIFIED_EMAIL": False,
        "VERSION": "v20.0",
        "GRAPH_API_URL": "https://graph.facebook.com/v20.0",
    },
}


print(f"loading. .. {__file__}")