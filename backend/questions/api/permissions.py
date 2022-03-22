from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """ 
        make sure that current auth user can update 
        or delete question becuase they are the 
        author of the question otherwise read only
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
