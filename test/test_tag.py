from test.base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail 


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {"title": "urgent"}

    auth_error = {"detail": ErrorDetail(string="Authentication credentials were not provided.", code="not_authenticated")}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create_success(self) -> None:
        tag = self.create(data=self.tag_attributes, is_auth=True)
        expected_response = self.expected_details(tag, self.tag_attributes)

        assert tag == expected_response
    
    def test_create_fail(self) -> None:
        response = self.create(data=self.tag_attributes)
        expected_response = self.auth_error

        assert response == expected_response

    def test_list_success(self) -> None:
        self.create(data=self.tag_attributes, is_auth=True)
        response = self.list(is_auth=True)[-1]
        expected_response = self.expected_details(response, self.tag_attributes)

        assert response == expected_response

    def test_list_fail(self) -> None:
        self.create(data=self.tag_attributes, is_auth=True)
        response = self.list()
        expected_response = self.auth_error

        assert response == expected_response

    def test_retrieve_success(self) -> None:
        tag = self.create(data=self.tag_attributes, is_auth=True)
        response = self.retrieve(is_auth=True, args=tag["id"])
        expected_response = self.expected_details(response, self.tag_attributes)

        assert response == expected_response
    
    def test_retrieve_fail(self) -> None:
        tag = self.create(data=self.tag_attributes, is_auth=True)
        response = self.retrieve(args=tag["id"])
        expected_response = self.auth_error

        assert response == expected_response

    def test_delete_success(self) -> None:
        tag = self.create(self.tag_attributes, is_auth=True)
        response = self.delete(is_admin=True, args=tag["id"])
        expected_response = None

        assert response == expected_response

    def test_delete_fail(self) -> None:
        tag = self.create(self.tag_attributes, is_auth=True)
        response = self.delete(args=tag["id"])
        expected_response = self.auth_error

        assert response == expected_response
    