__author__ = 'ceduth'
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsNewUser(permissions.BasePermission):
    """ 
    Allow non-authenticated user to create via POST  
    """
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to edit.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True
            # Write permissions are only allowed to the admin.
            else:
                return request.user.is_admin
        else:
            raise PermissionDenied("You must be logged in to view this.")


class IsOneUserAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated():
            return obj.user == request.user or request.user.is_admin
        else:
            raise PermissionDenied("You must be logged in to view this.")

    def has_permission(self, request, view):
        if request.user.is_authenticated():
            pk = int(view.kwargs['pk'])
            return request.user.pk == pk or request.user.is_admin
        else:
            raise PermissionDenied("You must be logged in to view this.")


class IsOneSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            return request.user.is_admin
        else:
            raise PermissionDenied("You must be logged in as an admin to view this.")


class IsOneSuperAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin