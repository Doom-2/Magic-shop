from rest_framework import permissions


class SelectionUpdateDeletePermission(permissions.BasePermission):

    message = 'Updating or deleting not your selection is not permitted'

    def has_object_permission(self, request, view, obj):
        """
        Checking whether the object has required field 'owner'
        and whether user is authenticated, and we logged in under ourselves.
        """

        if hasattr(obj, "owner"):
            return request.user and request.user.is_authenticated and obj.owner == request.user


class AdUpdateDeletePermission(permissions.BasePermission):

    message = 'Updating or deleting an add can be done by authors or admins/moderators only'

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated and request.user.role in ("admin", "moderator"):
            return True

        elif hasattr(obj, "author"):
            return request.user and request.user.is_authenticated and obj.author == request.user
