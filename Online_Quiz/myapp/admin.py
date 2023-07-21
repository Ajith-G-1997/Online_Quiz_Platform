from django.contrib import admin
from .models import User, Quiz, Question, Choice, Submission

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'difficulty_level', 'date_created']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'user', 'score']
