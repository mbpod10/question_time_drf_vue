from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from questions.api.permissions import IsAuthorOrReadOnly
from questions.models import Question, Answer
from questions.api.serializers import QuestionSerializer, AnswerSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """ 
    ModelViewSet gives all CRUD functionality 
    lookup_field used for detail/update/delete view if user is author 
    else read only based on permission_classes 
    example http://127.0.0.1:8000/api/v1/questions/our-very-first-question-Cj2mINQn/     
    slug will be used in url to get detail view in lookup_field
    example '/questions/<content-slug>' 
    """
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    lookup_field = 'slug'

    def perform_create(self, serializer):
        """ authenticated user will be the one to create the question """
        serializer.save(author=self.request.user)


class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ get current authenticated user """
        request_user = self.request.user
        """ get slug from current question """
        kwarg_slug = self.kwargs.get("slug")
        """ search for question with slug """
        question = get_object_or_404(Question, slug=kwarg_slug)
        """ raise error if current user already answered question"""
        if question.answers.filter(author=request_user).exists():
            raise ValidationError("You have already answered this question!")
        """ create answer with author as curr user and question as filtered question """
        serializer.save(author=request_user, question=question)


class AnswerRUDAPI(generics.RetrieveUpdateDestroyAPIView):
    """ 
    retrieve the detail view of an answer with RUD func as
    long as curent auth user is author of answer
    if not author then ready only from custom permissions
     """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = 'uuid'


class AnswerListAPIView(generics.ListAPIView):
    """ retrieve all answers for a certain question """
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        """ return all answers for the question slug """
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-created_at")


class AnswerLikeAPIView(APIView):
    """ create endpoint that will allow user to like or delete like of an answer to question """
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        answer.voters.add(request.user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid):
        answer = get_object_or_404(Answer, uuid=uuid)
        answer.voters.remove(request.user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
