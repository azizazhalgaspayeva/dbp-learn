from rest_framework import serializers
from models import User, Task, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 
                  'email', 'date_of_birth', 'phone')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'date_created', 'date_edited', 
                  'deadline', 'status', 'priority', 'tags', 'reporter', 'assignee')

class Task(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')