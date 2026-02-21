from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_auth import MyTokenObtainPairView
from . import views_student, views_teacher, views_code, views_ai

from .views_assignments import (
    TeacherAssignmentListCreate,
    TeacherAssignmentRetrieveUpdateDestroy,
    TeacherAssignmentSubmissions,
    TeacherGradeSubmission,
    StudentAssignmentList,
    StudentAssignmentRetrieve,
    StudentSubmitAssignment,
    StudentSubmissionList,
)


urlpatterns = [
    # Auth
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Student
    
    path("student/assignments/", StudentAssignmentList.as_view()),
    path("student/assignments/<int:pk>/", StudentAssignmentRetrieve.as_view()),
    path("student/submit/", StudentSubmitAssignment.as_view()),
    path("student/submissions/", StudentSubmissionList.as_view()),
    path('student/run-code/', views_code.run_code),
    path('student/ai-hint/', views_ai.ai_hint),

    # Teacher
    path("teacher/assignments/", TeacherAssignmentListCreate.as_view()),
    path("teacher/assignments/<int:pk>/", TeacherAssignmentRetrieveUpdateDestroy.as_view()),
    path("teacher/assignments/<int:assignment_id>/submissions/", TeacherAssignmentSubmissions.as_view()),
    path("teacher/submissions/<int:submission_id>/grade/", TeacherGradeSubmission.as_view()),

]