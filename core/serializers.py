from rest_framework import serializers
from .models import User, Assignment, Submission, Class

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']

class AssignmentSerializer(serializers.ModelSerializer):
    class_obj = ClassSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'starter_code', 'created_at', 'due_date', 'class_obj']

class SubmissionSerializer(serializers.ModelSerializer):
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'code', 'output', 'created_at', 'updated_at']