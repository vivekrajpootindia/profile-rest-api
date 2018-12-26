from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    # edit your own profile
    # def has_permission(self, request, view):
    #     return True

    def has_object_permission(self, request, view, obj):
        # check user try to edit own profile

        if request.method in permissions.SAFE_METHODS:
            return True;

        return obj.id == request.user.id


class PostOwnStatus(permissions.BasePermission):
    # allow user to update there own status

    def has_object_permission(self, request, view, obj):
        # check user try to update own status

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id
