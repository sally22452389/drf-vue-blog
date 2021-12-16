from rest_framework import serializers
from article.models import Article
from user_info.serializers import UserDescSerializer

from article.models import Category
from article.models import Tag
from article.models import Avatar
from comment.serializers import CommentSerializer
"""
# 序列 指定數據各個字段的具體類型;父類別ModelSerializer
# List
class ArticleListSerializer(serializers.ModelSerializer):
    # 超連結 view_name 是 path(... name='xxx')
    url = serializers.HyperlinkedIdentityField(view_name="article:detail")
    # read_only 設置僅供讀
    author = UserDescSerializer(read_only=True)
    class Meta:
        model = Article
        fields = [
            'url',
            # 'id', 已有 url
            'title',
            'created',
            'author',
        ]

# Detail
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
"""

class AvatarSerializer(serializers.ModelSerializer):
    """圖片序列化"""
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """分類的序列化設置;router自動設置詳細頁面名稱"""
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']

# hyperlinked views
# class ArticleSerializer(serializers.HyperlinkedModelSerializer):
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    """文章序列化設置"""
    id = serializers.IntegerField(read_only=True)
    author = UserDescSerializer(read_only=True)
    # category 分類的可讀序列化字段
    category = CategorySerializer(read_only=True)
    # category 的 id 字段，用創建/更新 category 
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # tag 字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )
    # 圖片字段
    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True, 
        allow_null=True, 
        required=False
    )
    """
    # 驗證圖片id是否存在;不存在返回驗證錯誤
    def validate_avatar_id(self, value):
        if not Avatar.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Avatar with id {} not exists.".format(value))

        return value
    # category_id 字段的驗證
    def validate_category_id(self, value):
        if not Category.objects.filter(id=value).exists() and value is not None:
            raise serializers.ValidationError("Category with id {} not exists.".format(value))
        return value
    """
    # 覆寫方法，如果輸入的標籤不存在則創建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)
    # 錯誤訊息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )

        return value

    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )

        return value

class ArticleSerializer(ArticleBaseSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        # 列表顯示
        extra_kwargs = {'body': {'write_only': True}}
    

class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """分類文章的序列化設置"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分類詳細文章序列化"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles',
        ]

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """標籤序列化設置"""
    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'    

class ArticleDetailSerializer(ArticleBaseSerializer):
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # md轉換後的正文
    body_html = serializers.SerializerMethodField()
    # md轉換後的目錄
    toc_html = serializers.SerializerMethodField()
    # obj 是 serializer 序列化獲得的 model;文章對象
    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'


