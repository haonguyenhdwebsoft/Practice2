from rest_framework import status
from apps.core.models import APIResponse

class AuthenticationServiceMixin:
    def register(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return APIResponse(status_code=status.HTTP_201_CREATED, success=True, data=serializer.data)
    
    def login(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
class UserServiceMixin:
    def get_user(self, data):
        serializer = self.serializer_class(data)

        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)
    
    def update_user(self, user, update_data):
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

        return APIResponse(status_code=status.HTTP_200_OK, success=True, data=serializer.data)