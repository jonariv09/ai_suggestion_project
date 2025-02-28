from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ai_suggestion_project.users.serializers.registration import RegistrationResponseSerializer, RegistrationSerializer


class RegistrationAPIView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = RegistrationResponseSerializer(data={"access": str(refresh.access_token), "refresh": str(refresh)})
        response.is_valid(raise_exception=True)
        return Response(response.data, status=status.HTTP_201_CREATED)
