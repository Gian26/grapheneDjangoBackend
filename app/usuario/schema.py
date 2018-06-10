from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import graphene
from graphene import Mutation,ObjectType
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model=User


class CreateUser(Mutation):
    user=graphene.relay.Node.Field(UserType)

    class Arguments:
        username=graphene.String(required=True)
        password=graphene.String(required=True)
        email=graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user=User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class UserQuery(ObjectType):
    users=graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()

class UserMutation(ObjectType):
    create_user=CreateUser.Field()
