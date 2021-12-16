from rest_framework.permissions import BasePermission, SAFE_METHODS

# 權限設置
class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner to update. 您必須是所有者才能更新.'
    # 驗證發文者與登錄者一致性
    def safe_methods_or_owner(self, request, func):
        if request.method in SAFE_METHODS:
            return True

        return func()

    def has_permission(self, request, view):
        return self.safe_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return self.safe_methods_or_owner(
            request,
            lambda: obj.author == request.user
        )