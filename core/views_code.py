import io
import sys
import contextlib
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_code(request):
    code = request.data.get('code', '')
    stdout = io.StringIO()

    safe_builtins = {
        "print": print,
        "range": range,
        "len": len,
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
    }

    exec_globals = {"__builtins__": safe_builtins}
    exec_locals = {}

    try:
        with contextlib.redirect_stdout(stdout):
            exec(code, exec_globals, exec_locals)
        output = stdout.getvalue()
    except Exception as e:
        output = f"Error: {str(e)}"

    return Response({'output': output})