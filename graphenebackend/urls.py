from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

from graphenebackend.schema import *

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
