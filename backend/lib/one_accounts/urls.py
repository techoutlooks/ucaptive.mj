"""
Wire up restful views that return JSONResponse

"""
from .api.views import *
from django.conf.urls import url, include


urlpatterns = [
    # User management (one_accounts)
    # ------------------------------------------------------------------------
    # GET, POST ../                     (one_accounts) get all users, create new user
    # GET, PUT, DELETE ../profile/      (one_accounts) OneUserDetails
    # POST ../profile/reset_password/   (one_accounts) password reset (authenticated users only)
    # POST ../profile/recover_password/ (one_accounts) password recovery via email

    url(r'^$', AllUserList.as_view(), name='users-list'),
    url(r'^(?P<pk>[0-9]+)/$', OneUserDetails.as_view(), name='user-detail'),
    url(r'^profile/$', OneAuthenticatedUserDetail.as_view(), name='user-profile'),
    url(r'^profile/reset_password/$', OneUserSetPassword.as_view(), name='set-pass-user'),

    # being debugged ...
    url(r'^profile/recover_password/$', OneUserRecoverPassword.as_view(), name='recover-pass-user'),

    # Restful Login & Logout views (one_auth)
    # ------------------------------------------------------------------------
    # POST ../login,                  returns auth_token (provided by one_auth)
    # POST ../logout                  logs out (provided by one_auth)
    url('', include('one_auth.urls')),

]
