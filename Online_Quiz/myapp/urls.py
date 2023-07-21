from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserSignUpView, QuizListView,QuizPerformanceView, QuizDetailView,UserQuizUpdateView, UserQuizDeleteView, QuizSubmissionView, QuizResultsView, QuizFilterView, QuizAnalyticsView, UserProfileView, UserManagementListView, UserManagementDetailView

urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='signup'),

    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/update/', UserQuizUpdateView.as_view(), name='quiz-update'),
    path('quizzes/<int:pk>/delete/', UserQuizDeleteView.as_view(), name='quiz-delete'),
    path('quizzes/<int:pk>/submit/', QuizSubmissionView.as_view(), name='quiz-submit'),
    path('result/view/', QuizResultsView.as_view(), name='quiz-results'),
    path('quizzes/filter/', QuizFilterView.as_view(), name='quiz-filter'),
    path('/analytics/', QuizAnalyticsView.as_view(), name='quiz-analytics'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserManagementListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserManagementDetailView.as_view(), name='user-detail'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('quizzes/<int:pk>/performance/', QuizPerformanceView.as_view(), name='quiz-performance'),
]
