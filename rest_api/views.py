from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_api.models import User

from .serializers import *


def user_access_token(user, context, is_created=False):
    refresh = RefreshToken.for_user(user)
    response = {
        "access": str(refresh.access_token),
        "user": UserSerializer(user, context=context).data,
    }
    if is_created:
        response['message'] = "User created successfully."

    return Response(response)


class RegisterUserView(generics.GenericAPIView):
    """ Create API view for serializer class "RegisterUserSerializer" and "UserSerializer".
    This view verify all input and create new user """
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        if User.objects.filter(email__iexact=request.data['email']).exists():
            return Response({'error': {"email": ["Your email already register. please login with password."]}}, status=400)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)

    
class CutomObtainPairView(TokenObtainPairView):
    """ Create API view for serializer class 'CustomTokenObtainPairSerializer' """
    serializer_class = CustomTokenObtainPairSerializer
