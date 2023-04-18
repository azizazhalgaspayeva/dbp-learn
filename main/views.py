from rest_framework import viewsets
import django_filters
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.permissions import IsAdminUser, IsAuthenticated

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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser(), ]        
        return super(UserViewSet, self).get_permissions()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.Status.choices)
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all(),conjoined=True)
    reporter = django_filters.CharFilter(lookup_expr='icontains')
    assignee = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Task
        fields = ('status', 'tags', 'reporter', 'assignee',)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser(), ]        
        return super(UserViewSet, self).get_permissions()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminUser(), ]        
        return super(UserViewSet, self).get_permissions()
