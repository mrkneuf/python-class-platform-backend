import io
import contextlib
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_code(request):
    code = request.data.get('code', '')
    stdout = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, {"__builtins__": {}})
        output = stdout.getvalue()
    except Exception as e:
        output = f"Error: {e}"
    return Response({'output': output})