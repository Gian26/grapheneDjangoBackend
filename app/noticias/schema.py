from collections import namedtuple
from datetime import datetime

from django.utils.text import slugify
from django.contrib.auth.models import User

import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from app.noticias.models import News


class NewsType(DjangoObjectType):
    class Meta:
        model = News
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'publish_date': ['gte', 'lte', 'exact'],
            'body': ['icontains'],
            'slug': ['exact'],
            'public': ['exact']
        }
        interfaces = (graphene.relay.Node, )


class NewsGraph(graphene.ObjectType):
    title = graphene.String()
    body = graphene.String()
    publish_date = graphene.types.datetime.Date()
    public = graphene.Boolean()
    slug = graphene.String()


class CreateNews(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()
        publish_date = graphene.types.datetime.Date()
        public = graphene.Boolean()
        slug = graphene.String()

    ok = graphene.Boolean()
    news = graphene.Field(lambda: NewsGraph)

    def mutate(self, info, title, body, public, publish_date):

        user = info.context.user
        if user.is_anonymous:
            raise Exception(
                'Not logged in, Authentication credentials were not provided')

        news = News(
            title=title,
            body=body,
            slug=slugify(title),
            public=public,
            publish_date=publish_date)
        news.save()
        ok = True
        return CreateNews(news=news, ok=ok)


class UpdateNews(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()
        publish_date = graphene.types.datetime.Date()
        public = graphene.Boolean()
        slug = graphene.String()

    ok = graphene.Boolean()
    news = graphene.Field(lambda: NewsGraph)

    def mutate(self, info, title, body, public, publish_date, slug):

        user = info.context.user
        if user.is_anonymous:
            raise Exception(
                'Not logged in, Authentication credentials were not provided')

        news_user = News.objects.get(slug=slug)

        news_user.title = title
        news_user.body = body
        news_user.public = public
        news_user.publish_date = publish_date
        news_user.slug = slug
        news_user.save()
        ok = True
        return UpdateNews(news=news_user, ok=ok)


class NewsMutation(graphene.ObjectType):
    create_news = CreateNews.Field()
    update_news = UpdateNews.Field()


class NewsQuery(graphene.ObjectType):
    news = graphene.relay.Node.Field(NewsType)
    all_News = DjangoFilterConnectionField(NewsType)

    def resolve_all_News(self, info, **kwargs):
        return News.objects.all()
