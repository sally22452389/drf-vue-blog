from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown

# Create your models here.

class Category(models.Model):
    """文章分類"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Tag(models.Model):
    """文章標籤"""
    text = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.text

class Avatar(models.Model):
    # 圖片
    content = models.ImageField(upload_to='avatar/%Y%m%d')

class Article(models.Model):
    # 分類
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    author = models.ForeignKey(
        User, 
        null=True,
        on_delete=models.CASCADE, 
        related_name='articles'
    )
    # 標題
    title = models.CharField(max_length=100)
    # 內文
    body = models.TextField()
    # 創建時間
    created = models.DateTimeField(default=timezone.now)
    # 更新時間
    updated = models.DateTimeField(auto_now=True)
    # 標籤
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles'
    )
    # 標題圖
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

    # 新增方法，將body 轉為帶 html 標籤的正文
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是轉換後的目錄
        return md_body, md.toc