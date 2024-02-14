import factory
from factory.faker import Faker

from .base import ImageFileProvider
from main.models import User

Faker.add_provider(ImageFileProvider)


class UserFactory(factory.django.DjangoModelFactory):
    username = Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = User
