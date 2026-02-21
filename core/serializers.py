from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Assignment, Submission

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Add/remove fields as you prefer; this is a safe default set
        fields = ["id", "username", "email", "first_name", "last_name"]



class AssignmentSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Assignment
        fields = [
            "id", "title", "description", "due_at", "points",
            "created_by", "created_at", "updated_at"
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.ReadOnlyField(source="assignment.title")
    student_username = serializers.ReadOnlyField(source="student.username")

    class Meta:
        model = Submission
        fields = [
            "id", "assignment", "assignment_title",
            "student", "student_username",
            "attempt", "code", "answer",
            "status", "score", "feedback",
            "submitted_at", "graded_at",
        ]
        read_only_fields = ["status", "submitted_at", "graded_at"]


class GradeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["score", "feedback", "status"]