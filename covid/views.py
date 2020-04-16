import requests

from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

# Create your views here.

# Pass Through View to Flask API
class ProxyToModelAPIView(ProtectedResourceView, APIView):

    def get(self, request, format=None):
        api_path = request.get_full_path().replace(settings.MODEL_API_SUBPATH, settings.MODEL_API_BASE_URL)
        r = requests.get(api_path)
        
        return Response(r.json())