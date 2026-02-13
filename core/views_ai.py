from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_hint(request):
    code = request.data.get('code', '')
    question = request.data.get('question', '')

    # Placeholder logic – replace with real LLM call later
    hint = (
        "Think about what each line of your code is doing.\n"
        "Try printing intermediate values to see where it diverges from what you expect.\n"
        "Focus especially on loops and conditions related to your question."
    )

    return Response({'hint': hint})