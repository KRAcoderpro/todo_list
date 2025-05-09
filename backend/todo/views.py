from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Task, Category, User
from .serializers import TaskSerializer, CategorySerializer
from .permissions import TelegramIDAuth


class RegisterTelegramUserView(APIView):

    def post(self, request):
        tg_id = request.data.get("telegram_id")

        if tg_id is None:
            return Response({"error": "telegram_id is required"}, status=400)

        user, created = User.objects.get_or_create(
            telegram_id=tg_id
        )
        return Response({"user_id": user.id}, status=201 if created else 200)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [TelegramIDAuth]
    filterset_fields = ["category", "finished"]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [TelegramIDAuth]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["get"], detail=False, url_path="default")
    def get_default_categories(self, request):
        categories = Category.objects.filter(user=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
