from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Assignment, Submission
from .serializers import (
    AssignmentSerializer,
    SubmissionSerializer,
    GradeSubmissionSerializer
)
from .permissions import IsTeacher, IsStudent


# -----------------
# TEACHER ENDPOINTS
# -----------------

class TeacherAssignmentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeacherAssignmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()

    def get_queryset(self):
        # Teachers can only access their own assignments
        return Assignment.objects.filter(created_by=self.request.user)


class TeacherAssignmentSubmissions(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        assignment_id = self.kwargs["assignment_id"]
        assignment = get_object_or_404(
            Assignment, id=assignment_id, created_by=self.request.user
        )
        return assignment.submissions.all()


class TeacherGradeSubmission(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = GradeSubmissionSerializer
    queryset = Submission.objects.all()
    lookup_url_kwarg = "submission_id"

    def update(self, request, *args, **kwargs):
        submission = self.get_object()
        # Ensure the teacher owns the assignment
        if submission.assignment.created_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop("partial", True)
        serializer = self.get_serializer(submission, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.status == "graded" and not instance.graded_at:
            instance.graded_at = timezone.now()
            instance.save(update_fields=["graded_at"])
        return Response(SubmissionSerializer(instance).data)


# ----------------
# STUDENT ENDPOINTS
# ----------------

class StudentAssignmentList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    # Later you can filter by class/enrollment. For now: show all.


class StudentAssignmentRetrieve(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()


class StudentSubmitAssignment(generics.CreateAPIView):
    """
    POST body: { "assignment": <id>, "code": "...", "answer": "..." }
    Creates a new attempt (attempt = last + 1).
    """
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        assignment_id = request.data.get("assignment")
        assignment = get_object_or_404(Assignment, id=assignment_id)
        last = Submission.objects.filter(
            assignment=assignment, student=request.user
        ).order_by("-attempt").first()
        attempt = (last.attempt + 1) if last else 1

        sub = Submission.objects.create(
            assignment=assignment,
            student=request.user,
            attempt=attempt,
            code=request.data.get("code", ""),
            answer=request.data.get("answer", ""),
            status="submitted",
        )
        return Response(SubmissionSerializer(sub).data, status=status.HTTP_201_CREATED)


class StudentSubmissionList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)