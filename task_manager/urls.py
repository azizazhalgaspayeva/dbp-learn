from main.admin import task_manager_admin_site
from django.urls import path, include
from rest_framework import routers

from main import views


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'tasks', views.TaskViewSet, basename='tasks')
router.register(r'tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path("api/", include(router.urls)),
]
