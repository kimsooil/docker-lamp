from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from oauth2_provider.views.generic import ProtectedResourceView

from users.serializers.user_serializers import UserSerializer
from users.serializers.group import GroupSerializer

User = get_user_model()


class AdminUserViewSet(ProtectedResourceView, viewsets.ViewSet):
    """
    Return a list of users and A user if the current user is an admin.
    """
    throttle_classes = ()
    permission_classes = (IsAdminUser,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (UserSerializer,)

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AdminGroupViewSet(ProtectedResourceView, viewsets.ViewSet):
    """
    Return a list of groups.
    """
    throttle_classes = ()
    permission_classes = (IsAdminUser,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (GroupSerializer,)

    def list(self, request):
        serializer = GroupSerializer(Group.objects.all(), many=True)
        return Response(serializer.data)


class AdminUserGroupViewSet(ProtectedResourceView, viewsets.ViewSet):
    """
    A ViewSet for managing groups.
    """
    throttle_classes = ()
    permission_classes = (IsAdminUser,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (GroupSerializer,)

    def list(self, request):
        user_id = request.GET.get('user_id', request.user.id)
        user = User.objects.get(id=user_id)
        return Response(user.groups.values_list('name', flat=True))

    def create(self, request):
        user_id = request.data['user_id']
        group_id = request.data['group_id']

        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, pk=group_id)
        user.groups.add(group)

        return Response({})

    def destroy(self, request, pk=None):
        user_id = request.GET.get('user_id', None)
        group_id = request.GET.get('group_id', None)

        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, pk=group_id)
        user.groups.remove(group)

        return Response({})
