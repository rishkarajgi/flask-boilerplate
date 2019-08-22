import re

CREATE = 'create'
DELETE = 'delete'
GET = 'get'
HEAD = 'head'
LIST = 'list'
PATCH = 'patch'
POST = 'post'
PUT = 'put'

ALL_METHODS = (CREATE, DELETE, GET, LIST, PATCH, PUT)

READ_ONLY_FIELDS = ('slug', 'createdAt', 'updatedAt')


__PARAM_NAME_RE = r'<(\w+:)?(?P<param_name>\w+)>'
PARAM_NAME_RE = re.compile(__PARAM_NAME_RE)
LAST_PARAM_NAME_RE = re.compile(__PARAM_NAME_RE + r'$')
