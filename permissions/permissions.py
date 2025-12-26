from rest_framework.permissions import BasePermission
from permissions.utils import get_user_role


class IsOwnerDoctor(BasePermission):
    def has_permission(self, request, view):
        clinic = request.query_params.get('clinic')
        if not clinic:
            return False
        return get_user_role(request.user, clinic) == 'owner'


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        clinic = request.query_params.get('clinic')
        role = get_user_role(request.user, clinic)
        return role in ['owner', 'associate']


class IsFrontDesk(BasePermission):
    def has_permission(self, request, view):
        clinic = request.query_params.get('clinic')
        return get_user_role(request.user, clinic) == 'frontdesk'
