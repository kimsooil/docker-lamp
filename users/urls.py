from django.urls import path

from .views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

from .api import LoginAPIView, UpdateMeAPIView, MeAPIView, LogoutAPIView

# from django.contrib.auth.views import LogoutView
from .views import UserLogoutView

app_name = "users"
urlpatterns = [
    # path("", view=user_list_view, name="list"),

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
    
]
