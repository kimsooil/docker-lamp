from django.urls import path

from .views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
)

from .api import CustomAuthToken

app_name = "users"
urlpatterns = [
    # path("", view=user_list_view, name="list"),
    path("api/authenticate/", view=CustomAuthToken.as_view(), name="api-authenticate"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]