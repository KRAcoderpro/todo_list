from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

todo_router = SimpleRouter()
todo_router.register("tasks", views.TaskViewSet, basename='task')
todo_router.register("categories", views.CategoryViewSet, basename='category')

print(todo_router.urls)

urlpatterns = [
	path('api/v1/', include(todo_router.urls)),
	path("api/v1/register/", views.RegisterTelegramUserView.as_view()),
]
