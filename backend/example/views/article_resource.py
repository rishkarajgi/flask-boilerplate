from backend.api import ModelResource, GET, LIST, CREATE
from backend.api.docs import doc, marshal_with, use_kwargs
from backend.extensions.api import api

from .blueprint import example
from ..models import Article
from ..serializers import ArticleSerializer, ErrorSerializer


@doc(tags=['article'], params={
    'x-initiator': {
        'description': 'User Id of the request initiator',
        'in': 'header',
        'type': 'string',
        'required': False
    }
})
@marshal_with(ErrorSerializer, code=500, description='Returned in case of an error')
@api.model_resource(example, Article, '/articles', '/articles/<slug>')
class ArticleResource(ModelResource):
    include_methods = (GET, LIST, CREATE)
    exclude_decorators = (LIST,)

    doc_decorators = {
        CREATE: [
            use_kwargs(ArticleSerializer),
            marshal_with(ArticleSerializer, code=201,
                         description='Success Response')
        ],
        GET: [
            marshal_with(ArticleSerializer, code=200,
                         description='Success Response')
        ]
    }

    def list(self):
        return Article.get_published()
