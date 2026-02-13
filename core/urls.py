from django.urls import path
from .views_auth import MyTokenObtainPairView
from . import views_student, views_teacher, views_code, views_ai

urlpatterns = [
    # Auth
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Student
    path('student/assignments/', views_student.StudentAssignmentsList.as_view()),
    path('student/submit/', views_student.submit_assignment),
    path('student/run-code/', views_code.run_code),
    path('student/ai-hint/', views_ai.ai_hint),

    # Teacher
    path('teacher/students/', views_teacher.TeacherStudentsList.as_view()),
    path('teacher/students/<int:student_id>/submissions/', views_teacher.student_submissions),
    path('teacher/assignments/', views_teacher.TeacherAssignmentsList.as_view()),
    path('teacher/assignments/<int:assignment_id>/submissions/', views_teacher.assignment_submissions),
]