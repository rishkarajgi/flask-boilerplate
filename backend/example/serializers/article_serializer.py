from backend.api import ModelSerializer, fields
from backend.extensions.api import api

from ..models import Article

ARTICLE_FIELDS = ('category',
                  'header_image',
                  'last_updated',
                  'preview',
                  'publish_date',
                  'slug',
                  'title',
                  )


class ArticleSerializer(ModelSerializer):
    category = fields.Nested('CategorySerializer', only=('id', 'name', 'slug'))

    class Meta:
        model = Article
        fields = ARTICLE_FIELDS + ('html',)


@api.serializer(many=True)
class ArticleListSerializer(ArticleSerializer):

    class Meta:
        model = Article
        fields = ARTICLE_FIELDS
