from rest_framework.permissions import BasePermission
from .models import Creditcard


class IsOwner(BasePermission):
    """Custom permission class to allow only creditcard owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the creditcard owner."""
        if isinstance(obj, Creditcard):
            return obj.owner == request.user
        return obj.owner == request.user
