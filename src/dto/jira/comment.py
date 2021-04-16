from flask_restplus import fields

from src import api
from src.dto.jira.user import user


comment = api.model('jira-comment', {
    'author': fields.Nested(user),
    'body': fields.String,
    'created': fields.DateTime,
    'updated': fields.DateTime
})
