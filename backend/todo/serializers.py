from rest_framework import serializers
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'created_at',
            'due_date',
            'finished',
            'category',
            'category_id'
        ]
