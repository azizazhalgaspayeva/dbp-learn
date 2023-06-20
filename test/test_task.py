from test.base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail 

from main.models import User, Tag


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    auth_error = {"detail": ErrorDetail(string="Authentication credentials were not provided.", code="not_authenticated")}

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        extra_attributes = {"id": entity["id"],
                            "date_created": entity["date_created"],
                            "date_edited": entity["date_edited"],
                            "deadline": entity["deadline"],
                            "description": entity["description"],
                            "priority": entity["priority"],
                            "status": entity["status"],
                            "tags": entity["tags"],}
        return {**attributes, **extra_attributes}

    @staticmethod
    def get_task_attributes(title: str = "task") -> dict:
        reporter = User.objects.create(username="user1", first_name="user1")
        assignee = User.objects.create(username="user2", first_name="user2")
        tag = Tag.objects.create(title="urgent")
        task_attributes = {
            "title": title,
            "reporter": reporter.id,
            "assignee": assignee.id,
            "tags": tag.id,
        }
        return task_attributes

    def test_create_success(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        expected_response = self.expected_details(task, task_attributes)

        assert task == expected_response

    def test_create_fail(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes)
        expected_response = self.auth_error

        assert task == expected_response

    def test_list_success(self) -> None:
        task_attributes = self.get_task_attributes()
        self.create(data=task_attributes, is_auth=True)
        response = self.list(is_auth=True)[-1]
        expected_response = self.expected_details(response, task_attributes)

        assert response == expected_response
    
    def test_list_fail(self) -> None:
        task_attributes = self.get_task_attributes()
        self.create(data=task_attributes, is_auth=True)
        response = self.list()
        expected_response = self.auth_error

        assert response == expected_response

    def test_retrieve_success(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        response = self.retrieve(args=task["id"], is_auth=True)
        expected_response = self.expected_details(response, task_attributes)

        assert response == expected_response
    
    def test_retrieve_fail(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        response = self.retrieve(args=task["id"])
        expected_response = self.auth_error

        assert response == expected_response

    def test_delete_success(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        response = self.delete(args=task["id"], is_admin=True)
        expected_response = None

        assert response == expected_response

    def test_delete_fail(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        response = self.delete(args=task["id"])
        expected_response = self.auth_error

        assert response == expected_response
    
    def test_filter_success(self) -> None:
        task_attributes = self.get_task_attributes()
        task = self.create(data=task_attributes, is_auth=True)
        tag = task["tags"][-1]
        
        response = self.filter(args=f"?reporter=user1&assignee=user2&status=new_task&tags={tag}")[-1]
        expected_response = self.expected_details(response, task_attributes)

        assert response == expected_response
