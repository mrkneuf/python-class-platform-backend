from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Assignment, Submission, Enrollment
from .serializers import AssignmentSerializer, SubmissionSerializer
from .permissions import IsStudent

class StudentAssignmentsList(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        enrolled_classes = Enrollment.objects.filter(student=user).values_list('class_obj', flat=True)
        return Assignment.objects.filter(class_obj__in=enrolled_classes).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsStudent])
def submit_assignment(request):
    user = request.user
    assignment_id = request.data.get('assignment_id')
    code = request.data.get('code', '')
    output = request.data.get('output', '')

    assignment = get_object_or_404(Assignment, id=assignment_id)
    submission, created = Submission.objects.update_or_create(
        assignment=assignment,
        student=user,
        defaults={'code': code, 'output': output},
    )
    return Response(SubmissionSerializer(submission).data)