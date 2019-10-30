from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status

from oauth2_provider.views.generic import ProtectedResourceView

from users.serializers.user_serializers import UserSerializer
from users.serializers.group import GroupSerializer

User = get_user_model()


class MeAPIView(ProtectedResourceView, APIView):
    """
    Return user's account info.
    """
    throttle_classes = ()
    permission_classes = ()

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (UserSerializer,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UpdateMeAPIView(ProtectedResourceView, APIView):
    """
    - Allows user to update their name/username.
    """
    throttle_classes = ()
    permission_classes = ()

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (UserSerializer,)

    def put(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)

        # Check that the data is valid using the serializer.
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():

            # Get and check that the username is valid.
            username = request.data['username']
            if not username == user.username:
                if User.objects.filter(username=username).exists():
                    message = "Username '%s' already exists." % username
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            user.name = request.data['name']
            user.username = request.data['username']
            user.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
