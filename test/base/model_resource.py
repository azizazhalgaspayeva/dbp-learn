from typing import Any, Generic, TypeVar

import factory
from django.db.models import Model
from django.forms.models import model_to_dict

from main.models import Tag, Task, User

from .factory_base import TagFactory, TaskFactory, UserFactory

T = TypeVar("T", bound=Model)


class ModelResource(Generic[T]):
    factory: type[factory.Factory]
    model: type[T]

    def create(self, **kwargs: Any) -> T:
        return self.factory.create()


class UserResource(ModelResource[User]):
    factory = UserFactory
    model = User


class TaskResource(ModelResource[Task]):
    factory = TaskFactory
    model = Task


class TagResource(ModelResource[Tag]):
    factory = TagFactory
    model = Tag
