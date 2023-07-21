from rest_framework import serializers
from .models import User
from .models import Quiz, Question, Choice, Submission

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'topic', 'difficulty_level', 'date_created', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop('choices')
            question = Question.objects.create(quiz=quiz, **question_data)

            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)

        return quiz

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['score']

    def create(self, validated_data):
        user = self.context['request'].user
        quiz = self.context['quiz']
        score = 0

        for question in quiz.questions.all():
            user_choice_id = validated_data.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = Choice.objects.get(pk=user_choice_id)
                if user_choice.is_correct:
                    score += 1

        submission = Submission.objects.create(user=user, quiz=quiz, score=score)
        return submission

class UserProfileSerializer(serializers.ModelSerializer):
    created_quizzes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'created_quizzes']
