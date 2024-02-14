import factory
from factory.faker import Faker

from main.models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    title = Faker("title")
    status = Faker("word")

    class Meta:
        model = Task
