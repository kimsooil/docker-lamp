"""dcc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from .views import HomeView, AboutView, HelpView
from .views import ExampleAuthenticatedView, ExampleView

from users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include(users_urls)),

    # re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('help/', HelpView.as_view(), name='help'),

    # Wagtail.
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),

    # Example DRF views.
    path('drf/not-authenticated/', ExampleView.as_view()),
    path('drf/authenticated/', ExampleAuthenticatedView.as_view())
] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# If debugging is on (i.e. not production), then include these urls.
if settings.DEBUG:
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title='API')
    urlpatterns.append(path(r'swagger', schema_view))
