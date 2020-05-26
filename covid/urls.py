from django.urls import path, include
from rest_framework import routers
from .views import CountyResourcesAPIView, SimulationRunViewSet

router = routers.SimpleRouter()
router.register(r'api/simulations',SimulationRunViewSet )

urlpatterns = [
    # Return all county resources
    path(
        'api/county_resources/',
        CountyResourcesAPIView.as_view(),
        name="county_resources"
    ),
]

urlpatterns += router.urls
