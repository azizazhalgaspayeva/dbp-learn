from django.db import models

from .tag import Tag
from .user import User


class Task(models.Model):
    class Status(models.TextChoices):
        NEW_TASK = "new_task"
        IN_DEVELOPMENT = "in_development"
        ARCHIVED = "archived"
        IN_QA = "in_qa"
        IN_CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True)
    status = models.CharField(
        max_length=255, default=Status.NEW_TASK, choices=Status.choices
    )
    priority = models.IntegerField()
    tags = models.ManyToManyField(Tag)
    reporter = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="reporter"
    )
    assignee = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="assignee"
    )

    def __str__(self):
        return self.title
