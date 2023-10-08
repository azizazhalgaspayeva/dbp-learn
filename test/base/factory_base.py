import factory
from factory.faker import Faker

from main.models import Tag, Task, User


class UserFactory(factory.django.DjangoModelFactory):
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class TaskFactory(factory.django.DjangoModelFactory):
    title = Faker("title")
    status = Faker("word")

    class Meta:
        model = Task


class TagFactory(factory.django.DjangoModelFactory):
    title = Faker("title")

    class Meta:
        model = Tag
