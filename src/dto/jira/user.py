from flask_restplus import fields

from src import api


user = api.model('jira-user', {
    'id': fields.String(attribute='accountId'),
    'avatar': fields.Url(attribute=lambda x: x['avatarUrls']['16x16']),
    'display-name': fields.String(attribute='displayName'),
    'email': fields.String(attribute='emailAddress'),
})