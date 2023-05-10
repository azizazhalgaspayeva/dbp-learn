from rest_framework.permissions import BasePermission

class DeleteStaffOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE" and not request.user.is_staff:
            return False      
        return True