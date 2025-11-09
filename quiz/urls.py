from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    
    # Quiz taking
    path('quiz/<int:pk>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:pk>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    
    # Results and review
    path('attempt/<int:pk>/result/', views.quiz_result, name='quiz_result'),
    path('attempt/<int:pk>/review/', views.quiz_review, name='quiz_review'),
    
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/<int:pk>/', views.leaderboard, name='leaderboard'),
    
    # Category filtering
    path('category/<int:pk>/', views.category_quizzes, name='category_quizzes'),
]