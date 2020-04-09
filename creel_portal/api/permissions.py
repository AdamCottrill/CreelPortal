from rest_framework import permissions
from ..utils import is_admin


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        # is_admin = super(IsAdminUserOrReadOnly, self).has_permission(request, view)
        # Python3:
        is_admin = super().has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsPrjLeadOrAdminOrReadOnly(permissions.BasePermission):
    """A custom perission class that will only allow the creel project lead or a
    site administrator access the endpoint (for creating, updating or
    deleting creel design objects).

    TODO: add Crew or readonly to allow field crew to collect data but
    not alter creel design tables.

    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "creel"):
            lead_or_crew = obj.creel.prj_ldr == request.user
        else:
            lead_or_crew = obj.prj_ldr == request.user

        return lead_or_crew or is_admin(request.user)
