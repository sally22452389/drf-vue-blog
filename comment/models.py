from django.db import models
from django.utils import timezone

from article.models import Article
from django.contrib.auth.models import User

# Create your models here.
# 留言
class Comment(models.Model):
    # 作者1對多
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 文章1對多
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 內容
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    # 父評論
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[:20]