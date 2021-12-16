"""drf_vue_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter
from article import views

from django.conf import settings
from django.conf.urls.static import static

from comment.views import CommentViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_info.views import UserViewSet

router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)
# 分類
router.register(r'category', views.CategoryViewSet)
# 標籤
router.register(r'tag', views.TagViewSet)
# 圖片
router.register(r'avatar', views.AvatarViewSet)
# 留言
router.register(r'comment', CommentViewSet)
# 用戶
router.register(r'user', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/article/', include('article.urls', namespace='article')),
]
# 圖片檔案路徑
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)