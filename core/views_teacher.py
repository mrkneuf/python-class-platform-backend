from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import User, Assignment, Submission, Class
from .serializers import UserSerializer, AssignmentSerializer, SubmissionSerializer
from .permissions import IsTeacher

class TeacherStudentsList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        teacher = self.request.user
        classes = Class.objects.filter(teacher=teacher)
        student_ids = set()
        for c in classes:
            for e in c.enrollments.all():
                student_ids.add(e.student_id)
        return User.objects.filter(id__in=student_ids, role='student')

@api_view(['GET'])
@permission_classes([IsTeacher])
def student_submissions(request, student_id):
    teacher = request.user
    student = User.objects.get(id=student_id, role='student')
    classes = Class.objects.filter(teacher=teacher)
    assignments = Assignment.objects.filter(class_obj__in=classes)
    submissions = Submission.objects.filter(student=student, assignment__in=assignments)
    return Response(SubmissionSerializer(submissions, many=True).data)

class TeacherAssignmentsList(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        teacher = self.request.user
        return Assignment.objects.filter(class_obj__teacher=teacher).order_by('-created_at')

@api_view(['GET'])
@permission_classes([IsTeacher])
def assignment_submissions(request, assignment_id):
    teacher = request.user
    assignment = Assignment.objects.get(id=assignment_id, class_obj__teacher=teacher)
    submissions = assignment.submissions.select_related('student')
    data = []
    for s in submissions:
        data.append({
            'id': s.id,
            'student': {
                'id': s.student.id,
                'username': s.student.username,
            },
            'code': s.code,
            'output': s.output,
            'created_at': s.created_at,
            'updated_at': s.updated_at,
        })
    return Response(data)