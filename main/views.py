from rest_framework import viewsets
import django_filters

from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ('first_name',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all(),conjoined=True)
    reporter = django_filters.CharFilter(lookup_expr='icontains')
    assignee = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Task
        fields = ('status', 'tags', 'reporter', 'assignee',)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("reporter", "assignee").prefetch_related("tags")
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
