from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from apps.core.models import APIResponse
from .services import AuthenticationServiceMixin, UserServiceMixin

class RegistrationAPIView(AuthenticationServiceMixin, APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        api_response = self.register(request.data)
        
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)


class LoginAPIView(AuthenticationServiceMixin, APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        api_response = self.login(request.data)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(UserServiceMixin, RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        api_response = self.get_user(request.user)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        update_data = request.data
        user = request.user

        api_response = self.update_user(user, update_data)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)

