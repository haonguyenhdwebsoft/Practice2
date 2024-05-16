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

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        api_response = APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
        
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        update_data = request.data
        user = request.user

        serializer_data = {
            'username': update_data.get('username', user.username),
            'email': update_data.get('email', user.email),

            'profile': {
                'bio': update_data.get('bio', user.profile.bio),
                'image': update_data.get('image', user.profile.image)
            }
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        api_response = APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
        
        return Response(api_response.get_response(), status=status.HTTP_200_OK)

