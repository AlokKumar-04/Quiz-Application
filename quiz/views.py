
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Avg, Q
from datetime import timedelta
import json

from .models import (
    Quiz, Question, Choice, QuizAttempt, 
    Answer, Category, UserProfile
)

# Create your views here.
def home(request):
    categories = Category.objects.all()
    featured_quizzes = Quiz.objects.filter(is_active=True)[:6]
    
    # Get statistics
    total_quizzes = Quiz.objects.filter(is_active=True).count()
    total_users = QuizAttempt.objects.values('user').distinct().count()
    
    context = {
        'categories': categories,
        'featured_quizzes': featured_quizzes,
        'total_quizzes': total_quizzes,
        'total_users': total_users,
    }
    return render(request, 'quiz/home.html', context)

def quiz_list(request):
    return render(request, 'quiz/quiz_list.html')

def quiz_detail(request):
    return render(request, 'quiz/quiz_details.html')

def start_quiz(request):
    pass

def take_quiz(request):
    pass

def submit_quiz(request):
    pass

def quiz_result(request):
    pass

def quiz_review(request):
    pass

def dashboard(request):
    pass

def leaderboard(request):
    pass

def category_quizzes(request):
    pass
