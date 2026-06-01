from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    # ModelSerializer maps the Django model to JSON and validates model fields automatically.
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'course']
        read_only_fields = ['id']
