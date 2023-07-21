from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Quiz, Question, Choice, Submission
from .serializers import UserSerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer, SubmissionSerializer, UserProfileSerializer
from .permissions import IsAdminOrSelf
from .models import User
from django.db.models import Avg, Count, Q
from rest_framework.response import Response
from django.db import models
from django.db.models import Avg, Count, Max, Min




class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuizListView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class UserQuizUpdateView(generics.UpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            self.permission_denied(self.request)
        return obj

class UserQuizDeleteView(generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        if obj.user != self.request.user:
            self.permission_denied(self.request)

        return obj

class QuizSubmissionView(generics.CreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        quiz = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(quiz=quiz, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

class QuizResultsView(generics.ListAPIView):
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.filter(user=user)

class QuizFilterView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        topic = self.request.query_params.get('topic')
        difficulty_level = self.request.query_params.get('difficulty_level')
        date_created = self.request.query_params.get('date_created')

        queryset = Quiz.objects.all()

        if topic:
            queryset = queryset.filter(topic__iexact=topic)

        if difficulty_level:
            queryset = queryset.filter(difficulty_level__iexact=difficulty_level)

        if date_created:
            queryset = queryset.filter(date_created=date_created)

        return queryset

class QuizAnalyticsView(generics.RetrieveAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        quiz_id = instance.id

        
        no_of_quizzes = Quiz.objects.count()

       
        no_of_quiz_takers = Submission.objects.filter(quiz_id=quiz_id).values('user').distinct().count()

        quiz_overview = {
            "no_of_quizzes": no_of_quizzes,
            "no_of_quiz_takers": no_of_quiz_takers,
        }

        serializer = self.get_serializer(instance)
        return Response({"quiz_overview": quiz_overview})

        

# class QuizPerformanceView(generics.RetrieveAPIView):
#     serializer_class = QuizSerializer

#     def get_queryset(self):
#         return Quiz.objects.all()

#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         quiz_id = instance.id

        
#         average_score_for_quiz = Submission.objects.filter(quiz_id=quiz_id).aggregate(average_score=Avg('score'))['average_score']

        
#         total_attempts_for_quiz = Submission.objects.filter(quiz_id=quiz_id).count()

      
#         pass_percentage_for_quiz = Submission.objects.filter(quiz_id=quiz_id, score__gte=50).count() * 100 / total_attempts_for_quiz

        
#         instance.average_score_for_quiz = average_score_for_quiz
#         instance.total_attempts_for_quiz = total_attempts_for_quiz
#         instance.pass_percentage_for_quiz = pass_percentage_for_quiz

#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)



# class QuizPerformanceView(generics.RetrieveAPIView):
#     serializer_class = QuizSerializer

#     def get_queryset(self):
#         return Quiz.objects.all()

#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         quiz_id = instance.id

#         analytics = Submission.objects.filter(quiz_id=quiz_id).aggregate(
#             average_score=Avg('score'),
#             total_attempts=Count('id'),
#             pass_percentage=Count('id', filter=Q(score__gte=50)) * 100 / Count('id')
#         )

#         instance.average_score = analytics['average_score']
#         instance.total_attempts = analytics['total_attempts']
#         instance.pass_percentage = analytics['pass_percentage']

#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            return user
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)


class UserManagementListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class UserManagementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrSelf]
class QuizAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        total_quizzes = Quiz.objects.count()
        total_quiz_takers = Submission.objects.values('user').distinct().count()
        average_quiz_score = Submission.objects.aggregate(avg_score=Avg('score'))['avg_score']

        quizzes = Quiz.objects.all()
        avgscores_of_eachquiz= quizzes.annotate(avg_score=Avg('userquizresponse__score')).values('title', 'avg_score')
        highest_score = Submission.objects.aggregate(max_score=Max('score'))['max_score']
        lowest_score = Submission.objects.aggregate(min_score=Min('score'))['min_score']
        quiz_taken_counts = Submission.objects.values('quiz__title').annotate(quiz_count=Count('quiz'))


        question_responses_count = Submission.objects.values('quiz__questions__qstn').annotate(response_count=Count('quiz'))
        least_answered = question_responses_count.order_by('response_count')
        most_answered = question_responses_count.order_by('-response_count')
        most_answered_questions = [item['quiz__questions__qstn'] for item in most_answered]
        least_answered_questions = [item['quiz__questions__qstn'] for item in least_answered]


        total_users=User.objects.count()
        passed_users = Submission.objects.filter(score__gte=40).values('user').distinct().count()
        percentage_of_users= (passed_users/total_users)*100


        Quiz_Overview= {
            'total_quizzes': total_quizzes,
            'total_quiz_takers': total_quiz_takers,
            'average_quiz_score': average_quiz_score,
        }

        Performance_Metrics= {
            'quiz_taken_counts': list(quiz_taken_counts),
            'average_scores': list(avgscores_of_eachquiz),  
            'highest_score': highest_score,
            'lowest_score': lowest_score,
        }

        Question_Statistics = {
            "most_answered_questions":most_answered_questions,
            "least_answered_questions":least_answered_questions
        }

        Percentage = {
            "percentage_of_users_passed":percentage_of_users,
        }

        return Response({
            'Quiz_Overview': Quiz_Overview,
            'Performance_Metrics': Performance_Metrics,
            'Question_Statistics': Question_Statistics,
            'percentage_of_users_passed':percentage_of_users
        })