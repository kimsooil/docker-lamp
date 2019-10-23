from django.urls import path

from .views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

from .api import LoginAPIView, UpdateMeAPIView, MeAPIView, LogoutAPIView, ForgotPasswordAPIView, PasswordResetAPIView, PasswordChangeAPIView

# from django.contrib.auth.views import LogoutView
from .views import UserLogoutView

# OAuth2 provider views.
import oauth2_provider.views as oauth2_views

app_name = "users"
urlpatterns = [
    # path("", view=user_list_view, name="list"),

    # Authentication/Authorization/Revoke paths.
    # path('api/authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('api/token/', oauth2_views.TokenView.as_view(), name="token"),
    path('api/revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),

    # Login/LOgout paths.
    path("api/login/", view=LoginAPIView.as_view(), name="api-login"),
    path("api/logout/", view=LogoutAPIView.as_view(), name="api-logout-everywhere"),

    # Account and update paths.
    path("api/me/", view=MeAPIView.as_view(), name="api-me"),
    path("api/update/", view=UpdateMeAPIView.as_view(), name="api-update"),
    
    # HTML Logout.
    path("logout/", view=UserLogoutView.as_view(), name="logout"),

    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    

    # Forgot Password
    path("api/forgot-password/", view=ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path('api/reset-password/', view=PasswordResetAPIView.as_view(), name='reset-password'),

    path('api/change-password/', view=PasswordChangeAPIView.as_view(), name='change-password'),
]
