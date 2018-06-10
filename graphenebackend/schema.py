import graphene

from app.noticias.schema import NewsQuery, NewsMutation
from app.usuario.schema import UserQuery, UserMutation
from app.usuario.JWT_Token.JSONWebToken import JSONWebTokenMutation


class Query(NewsQuery, UserQuery, graphene.ObjectType):
    pass


class Mutation(NewsMutation, UserMutation, JSONWebTokenMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
