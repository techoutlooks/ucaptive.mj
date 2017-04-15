from datetime import datetime
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .models import OneAuthToken
from .authentication import OneTokenAuthentication
from .serializers import OneLoginSerializer

# todo: one_auth should not rely on external app. make permissions abstract.
from one_accounts.permissions import IsOneUserAuthenticated
from lib.restutils import JSONResponse


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = OneLoginSerializer

    def post(self, request, format=None):
        data = JSONParser().parse(request)

        self.serializer = self.get_serializer(data=data)
        self.serializer.is_valid(raise_exception=True)

        self.user = self.serializer.validated_data['user']
        if self.user:
            token = OneAuthToken.objects.create(user=self.user)
            self.user.last_login = datetime.now()
            self.user.save()
            return JSONResponse({"token": token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (OneTokenAuthentication,)
    permission_classes = (IsOneUserAuthenticated,)

    def post(self, request, format=None):
        # simply delete the token to force a login
        # request.user.auth_token.delete()
        request._auth.delete()
        return JSONResponse({"sucess": "true"}, status=status.HTTP_200_OK)

#
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# class Logout(APIView):
#       """
#       http: // stackoverflow.com / questions / 30739352 / django - rest - framework - token - authentication - logout
#       """
#     queryset = User.objects.all()
#
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)