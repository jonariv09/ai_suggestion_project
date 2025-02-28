from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from services.suggestions import SuggestionService

class GenerateSuggestionsAPIView(GenericAPIView):
  def __init__(self):
    self.suggestion_service = SuggestionService()

  def post(self, request):
    response = self.suggestion_service.create_suggestions()
    
    return Response(response, status=status.HTTP_200_OK)
