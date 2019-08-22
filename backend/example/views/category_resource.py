from backend.api import ModelResource, GET, LIST, jsonify, param_converter
from backend.api.docs import doc, marshal_with, use_kwargs
from backend.extensions.api import api

from .blueprint import example
from ..models import Article, Category
from ..serializers import CategoryListSerializer, CategorySerializer, ErrorSerializer


@doc(tags=['category'])
@api.model_resource(example, Category, '/categories', '/categories/<slug>')
class CategoryResource(ModelResource):
    include_methods = (GET, LIST)

    doc_decorators = {
        LIST: [
            marshal_with(CategoryListSerializer(many=True), code=200),
            marshal_with(ErrorSerializer, code=400),
            marshal_with(ErrorSerializer, code=500)
        ],
        GET: [
            marshal_with(ErrorSerializer, code=400),
            marshal_with(ErrorSerializer, code=500)
        ]
    }

    def get(self, category):
        return self.serializer.dump({
            'name': category.name,
            'slug': category.slug,
            'articles': Article.filter_by(category=category).all(),
        })


@api.route(example, '/categories_by_id/<id>', methods=['GET'])
@param_converter(id={'categories': Category,
                     'is_list': True,
                     'validations': [
                         {
                             'validation_type': 'data_type',
                             'expected_type': 'uuid'
                         }
                     ]})
@marshal_with(ErrorSerializer, code=400)
@marshal_with(ErrorSerializer, code=500)
def get_categories(categories):
    return jsonify(categories)
