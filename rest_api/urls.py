from django.urls import path
from .views import RegisterUserView, CutomObtainPairView


urlpatterns = [
    path("signup/", RegisterUserView.as_view(), name="noramal_register"),
    path('signin/', CutomObtainPairView.as_view(), name='noramal_signin'),
]