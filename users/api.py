from django.contrib.auth import get_user_model

from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import parsers
from rest_framework import renderers
from rest_framework import status

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from users.serializers.user_serializers import UserSerializer
from users.serializers.forgot_password_serializer import PasswordResetSerializer
from users.serializers.password_reset_serializer import PasswordResetConfirmSerializer
from users.serializers.change_password_serializer import PasswordChangeSerializer

from oauth2_provider.views.generic import ProtectedResourceView

from rest_framework.permissions import AllowAny

from django.utils.translation import ugettext_lazy as _

User = get_user_model()


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'new_password', 'confirm_new_password'
    )
)


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


class PasswordResetAPIView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
        new_password, confirm_new_password
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetAPIView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )


class PasswordChangeAPIView(ProtectedResourceView, GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordChangeSerializer
    permission_classes = ()

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeAPIView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been saved.")})
