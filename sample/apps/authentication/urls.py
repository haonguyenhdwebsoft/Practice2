from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path("users", UserRetrieveUpdateAPIView.as_view()),
    path("users/register", RegistrationAPIView.as_view()),
    path("users/login", LoginAPIView.as_view()),
]
