# -*- coding: utf-8 -*-
import warnings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.deprecation import RemovedInDjango20Warning

from .serializers import ChangePasswordUserSerializer, RecoverPasswordUserSerializer
from .serializers import OneUserSerializer, OneUserDetailsSerializer
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny

from one_auth.authentication import OneTokenAuthentication
from .permissions import IsAdminOrReadOnly, IsOneUserAuthenticated, IsOneSuperAdmin
from lib.restutils import JSONResponse

User = get_user_model()


class AllUserList(generics.ListCreateAPIView):
    """ 
    List all users (readonly if not admin) or create a new one (anyone). 
    
    GET     ../api/v1/
    POST    ../api/v1/
    """
    serializer_class = OneUserSerializer
    authentication_classes = (OneTokenAuthentication,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('username', 'is_active', 'is_admin')

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsAdminOrReadOnly(),)

    def get_queryset(self):
        return User.objects.all()


class OneUserDetails(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin view to do RUD (retrieve, update, delete) ops on a user. 
    Leaves related models (eg. profile) untouched.
    
    GET             ../api/v1/profile/
    PUT, DELETE     ../api/v1/profile/{pk}/$
    
    """
    queryset = User.objects.all()
    serializer_class = OneUserDetailsSerializer
    authentication_classes = (OneTokenAuthentication,)
    permission_classes = (IsOneSuperAdmin,)
    renderer_classes = (JSONRenderer,)

    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])

    def perform_update(self, serializer):
        # Update password
        user = self.get_object()
        serializer.save()
        if "password" in self.request.data and self.request.data["password"] != "":
            password_serializer = ChangePasswordUserSerializer(data={"password": self.request.data["password"]})
            if password_serializer.is_valid(raise_exception=True):
                user.set_password(self.request.data["password"])
                user.save()
                # Logout all sessions if new password is not current password
                OneTokenAuthentication().delete_another_tokens(user)

    def perform_destroy(self, instance):
        # instance.delete()
        instance.is_active = 0
        instance.save()


class OneAuthenticatedUserDetail(generics.RetrieveUpdateAPIView):
    """
    View to do RU (retrieve, update) ops on a user. Leaves related models (eg. profile) untouched.
    
    GET     ../profile/
    PUT     ../profile/
    """
    queryset = User.objects.all()
    serializer_class = OneUserDetailsSerializer
    authentication_classes = (OneTokenAuthentication,)
    permission_classes = (IsOneUserAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get_object(self):
        return self.request.user


class OneUserSetPassword(generics.CreateAPIView):
    """
    Password change view.
    
    POST    ../profile/reset_password/
    """
    queryset = User.objects.all()
    serializer_class = ChangePasswordUserSerializer
    authentication_classes = (OneTokenAuthentication,)
    permission_classes = (IsOneUserAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def create(self, request, *args, **kwargs):
        user = request.user
        request_data = request.data
        print (request_data)
        if user.check_password(request_data["current_password"]):
            serializer = ChangePasswordUserSerializer(data={"password": self.request.data["new_password"]})
            if serializer.is_valid(raise_exception=True):
                if "new_password" in request_data:
                    user.set_password(request_data["new_password"])
                    user.save()
                    # Logout all sessions
                    if request_data["new_password"] != request_data["current_password"]:
                        OneTokenAuthentication().delete_another_tokens(user)
                    return JSONResponse({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return JSONResponse({'status': "fail",
                                 'data': {"password": "Current password is not correct"}},
                                status=status.HTTP_400_BAD_REQUEST)


# POST ../profile/recover_password/
class OneUserRecoverPassword(generics.CreateAPIView):
    """
    Send password reset link through email via django-registration.

    """
    queryset = User.objects.all()
    serializer_class = RecoverPasswordUserSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    is_admin_site=False
    template_name='one_accounts/password_reset_form.html'
    email_template_name='one_accounts/password_reset_email.html'
    subject_template_name='one_accounts/password_reset_subject.txt'
    from_email=None
    current_app=None
    extra_context=None
    html_email_template_name=None

    def create(self, request, *args, **kwargs):
        print "request.data==%s" %request.data
        user = request.user
        email = request.data["email"]

        # a user in currently logged in, but his profile has no email.
        if hasattr(user, 'email') and not user.email:
            return JSONResponse(
                {
                    'status': "fail",
                    'data': {"password": "Please, add an email to your account first !"}
                 },
                status=status.HTTP_400_BAD_REQUEST
            )

        # assumes email already in request.data.
        # check should be performed in frontend
        serializer = self.serializer_class(data={"email": email})
        if serializer.is_valid(raise_exception=True):
            opts = {
                'use_https': self.request.is_secure(),
                # 'token_generator': self.token_generator,
                'from_email': self.from_email,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': self.request,
                'html_email_template_name': self.html_email_template_name,
            }
            if self.is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                    RemovedInDjango20Warning, 3
                )
                opts = dict(opts, domain_override=self.request.get_host())

            serializer.save(**opts)
            return JSONResponse({'status': 'success'}, status=status.HTTP_200_OK)


class OneUserSimpleRegistrationView(generics.CreateAPIView):
    """
    URLconf for registration using django-registration's simple one-step
    workflow.

    A one-step (user signs up and is immediately active and logged in)
    workflow.

    """
    pass


class OneUserHMACRegistrationView(generics.CreateAPIView):
    """
    Restful view for registration and activation, using django-registration's
    HMAC activation workflow.

    A two-step (registration followed by activation) workflow, implemented
    by emailing an HMAC-verified timestamped activation token to the user
    on signup.

    """
    pass