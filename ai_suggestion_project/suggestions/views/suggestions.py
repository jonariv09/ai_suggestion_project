import json
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from ai_suggestion_project.suggestions.services import SuggestionService
import json

class GenerateSuggestionsAPIView(GenericAPIView):
  def __init__(self):
    self.suggestion_service = SuggestionService()

  def post(self, request):
    best_matches = self.suggestion_service.create_suggestions(request.data)

    return Response(best_matches.tolist(), status=status.HTTP_200_OK)
