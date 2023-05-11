from http import HTTPStatus
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from typing import Union, List
from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    token_url = reverse("token_obtain_pair")

    attributes = {
        "username": "user",
        "first_name": "name",
        "last_name": "surname",
        "email": "user@test.com",
        "password": "123",
    }
    admin_attributes = {
        "username": "admin",
        "first_name": "name",
        "last_name": "surname",
        "email": "admin@test.com",
        "password": "123",
    }

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.admin = cls.create_api_admin()
        cls.client = APIClient()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)
    
    @classmethod
    def filter_url(cls, args: str = None) -> str:
        return reverse(f"{cls.basename}-list") + args
    
    @classmethod
    def create_api_user(cls):
        return User.objects.create(**cls.attributes)
    
    @classmethod
    def create_api_admin(cls):
        return User.objects.create_superuser(**cls.admin_attributes)
    
    @classmethod
    def token_auth(cls, client):
        response = client.post(cls.token_url, data={"username": cls.admin_attributes["username"], 
                                                    "password": cls.admin_attributes["password"]})
        token = response.json()["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        client.force_login(cls.admin)
    
    @classmethod
    def get_status_code(cls, client, is_auth, is_admin, status_success):        
        if is_admin:
            cls.token_auth(client)
            return status_success
        
        elif is_auth:
            client.force_login(cls.user)
            client.credentials()
             
        else:
            client.logout()
            
        return HTTPStatus.UNAUTHORIZED

    def create(self, data: dict, is_auth: bool = False, args: List[Union[str, int]] = None) -> dict:
        is_admin = is_auth
        expected_status_code = self.get_status_code(self.client, is_auth, is_admin, HTTPStatus.CREATED)
        response = self.client.post(self.list_url(args), data=data)

        assert response.status_code == expected_status_code, response.content
        return response.data

    def list(self, is_auth: bool = False, args: List[Union[str, int]] = None) -> dict:
        is_admin = is_auth
        expected_status_code = self.get_status_code(self.client, is_auth, is_admin, HTTPStatus.OK)
        response = self.client.get(self.list_url(args))

        assert response.status_code == expected_status_code, response.content
        return response.data

    def retrieve(self, is_auth: bool = False, args: List[Union[str, int]] = None) -> dict:
        is_admin = is_auth
        expected_status_code = self.get_status_code(self.client, is_auth, is_admin, HTTPStatus.OK)
        response = self.client.get(self.detail_url(args))
        
        assert response.status_code == expected_status_code, response.content
        return response.data

    def delete(self, is_admin: bool = False, args: List[Union[str, int]] = None) -> dict:
        is_auth = True
        expected_status_code = self.get_status_code(self.client, is_auth, is_admin, HTTPStatus.NO_CONTENT)
        response = self.client.delete(self.detail_url(args))

        print("!!!!!!!!!!!!!")
        print(response)
        print(expected_status_code)

        assert response.status_code == expected_status_code, response.content
        return response.data
    
    def filter(self, args: str = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.filter_url(args))

        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
