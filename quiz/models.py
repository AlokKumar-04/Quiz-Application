from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Category(models.Model):
    """Quiz categories like Math, Science, History, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Quiz(models.Model):
    """Main Quiz model"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    time_limit = models.IntegerField(
        help_text="Time limit in minutes",
        validators=[MinValueValidator(1), MaxValueValidator(180)]
    )
    passing_score = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Passing percentage"
    )
    is_active = models.BooleanField(default=True)
    max_attempts = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of attempts allowed"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def total_questions(self):
        return self.questions.count()
    
    def total_marks(self):
        return sum(question.marks for question in self.questions.all())


class Question(models.Model):
    """Quiz questions"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    marks = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.question_text[:50]}"
    
    def get_correct_answer(self):
        return self.choices.filter(is_correct=True).first()


class Choice(models.Model):
    """Answer choices for questions"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.question.question_text[:30]} - {self.choice_text[:30]}"


class QuizAttempt(models.Model):
    """Records of quiz attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_marks = models.IntegerField()
    percentage = models.FloatField(default=0.0)
    time_taken = models.IntegerField(help_text="Time taken in seconds")
    is_passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_marks}"
    
    def calculate_percentage(self):
        if self.total_marks > 0:
            self.percentage = (self.score / self.total_marks) * 100
        else:
            self.percentage = 0
        return self.percentage
    
    def check_passed(self):
        self.is_passed = self.percentage >= self.quiz.passing_score
        return self.is_passed


class Answer(models.Model):
    """User answers for each question"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('attempt', 'question')
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}"


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    total_quizzes_taken = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def update_stats(self):
        attempts = QuizAttempt.objects.filter(user=self.user)
        self.total_quizzes_taken = attempts.count()
        self.total_score = sum(attempt.score for attempt in attempts)
        self.save()