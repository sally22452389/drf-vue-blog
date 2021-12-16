from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404

from article.models import Article
from article.serializers import ArticleDetailSerializer
# from article.serializers import ArticleListSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
# from rest_framework.permissions import IsAdminUser 
from article.permissions import IsAdminUserOrReadOnly

from rest_framework import viewsets
from article.serializers import ArticleSerializer

# django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# 分類
from article.models import Category
from article.serializers import CategorySerializer, CategoryDetailSerializer
# 標籤
from article.models import Tag
from article.serializers import TagSerializer
# 圖片
from article.models import Avatar
from article.serializers import AvatarSerializer
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    """分類category view"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    # 使分類更簡潔
    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    # 部分搜索
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    # filterset_fields = ['author__username', 'title']
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    # 過濾
    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username', None)

        if username is not None:
            queryset = queryset.filter(author__username=username)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]

"""
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    # 文章詳細view
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    # 權限
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    # 權限
    permission_classes = [IsAdminUserOrReadOnly]
    # 文章創建者序列
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
"""
"""
    def get_object(self, pk):
        獲得單一文章對象
        try:
            # pk 即主鍵，預設狀態下就是 id
            return Article.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        # 返回 Json 數值
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data)
        # 驗證送出數值是否有效
        # 如錯誤返回400
        if serializer.is_valid():
            # 序列化將持有的數據反序列後，
            # 保存到資料庫中
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        # 刪除成功後返回204
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
"""
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
