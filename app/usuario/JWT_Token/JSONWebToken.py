from django.contrib.auth import authenticate, get_user_model
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import update_last_login

from functools import wraps

from graphql_jwt.decorators import *
from graphql_jwt.mutations import *
from graphql_jwt.mixins import *
from graphql_jwt.utils import get_payload
from graphql_jwt import Verify, Refresh

from graphene import Field, ObjectType

from promise import Promise, is_thenable


def token_auth(f):
    @wraps(f)
    def wrapper(cls, root, info, password, **kwargs):
        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user, info.context)
            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=info.context, username=username, password=password)

        if user is None:
            raise exceptions.GraphQLJWTError(
                _('Please, enter valid credentials'))

        if hasattr(info.context, 'user'):
            update_last_login(None, user)
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        # Improved mutation with thenable check
        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)

    return wrapper

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **options):
        options.setdefault('arguments', cls.auth_fields())
        super(JSONWebTokenMutation, cls).__init_subclass_with_meta__(**options)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info)


class ObtainJSONWebToken2(ResolveMixin, JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""


class JSONWebTokenMutation(ObjectType):
    token_auth = ObtainJSONWebToken2.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
