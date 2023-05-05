from test.base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail 


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
    }
    auth_error = {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')}
    permission_error = {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create_success(self) -> None:
        user = self.create(data=self.user_attributes, is_auth=True)
        expected_response = self.expected_details(user, self.user_attributes)

        assert user == expected_response
    
    def test_create_fail(self) -> None:
        response = self.create(data=self.user_attributes)
        expected_response = self.auth_error

        assert response == expected_response

    def test_list_success(self) -> None:
        self.create(data=self.user_attributes, is_auth=True)
        response = self.list(is_auth=True)[-1]
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response

    def test_list_fail(self) -> None:
        self.create(data=self.user_attributes, is_auth=True)
        response = self.list()
        expected_response = self.auth_error

        assert response == expected_response

    def test_retrieve_success(self) -> None:
        user = self.create(data=self.user_attributes, is_auth=True)
        response = self.retrieve(is_auth=True, args=user["id"])
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response
    
    def test_retrieve_fail(self) -> None:
        user = self.create(data=self.user_attributes, is_auth=True)
        response = self.retrieve(args=user["id"])
        expected_response = self.auth_error

        assert response == expected_response

    def test_delete_success(self) -> None:
        user = self.create(self.user_attributes, is_auth=True)
        response = self.delete(is_admin=True, args=user["id"])
        expected_response = None

        assert response == expected_response

    def test_delete_fail(self) -> None:
        user = self.create(self.user_attributes, is_auth=True)
        response = self.delete(args=user["id"])
        expected_response = self.permission_error

        assert response == expected_response
    
    def test_filter_success(self) -> None:
        self.create(self.user_attributes, is_auth=True)
        response = self.filter(args='?first_name=oh')[-1]
        expected_response = self.expected_details(response, self.user_attributes)

        assert response == expected_response
