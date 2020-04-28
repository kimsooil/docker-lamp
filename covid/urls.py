from django.urls import path, include
from .views import CountyResourcesAPIView

urlpatterns = [
    # Return all county resources
    path(
        'api/county_resources/',
        CountyResourcesAPIView.as_view(),
        name="county_resources"
    ),
]
