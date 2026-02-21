from rest_framework.permissions import BasePermission


def user_in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Teacher")


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, "Student")