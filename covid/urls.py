from django.urls import path, include
from rest_framework import routers
from .views import CountyResourcesAPIView, SimulationRunViewSet, HashResourceAPIView

router = routers.SimpleRouter()
router.register(r'api/simulations', SimulationRunViewSet,
                basename="simulations")

urlpatterns = [
    # Return all county resources
    path(
        'api/county_resources/',
        CountyResourcesAPIView.as_view(),
        name="county_resources"
    ),
    path(
        'api/hash_resources/',
        HashResourceAPIView.as_view(),
        name="hash_resources"
    )
]

urlpatterns += router.urls
