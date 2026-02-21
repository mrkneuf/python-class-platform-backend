# core/serializers_auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def infer_role_for(user) -> str:
    """Return 'teacher' or 'student' based on Django Groups; '' if none."""
    if user.groups.filter(name='Teacher').exists():
        return 'teacher'
    if user.groups.filter(name='Student').exists():
        return 'student'
    return ''

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = infer_role_for(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['username'] = user.username
        data['role'] = infer_role_for(user)
        return data