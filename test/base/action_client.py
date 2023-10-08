from typing import Any, Optional

from http import HTTPStatus
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from main.models import User

from .model_resource import TagResource, TaskResource, UserResource


class ActionClient:
    def __init__(self, api_client: APIClient) -> None:
        self.api_client = api_client
        self.user: Optional[User] = None
        self.users = UserResource()
        self.tasks = TaskResource()
        self.tags = TagResource()
        self.user_attributes = {
            "username": "johnsmith",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@test.com",
        }
        self.task_attributes = {
            "title": "some_title",
            "status": "new_task",
        }

    def init_user(self) -> None:
        self.user = self.users.create()
        self.api_client.force_authenticate(user=self.user)  # type: ignore

    def create_user(self, **attributes: Optional[Any]) -> dict:
        self.user_attributes.update(attributes)
        response = self.request_create_user(**self.user_attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def create_task(self, **attributes: Any) -> dict:
        self.task_attributes.update(attributes)
        response = self.request_create_task(**self.task_attributes)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create_user(self, **attributes) -> Response:
        return self.api_client.post(reverse("users-list"), data=attributes)

    def request_create_task(self, **attributes) -> Response:
        return self.api_client.post(reverse("tasks-list"), data=attributes)
