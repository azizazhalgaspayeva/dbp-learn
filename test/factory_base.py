import factory
from factory.faker import Faker

from main.models import User


class UserFactory(factory.django.DjangoModelFactory):
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User