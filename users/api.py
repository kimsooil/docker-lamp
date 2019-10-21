from django.contrib.auth import get_user_model

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status

from users.serializers.user_serializers import UserSerializer
from users.serializers.forgot_password_serializer import PasswordResetSerializer

User = get_user_model()

from oauth2_provider.views.generic import ProtectedResourceView

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.utils.translation import ugettext_lazy as _

# class TestDOAuth2(ProtectedResourceView):
#     def get(self, request, *args, **kwargs):
#         return Response({'test': "Hi there!"})


class LoginAPIView(ObtainAuthToken):
    """
    - Inherits from ObtainAuthToken.
    Logs in the user by checking their username/
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

class MeAPIView(ProtectedResourceView, APIView):
    """
    - Return user's account info.
    """
    throttle_classes = ()
    permission_classes = ()
    # authentication_classes = (SessionAuthentication, TokenAuthentication,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializers = (UserSerializer,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UpdateMeAPIView(APIView):
    """
    - Allows user to update their name/username.
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
    - Logs out the user.
    NOTE: This will delete the token, thereby logging them out from everywhere.
    """
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (SessionAuthentication, TokenAuthentication,)

    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        response = Token.objects.get(user=self.request.user).delete()
        return Response({'response': response})

class ForgotPasswordAPIView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )
