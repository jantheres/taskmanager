from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Roles

class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role in [Roles.ADMIN, Roles.SUPERADMIN])

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Roles.SUPERADMIN