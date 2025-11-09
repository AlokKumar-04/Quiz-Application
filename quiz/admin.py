from django.contrib import admin
from .models import Category, Quiz, Question, Choice, QuizAttempt, Answer, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_per_page = 20


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    fields = ['choice_text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'marks', 'order']
    list_filter = ['quiz', 'marks']
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    list_per_page = 20


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        'title', 
        'category', 
        'difficulty', 
        'time_limit', 
        'passing_score',
        'is_active',
        'created_by',
        'total_questions',
        'created_at'
    ]
    list_filter = ['difficulty', 'category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'created_by')
        }),
        ('Quiz Settings', {
            'fields': ('difficulty', 'time_limit', 'passing_score', 'max_attempts', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [QuestionInline]
    list_per_page = 20
    
    def save_model(self, request, obj, form, change):
        if not change:  
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['choice_text', 'question__question_text']
    list_per_page = 50


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question', 'selected_choice', 'is_correct', 'marks_obtained']
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'quiz',
        'score',
        'total_marks',
        'percentage',
        'is_passed',
        'time_taken',
        'completed_at'
    ]
    list_filter = ['is_passed', 'quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = [
        'user', 
        'quiz', 
        'score', 
        'total_marks', 
        'percentage',
        'time_taken',
        'is_passed',
        'started_at',
        'completed_at'
    ]
    inlines = [AnswerInline]
    list_per_page = 50
    
    def has_add_permission(self, request):
        return False 


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'attempt',
        'question',
        'selected_choice',
        'is_correct',
        'marks_obtained'
    ]
    list_filter = ['is_correct', 'attempt__quiz']
    search_fields = ['attempt__user__username', 'question__question_text']
    readonly_fields = ['attempt', 'question', 'selected_choice', 'is_correct', 'marks_obtained']
    list_per_page = 100
    
    def has_add_permission(self, request):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'total_quizzes_taken',
        'total_score',
        'created_at'
    ]
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_quizzes_taken', 'total_score', 'created_at']
    list_per_page = 50


admin.site.site_header = "Quiz Application Admin"
admin.site.site_title = "Quiz Admin Portal"
admin.site.index_title = "Welcome to Quiz Application Admin Panel"