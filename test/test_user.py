from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms.models import model_to_dict
from rest_framework.exceptions import ErrorDetail

from test.base import TestViewSetBase
from test.base.factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    auth_error = {"detail": ErrorDetail(string="Authentication credentials were not provided.", code="not_authenticated")}
    required_fields = ["username", "first_name", "last_name", "email"]

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create_success(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        user = self.create(data=user_attributes, is_auth=True)
        expected_response = self.expected_details(user, user_attributes)

        assert user == expected_response
    
    def test_create_fail(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        response = self.create(data=user_attributes)
        expected_response = self.auth_error

        assert response == expected_response

    def test_list_success(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        self.create(data=user_attributes, is_auth=True)
        response = self.list(is_auth=True)[-1]
        expected_response = self.expected_details(response, user_attributes)

        assert response == expected_response

    def test_list_fail(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        self.create(data=user_attributes, is_auth=True)
        response = self.list()
        expected_response = self.auth_error

        assert response == expected_response

    def test_retrieve_success(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        user = self.create(data=user_attributes, is_auth=True)
        response = self.retrieve(is_auth=True, args=user["id"])
        expected_response = self.expected_details(response, user_attributes)

        assert response == expected_response
    
    def test_retrieve_fail(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        user = self.create(data=user_attributes, is_auth=True)
        response = self.retrieve(args=user["id"])
        expected_response = self.auth_error

        assert response == expected_response

    def test_delete_success(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        user = self.create(user_attributes, is_auth=True)
        response = self.delete(is_admin=True, args=user["id"])
        expected_response = None

        assert response == expected_response

    def test_delete_fail(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        user = self.create(user_attributes, is_auth=True)
        response = self.delete(args=user["id"])
        expected_response = self.auth_error

        assert response == expected_response
    
    def test_filter_success(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields)
        first_name = user_attributes["first_name"]

        self.create(user_attributes, is_auth=True)
        response = self.filter(args="?first_name=" + first_name)[-1]
        expected_response = self.expected_details(response, user_attributes)

        assert response == expected_response

    def test_large_avatar(self) -> None:
        user_faker = UserFactory.build(
            avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
        )
        user_attributes = model_to_dict(user_faker, fields=self.required_fields + ["avatar_picture"])
        response = self.action_client.request_create_user(**user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        user_faker = UserFactory.build()
        user_attributes = model_to_dict(user_faker, fields=self.required_fields + ["avatar_picture"])
        user_attributes["avatar_picture"].name = "bad_extension.pdf"

        response = self.action_client.request_create_user(**user_attributes)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
