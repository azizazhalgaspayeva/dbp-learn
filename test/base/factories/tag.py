import factory
from factory.faker import Faker

from main.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    title = Faker("title")

    class Meta:
        model = Tag
