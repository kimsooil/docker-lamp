from django.urls import path, include

from .api_users.group.api import UserGroupViewSet
from .api_users.group.admin_api import AdminUserViewSet, AdminGroupViewSet, AdminUserGroupViewSet

from rest_framework.routers import DefaultRouter

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

user_group_router = DefaultRouter()
user_group_router.register(r'user-groups', UserGroupViewSet, basename='user-groups')
<<<<<<< HEAD
=======

admin_user_router = DefaultRouter()
admin_user_router.register(r'admin-users', AdminUserViewSet, basename='admin-users')

admin_group_router = DefaultRouter()
admin_group_router.register(r'admin-groups', AdminGroupViewSet, basename='admin-groups')

admin_user_group_router = DefaultRouter()
admin_user_group_router.register(r'admin-user-group', AdminUserGroupViewSet, basename='admin-user-group')


app_name = "users"
urlpatterns = [
    # path("", view=user_list_view, name="list"),
>>>>>>> 554dba934776c16baecf3d3c1ba8fe365c7e355b

admin_user_router = DefaultRouter()
admin_user_router.register(r'admin-users', AdminUserViewSet, basename='admin-users')

admin_group_router = DefaultRouter()
admin_group_router.register(r'admin-groups', AdminGroupViewSet, basename='admin-groups')

admin_user_group_router = DefaultRouter()
admin_user_group_router.register(r'admin-user-group', AdminUserGroupViewSet, basename='admin-user-group')


app_name = "users"
urlpatterns = [
    # Get Authentication Token.
    path(
        'api/token/',
        oauth2_views.TokenView.as_view(),
        name="token"
    ),
    # Revoke Token (i.e. logout).
    path(
        'api/revoke-token/',
        oauth2_views.RevokeTokenView.as_view(),
        name="revoke-token"
    ),
    # Login/LOgout paths.
    path(
        "api/login/",
        view=LoginAPIView.as_view(),
        name="api-login"
    ),
    path(
        "api/logout/",
        view=LogoutAPIView.as_view(),
        name="api-logout-everywhere"
    ),
    # Account and update paths.
    path(
        "api/me/",
        view=MeAPIView.as_view(),
        name="api-me"
    ),
    path(
        "api/update/",
        view=UpdateMeAPIView.as_view(),
        name="api-update"
    ),
    path("api/me/", view=MeAPIView.as_view(), name="api-me"),
    path("api/update/", view=UpdateMeAPIView.as_view(), name="api-update"),

    path("api/", include(user_group_router.urls)),

    path("api/", include(admin_user_router.urls)),
    path("api/", include(admin_group_router.urls)),
    path("api/", include(admin_user_group_router.urls)),
    
    # HTML Logout.
    path("logout/", view=UserLogoutView.as_view(), name="logout"),

    path("api/", include(user_group_router.urls)),

    path("api/", include(admin_user_router.urls)),
    path("api/", include(admin_group_router.urls)),
    path("api/", include(admin_user_group_router.urls)),
    
    # HTML Logout.
    path(
        "logout/",
        view=UserLogoutView.as_view(),
        name="logout"
    ),
    path(
        "~redirect/",
        view=user_redirect_view,
        name="redirect"
    ),
    path(
        "~update/",
        view=user_update_view,
        name="update"
    ),
    path(
        "<str:username>/",
        view=user_detail_view,
        name="detail"
    ),
    # Forgot Password
    path(
        "api/forgot-password/",
        view=ForgotPasswordAPIView.as_view(),
        name="forgot-password"
    ),
    path(
        'api/reset-password/',
        view=PasswordResetAPIView.as_view(),
        name='reset-password'
    ),
    path(
        'api/change-password/',
        view=PasswordChangeAPIView.as_view(),
        name='change-password'
    ),
    path("api/forgot-password/", view=ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path('api/reset-password/', view=PasswordResetAPIView.as_view(), name='reset-password'),

    # Groups
    path("api/", include(user_group_router.urls)),

    path("api/", include(admin_user_router.urls)),
    path("api/", include(admin_group_router.urls)),
    path("api/", include(admin_user_group_router.urls)),
]
