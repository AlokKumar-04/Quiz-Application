from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
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
from .forms import UserRegisterForm


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('quiz:home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


def home(request):
    """Homepage with featured quizzes"""
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
    """List all available quizzes with filtering"""
    quizzes = Quiz.objects.filter(is_active=True)
    
    # Filtering
    category_id = request.GET.get('category', '')
    difficulty = request.GET.get('difficulty', '')
    search = request.GET.get('search', '')
    
    # Convert empty strings or 'None' to None
    if category_id and category_id != 'None':
        try:
            category_id = int(category_id)
            quizzes = quizzes.filter(category_id=category_id)
        except (ValueError, TypeError):
            category_id = None
    else:
        category_id = None
    
    if difficulty and difficulty != 'None':
        quizzes = quizzes.filter(difficulty=difficulty)
    else:
        difficulty = None
    
    if search and search != 'None':
        quizzes = quizzes.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    else:
        search = None
    
    categories = Category.objects.all()
    
    context = {
        'quizzes': quizzes,
        'categories': categories,
        'selected_category': category_id,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'quiz/quiz_list.html', context)


def quiz_detail(request, pk):
    """Quiz details and preview"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    questions_count = quiz.questions.count()
    total_marks = quiz.total_marks()
    
    # Check user's previous attempts
    user_attempts = None
    attempts_left = quiz.max_attempts
    
    if request.user.is_authenticated:
        user_attempts = QuizAttempt.objects.filter(
            user=request.user, 
            quiz=quiz
        ).order_by('-completed_at')
        attempts_taken = user_attempts.count()
        attempts_left = quiz.max_attempts - attempts_taken
    
    context = {
        'quiz': quiz,
        'questions_count': questions_count,
        'total_marks': total_marks,
        'user_attempts': user_attempts,
        'attempts_left': attempts_left,
    }
    return render(request, 'quiz/quiz_detail.html', context)


@login_required
def start_quiz(request, pk):
    """Initialize a new quiz attempt"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    
    # Check if user has attempts left
    attempts_count = QuizAttempt.objects.filter(
        user=request.user, 
        quiz=quiz
    ).count()
    
    if attempts_count >= quiz.max_attempts:
        messages.error(request, 'You have reached the maximum number of attempts for this quiz.')
        return redirect('quiz:quiz_detail', pk=pk)
    
    # Check if there's an ongoing attempt
    ongoing_attempt = request.session.get(f'quiz_attempt_{pk}')
    if ongoing_attempt:
        return redirect('quiz:take_quiz', pk=pk)
    
    # Create session data for quiz
    request.session[f'quiz_attempt_{pk}'] = {
        'started_at': timezone.now().isoformat(),
        'answers': {}
    }
    
    messages.success(request, f'Quiz started! You have {quiz.time_limit} minutes.')
    return redirect('quiz:take_quiz', pk=pk)


@login_required
def take_quiz(request, pk):
    """Quiz taking page"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    
    # Check if quiz session exists
    session_key = f'quiz_attempt_{pk}'
    if session_key not in request.session:
        return redirect('quiz:start_quiz', pk=pk)
    
    questions = quiz.questions.prefetch_related('choices').all()
    
    # Calculate remaining time
    started_at = timezone.datetime.fromisoformat(
        request.session[session_key]['started_at']
    )
    if timezone.is_naive(started_at):
        started_at = timezone.make_aware(started_at)
    
    elapsed_time = (timezone.now() - started_at).total_seconds()
    time_limit_seconds = quiz.time_limit * 60
    remaining_time = max(0, time_limit_seconds - elapsed_time)
    
    # If time is up, auto-submit
    if remaining_time <= 0:
        return redirect('quiz:submit_quiz')
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'remaining_time': int(remaining_time),
    }
    return render(request, 'quiz/quiz_take.html', context)


@login_required
def submit_quiz(request):
    """Process quiz submission"""
    if request.method != 'POST':
        return redirect('quiz:home')
    
    try:
        data = json.loads(request.body)
        quiz_id = data.get('quiz_id')
        answers = data.get('answers', {})
        
        quiz = get_object_or_404(Quiz, pk=quiz_id, is_active=True)
        
        # Get session data
        session_key = f'quiz_attempt_{quiz_id}'
        if session_key not in request.session:
            return JsonResponse({'error': 'No active quiz session'}, status=400)
        
        session_data = request.session[session_key]
        started_at = timezone.datetime.fromisoformat(session_data['started_at'])
        if timezone.is_naive(started_at):
            started_at = timezone.make_aware(started_at)
        
        # Calculate time taken
        time_taken = int((timezone.now() - started_at).total_seconds())
        
        # Create quiz attempt
        total_marks = quiz.total_marks()
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            total_marks=total_marks,
            time_taken=time_taken,
            started_at=started_at
        )
        
        # Process answers
        score = 0
        for question_id, choice_id in answers.items():
            question = Question.objects.get(id=question_id, quiz=quiz)
            selected_choice = Choice.objects.get(id=choice_id, question=question)
            
            is_correct = selected_choice.is_correct
            marks_obtained = question.marks if is_correct else 0
            score += marks_obtained
            
            Answer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct,
                marks_obtained=marks_obtained
            )
        
        # Update attempt with score
        attempt.score = score
        attempt.calculate_percentage()
        attempt.check_passed()
        attempt.save()
        
        # Update user profile stats
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.update_stats()
        
        # Clear session
        del request.session[session_key]
        
        return JsonResponse({
            'success': True,
            'attempt_id': attempt.id,
            'redirect_url': f'/attempt/{attempt.id}/result/'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def quiz_result(request, pk):
    """Display quiz results"""
    attempt = get_object_or_404(QuizAttempt, pk=pk, user=request.user)
    
    # Calculate correct and incorrect answers
    correct_answers = attempt.answers.filter(is_correct=True).count()
    total_answers = attempt.answers.count()
    incorrect_answers = total_answers - correct_answers
    
    context = {
        'attempt': attempt,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_answers': total_answers,
    }
    return render(request, 'quiz/quiz_result.html', context)


@login_required
def quiz_review(request, pk):
    """Review answers after completing quiz"""
    attempt = get_object_or_404(QuizAttempt, pk=pk, user=request.user)
    answers = attempt.answers.select_related(
        'question', 'selected_choice'
    ).prefetch_related('question__choices')
    
    # Calculate statistics
    correct_answers = answers.filter(is_correct=True).count()
    total_questions = answers.count()
    incorrect_answers = total_questions - correct_answers
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_questions': total_questions,
    }
    return render(request, 'quiz/quiz_review.html', context)


@login_required
def dashboard(request):
    """User dashboard with statistics"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).select_related('quiz').order_by('-completed_at')[:10]
    
    # Statistics
    total_attempts = QuizAttempt.objects.filter(user=request.user).count()
    passed_attempts = QuizAttempt.objects.filter(
        user=request.user, 
        is_passed=True
    ).count()
    failed_attempts = total_attempts - passed_attempts
    
    avg_score = QuizAttempt.objects.filter(
        user=request.user
    ).aggregate(Avg('percentage'))['percentage__avg'] or 0
    
    context = {
        'profile': profile,
        'recent_attempts': recent_attempts,
        'total_attempts': total_attempts,
        'passed_attempts': passed_attempts,
        'failed_attempts': failed_attempts,
        'avg_score': round(avg_score, 2),
    }
    return render(request, 'quiz/dashboard.html', context)


def leaderboard(request, pk):
    """Quiz leaderboard"""
    quiz = get_object_or_404(Quiz, pk=pk, is_active=True)
    
    # Get top attempts for this quiz
    top_attempts = QuizAttempt.objects.filter(
        quiz=quiz
    ).select_related('user').order_by('-score', 'time_taken')[:20]
    
    context = {
        'quiz': quiz,
        'top_attempts': top_attempts,
    }
    return render(request, 'quiz/leaderboard.html', context)


def category_quizzes(request, pk):
    """Quizzes filtered by category"""
    category = get_object_or_404(Category, pk=pk)
    quizzes = Quiz.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'quizzes': quizzes,
    }
    return render(request, 'quiz/category_quizzes.html', context)


# Error handlers
def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)