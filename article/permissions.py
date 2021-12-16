from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    僅管理員可進行修改
    其他僅查看
    """
    def has_permission(self, request, view):
        # 對所有人允許 GET, HEAD, OPTIONS 請求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 僅管理員可進行其他操作
        return request.user.is_superuser