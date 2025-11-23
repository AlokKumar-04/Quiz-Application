from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz.models import Category, Quiz, Question, Choice


class Command(BaseCommand):
    help = 'Load sample quiz data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # Create Categories
        python_cat = Category.objects.get_or_create(
            name='Python Programming',
            defaults={'description': 'Test your Python programming knowledge'}
        )[0]

        gk_cat = Category.objects.get_or_create(
            name='General Knowledge',
            defaults={'description': 'Questions about world facts and trivia'}
        )[0]

        math_cat = Category.objects.get_or_create(
            name='Mathematics',
            defaults={'description': 'Basic to intermediate math problems'}
        )[0]

        science_cat = Category.objects.get_or_create(
            name='Science',
            defaults={'description': 'Physics, Chemistry, and Biology questions'}
        )[0]

        # Python Basics Quiz
        python_quiz = Quiz.objects.create(
            title='Python Programming Fundamentals',
            description='Test your knowledge of Python basics including syntax, data types, and functions.',
            category=python_cat,
            difficulty='easy',
            time_limit=10,
            passing_score=60,
            max_attempts=3,
            created_by=admin_user
        )

        questions_data = [
            {
                'text': 'What is the correct file extension for Python files?',
                'marks': 1,
                'choices': [
                    ('pyth', False),
                    ('.pt', False),
                    ('.py', True),
                    ('.python', False)
                ]
            },
            {
                'text': 'Which keyword is used to create a function in Python?',
                'marks': 1,
                'choices': [
                    ('function', False),
                    ('def', True),
                    ('func', False),
                    ('define', False)
                ]
            },
            {
                'text': 'What is the output of: print(2 ** 3)?',
                'marks': 1,
                'choices': [
                    ('6', False),
                    ('8', True),
                    ('9', False),
                    ('23', False)
                ]
            },
            {
                'text': 'Which data type is mutable in Python?',
                'marks': 1,
                'choices': [
                    ('List', True),
                    ('Tuple', False),
                    ('String', False),
                    ('Integer', False)
                ]
            },
            {
                'text': 'What does the len() function do?',
                'marks': 1,
                'choices': [
                    ('Returns the last element', False),
                    ('Returns the length of an object', True),
                    ('Returns the type of an object', False),
                    ('Deletes an object', False)
                ]
            }
        ]

        for idx, q_data in enumerate(questions_data, 1):
            question = Question.objects.create(
                quiz=python_quiz,
                question_text=q_data['text'],
                marks=q_data['marks'],
                order=idx
            )
            for choice_idx, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=choice_idx
                )

        # General Knowledge Quiz
        gk_quiz = Quiz.objects.create(
            title='World General Knowledge',
            description='Test your knowledge about world geography, history, and culture.',
            category=gk_cat,
            difficulty='medium',
            time_limit=12,
            passing_score=50,
            max_attempts=3,
            created_by=admin_user
        )

        gk_questions = [
            {
                'text': 'What is the capital of France?',
                'marks': 1,
                'choices': [
                    ('London', False),
                    ('Paris', True),
                    ('Berlin', False),
                    ('Rome', False)
                ]
            },
            {
                'text': 'Who painted the Mona Lisa?',
                'marks': 1,
                'choices': [
                    ('Vincent van Gogh', False),
                    ('Leonardo da Vinci', True),
                    ('Pablo Picasso', False),
                    ('Michelangelo', False)
                ]
            },
            {
                'text': 'What is the largest planet in our solar system?',
                'marks': 1,
                'choices': [
                    ('Saturn', False),
                    ('Earth', False),
                    ('Jupiter', True),
                    ('Neptune', False)
                ]
            },
            {
                'text': 'In which year did World War II end?',
                'marks': 1,
                'choices': [
                    ('1943', False),
                    ('1944', False),
                    ('1945', True),
                    ('1946', False)
                ]
            },
            {
                'text': 'What is the smallest country in the world?',
                'marks': 1,
                'choices': [
                    ('Monaco', False),
                    ('Vatican City', True),
                    ('San Marino', False),
                    ('Liechtenstein', False)
                ]
            }
        ]

        for idx, q_data in enumerate(gk_questions, 1):
            question = Question.objects.create(
                quiz=gk_quiz,
                question_text=q_data['text'],
                marks=q_data['marks'],
                order=idx
            )
            for choice_idx, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=choice_idx
                )

        # Mathematics Quiz
        math_quiz = Quiz.objects.create(
            title='Basic Mathematics Quiz',
            description='Test your basic mathematical skills with arithmetic and simple geometry.',
            category=math_cat,
            difficulty='easy',
            time_limit=15,
            passing_score=60,
            max_attempts=3,
            created_by=admin_user
        )

        math_questions = [
            {
                'text': 'What is 15 + 27?',
                'marks': 1,
                'choices': [
                    ('41', False),
                    ('42', True),
                    ('43', False),
                    ('44', False)
                ]
            },
            {
                'text': 'What is the square root of 64?',
                'marks': 1,
                'choices': [
                    ('6', False),
                    ('7', False),
                    ('8', True),
                    ('9', False)
                ]
            },
            {
                'text': 'What is 12 × 8?',
                'marks': 1,
                'choices': [
                    ('94', False),
                    ('96', True),
                    ('98', False),
                    ('100', False)
                ]
            },
            {
                'text': 'What is 50% of 200?',
                'marks': 1,
                'choices': [
                    ('50', False),
                    ('100', True),
                    ('150', False),
                    ('200', False)
                ]
            }
        ]

        for idx, q_data in enumerate(math_questions, 1):
            question = Question.objects.create(
                quiz=math_quiz,
                question_text=q_data['text'],
                marks=q_data['marks'],
                order=idx
            )
            for choice_idx, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=choice_idx
                )

        # Science Quiz
        science_quiz = Quiz.objects.create(
            title='Basic Science Knowledge',
            description='Test your knowledge of basic science concepts from physics, chemistry, and biology.',
            category=science_cat,
            difficulty='medium',
            time_limit=12,
            passing_score=65,
            max_attempts=2,
            created_by=admin_user
        )

        science_questions = [
            {
                'text': 'What is the chemical formula for water?',
                'marks': 1,
                'choices': [
                    ('CO2', False),
                    ('H2O', True),
                    ('O2', False),
                    ('H2', False)
                ]
            },
            {
                'text': 'What is the powerhouse of the cell?',
                'marks': 1,
                'choices': [
                    ('Nucleus', False),
                    ('Mitochondria', True),
                    ('Ribosome', False),
                    ('Chloroplast', False)
                ]
            },
            {
                'text': 'What planet is known as the Red Planet?',
                'marks': 1,
                'choices': [
                    ('Venus', False),
                    ('Mars', True),
                    ('Jupiter', False),
                    ('Saturn', False)
                ]
            },
            {
                'text': 'At what temperature does water freeze (in Celsius)?',
                'marks': 1,
                'choices': [
                    ('-10°C', False),
                    ('0°C', True),
                    ('10°C', False),
                    ('32°C', False)
                ]
            }
        ]

        for idx, q_data in enumerate(science_questions, 1):
            question = Question.objects.create(
                quiz=science_quiz,
                question_text=q_data['text'],
                marks=q_data['marks'],
                order=idx
            )
            for choice_idx, (choice_text, is_correct) in enumerate(q_data['choices'], 1):
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    is_correct=is_correct,
                    order=choice_idx
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))
        self.stdout.write(f'Created {Category.objects.count()} categories')
        self.stdout.write(f'Created {Quiz.objects.count()} quizzes')
        self.stdout.write(f'Created {Question.objects.count()} questions')
        self.stdout.write(f'Created {Choice.objects.count()} choices')