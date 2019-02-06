from django.contrib.auth import get_user_model

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'username',
        ]
        read_only_fields = ['email']

class LoginAPIView(ObtainAuthToken):
    """
    - Inherits from ObtainAuthToken.
    - Logs in the user by checking their username/
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class MeAPIView(APIView):
    """
    - 
    """
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (UserSerializer,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UpdateMeAPIView(APIView):
    """
    - 
    """
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

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

class LogoutAPIView(APIView):
    """
    - 
    """
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        response = Token.objects.get(user=self.request.user).delete()
        return Response({'response': response})