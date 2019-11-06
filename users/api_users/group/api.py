from django.contrib.auth import get_user_model

from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import renderers

from oauth2_provider.views.generic import ProtectedResourceView

from users.serializers.group import GroupSerializer

User = get_user_model()


class UserGroupViewSet(ProtectedResourceView, viewsets.ViewSet):
    """
    Return a user's groups.
    """
    throttle_classes = ()
    permission_classes = ()

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (GroupSerializer,)

    def list(self, request):
        user = User.objects.get(id=request.user.id)
        return Response(user.groups.values_list('name', flat=True))
