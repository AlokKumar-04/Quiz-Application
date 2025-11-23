# 🎓 QuizMaster - Django Quiz Application

A comprehensive, feature-rich quiz application built with Django, Bootstrap 5, and JavaScript. Take quizzes, track your progress, and compete on leaderboards!

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django Version](https://img.shields.io/badge/django-4.2%2B-green)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.3-purple)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Sample Data](#sample-data)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🎯 Core Features

- **User Authentication System**
  - User registration with email validation
  - Login/Logout functionality
  - User profiles with statistics
  - Password validation and security

- **Quiz Management**
  - Create, edit, and delete quizzes (Admin)
  - Multiple-choice questions
  - Category-based organization
  - Difficulty levels (Easy, Medium, Hard)
  - Time limits for each quiz
  - Maximum attempt limits
  - Passing score configuration

- **Quiz Taking Experience**
  - Interactive quiz interface
  - Real-time countdown timer
  - Question navigation (Next/Previous)
  - Progress tracking
  - Auto-submit on time expiry
  - Review answers after submission

- **Results & Analytics**
  - Instant score calculation
  - Percentage and grade display
  - Correct/incorrect answer review
  - Detailed performance analysis
  - Quiz attempt history
  - Personal statistics dashboard

- **Additional Features**
  - Leaderboard for each quiz
  - Category-based filtering
  - Search functionality
  - Responsive design (mobile-friendly)
  - Achievement system
  - Profile customization

---

## 🖼️ Screenshots

### Homepage
Beautiful landing page with featured quizzes and categories.

### Quiz Taking Interface
Interactive interface with timer, progress bar, and easy navigation.

### Dashboard
Comprehensive user dashboard with statistics and recent attempts.

### Results Page
Detailed results with performance analysis and review options.

---

## 🛠️ Technologies Used

### Backend
- **Django 4.2+** - Python web framework
- **SQLite** - Database (Development)
- **Python 3.8+** - Programming language

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling
- **Bootstrap 5.3** - UI Framework
- **JavaScript (ES6)** - Client-side scripting
- **Font Awesome 6.4** - Icons

### Additional Libraries
- **django-crispy-forms** - Form rendering
- **crispy-bootstrap5** - Bootstrap 5 support
- **Pillow** - Image handling

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quiz-app.git
   cd quiz-app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir -p media/profile_pics
   mkdir -p static/css static/js static/images
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data (Optional)**
   ```bash
   python manage.py load_sample_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Homepage: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/`

---

## 🚀 Usage

### For Users

1. **Register an Account**
   - Click "Register" in the navigation bar
   - Fill in the registration form
   - Verify your email (if enabled)

2. **Browse Quizzes**
   - View all available quizzes
   - Filter by category, difficulty, or search
   - Read quiz details before starting

3. **Take a Quiz**
   - Click "Start Quiz" on any quiz detail page
   - Answer questions within the time limit
   - Navigate between questions
   - Submit when complete

4. **View Results**
   - See your score immediately
   - Review correct and incorrect answers
   - Track your progress in the dashboard

5. **Check Leaderboard**
   - View top performers for each quiz
   - Compare your scores with others

### For Administrators

1. **Access Admin Panel**
   - Go to `http://127.0.0.1:8000/admin/`
   - Login with superuser credentials

2. **Create Categories**
   - Navigate to Categories
   - Add new categories with descriptions

3. **Create Quizzes**
   - Click "Add Quiz"
   - Fill in quiz details (title, description, category, etc.)
   - Set time limit and passing score

4. **Add Questions**
   - Create questions for your quiz
   - Add multiple choice options
   - Mark the correct answer
   - Assign marks for each question

5. **Manage Users**
   - View all registered users
   - Check user statistics
   - View quiz attempts

---

## 📁 Project Structure

```
quiz_app/
│
├── quiz_project/              # Main project directory
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── quiz/                      # Main application
│   ├── migrations/           # Database migrations
│   ├── templates/            # HTML templates
│   │   └── quiz/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── quiz_list.html
│   │       ├── quiz_detail.html
│   │       ├── quiz_take.html
│   │       ├── quiz_result.html
│   │       ├── quiz_review.html
│   │       ├── dashboard.html
│   │       ├── leaderboard.html
│   │       └── category_quizzes.html
│   ├── management/
│   │   └── commands/
│   │       └── load_sample_data.py
│   ├── admin.py              # Admin configuration
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── urls.py               # App URL patterns
│   ├── forms.py              # Django forms
│   └── apps.py
│
├── templates/
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
├── static/                    # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
├── media/                     # User uploads
│   └── profile_pics/
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings Configuration

Key settings in `quiz_project/settings.py`:

```python
# Time zone
TIME_ZONE = 'Asia/Kolkata'  # Change to your timezone

# Login settings
LOGIN_REDIRECT_URL = 'quiz:home'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'quiz:home'

# Session settings
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True
```

---

## 📊 Sample Data

The application includes a management command to load sample data:

```bash
python manage.py load_sample_data
```

This will create:
- 4 Categories (Python Programming, General Knowledge, Mathematics, Science)
- 4 Complete Quizzes with questions
- Multiple choice questions with correct answers

### Sample Quizzes Included:

1. **Python Programming Fundamentals** (5 questions, Easy)
2. **World General Knowledge** (5 questions, Medium)
3. **Basic Mathematics Quiz** (4 questions, Easy)
4. **Basic Science Knowledge** (4 questions, Medium)

---

## 🔌 API Endpoints

### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage |
| GET | `/quizzes/` | List all quizzes |
| GET | `/quiz/<id>/` | Quiz details |
| GET | `/category/<id>/` | Quizzes by category |
| GET | `/register/` | Registration page |
| GET | `/login/` | Login page |
| POST | `/logout/` | Logout user |

### Protected Endpoints (Login Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | User dashboard |
| GET | `/quiz/<id>/start/` | Start quiz attempt |
| GET | `/quiz/<id>/take/` | Take quiz |
| POST | `/quiz/submit/` | Submit quiz answers |
| GET | `/attempt/<id>/result/` | View results |
| GET | `/attempt/<id>/review/` | Review answers |
| GET | `/leaderboard/<id>/` | Quiz leaderboard |

### Admin Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/` | Admin dashboard |
| CRUD | `/admin/quiz/` | Manage quizzes |
| CRUD | `/admin/quiz/question/` | Manage questions |
| CRUD | `/admin/quiz/category/` | Manage categories |

---

## 📱 Features in Detail

### User Authentication
- Secure password hashing
- Email validation
- Password strength requirements
- Session management
- Remember me functionality

### Quiz System
- **Categories**: Organize quizzes by topics
- **Difficulty Levels**: Easy, Medium, Hard
- **Time Management**: Countdown timer with auto-submit
- **Attempt Limits**: Configure maximum attempts per quiz
- **Passing Score**: Set minimum percentage to pass

### Dashboard Features
- Total quizzes taken
- Pass/fail statistics
- Average score calculation
- Recent attempt history
- Achievement badges
- Performance graphs

### Leaderboard
- Top 20 performers per quiz
- Score ranking
- Time taken comparison
- User position highlighting

### Admin Panel Features
- Bulk actions for questions
- Inline editing for choices
- Rich text editor support
- User management
- Statistics and reports

---

## 🎨 Customization

### Changing Theme Colors

Edit `static/css/style.css`:

```css
:root {
    --primary-color: #0d6efd;  /* Blue */
    --success-color: #198754;  /* Green */
    --danger-color: #dc3545;   /* Red */
    --warning-color: #ffc107;  /* Yellow */
    --info-color: #0dcaf0;     /* Cyan */
}
```

### Adding Custom Categories

1. Go to Admin Panel
2. Navigate to Categories
3. Click "Add Category"
4. Enter name and description
5. Save

### Modifying Quiz Settings

Edit quiz settings in admin or in `models.py`:

```python
class Quiz(models.Model):
    time_limit = models.IntegerField(default=10)  # Change default
    passing_score = models.IntegerField(default=50)  # Change default
    max_attempts = models.IntegerField(default=3)  # Change default
```

---

## 🧪 Testing

Run tests using Django's test framework:

```bash
python manage.py test
```

### Manual Testing Checklist

- [ ] User registration works
- [ ] Login/logout functionality
- [ ] Quiz listing and filtering
- [ ] Quiz taking with timer
- [ ] Answer submission
- [ ] Results display correctly
- [ ] Dashboard shows accurate stats
- [ ] Admin panel accessible
- [ ] Leaderboard updates
- [ ] Responsive design on mobile

---

## 🐛 Troubleshooting

### Common Issues

**1. Migration Errors**
```bash
python manage.py migrate --run-syncdb
```

**2. Static Files Not Loading**
```bash
python manage.py collectstatic
```

**3. Database Locked Error**
```bash
# Close all connections and restart server
```

**4. Template Not Found**
- Check `TEMPLATES` setting in `settings.py`
- Verify template file paths
- Ensure `APP_DIRS` is `True`

**5. Media Files Not Displaying**
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Verify URL configuration includes media patterns

---

## 📈 Future Enhancements

- [ ] Multiple question types (True/False, Fill in the blanks)
- [ ] Quiz categories with subcategories
- [ ] Social media sharing
- [ ] Email notifications
- [ ] Certificate generation
- [ ] Quiz recommendations based on performance
- [ ] Mobile application (React Native)
- [ ] Real-time multiplayer quizzes
- [ ] Quiz analytics dashboard
- [ ] Export results to PDF/Excel
- [ ] Dark mode theme
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Coding Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Test your changes before submitting

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Font Awesome Icons
- Stack Overflow Community
- All contributors and testers

---

## 📞 Contact & Support

- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Issues**: [GitHub Issues](https://github.com/yourusername/quiz-app/issues)

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Python Documentation](https://docs.python.org/3/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Made with ❤️ using Django and Bootstrap**

---

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- User authentication system
- Quiz creation and management
- Quiz taking with timer
- Results and analytics
- Dashboard and leaderboard
- Responsive design
- Admin panel

---

*Last Updated: November 2025*