from rest_framework.permissions import BasePermission

class DeleteStaffOnly(BasePermission):

    edit_methods = ("DELETE",)

    def has_permission(self, request, view):
        if request.method not in self.edit_methods:
            return True
        
        if request.user.is_staff:
            return True
        
        return False