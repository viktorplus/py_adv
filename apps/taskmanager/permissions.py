from rest_framework.permissions import BasePermission, SAFE_METHODS


# class IsAdminOrReadOnly(BasePermission):
#     message = 'Only admin can change or delete this object'
# # hw18
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#
#         user = request.user
#         return bool(user and user.is_staff)

class IsOwnerOrReadOnly(BasePermission):
    message = 'Only the owner can change or delete this object'
    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS requests are allowed for any user
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user