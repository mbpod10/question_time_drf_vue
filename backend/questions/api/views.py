from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from questions.api.permissions import IsAuthorOrReadOnly
from questions.models import Question, Answer
from questions.api.serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    """ 
    slug will be used in url to get detail view in lookup_field
     example '/questions/<content-slug>' 
    """
    lookup_field = 'slug'

    def perform_create(self, serializer):
        """ authenticated user will be the one to create the question """
        serializer.save(author=self.request.user)
