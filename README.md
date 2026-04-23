# StudyMind - AI-Powered Study Assistant

![StudyMind](https://img.shields.io/badge/Django-4.2-green) ![Python](https://img.shields.io/badge/Python-3.11-blue) ![OpenAI](https://img.shields.io/badge/OpenAI-API-orange) ![License](https://img.shields.io/badge/License-MIT-yellow)

**StudyMind** is an intelligent web application that leverages basic NLP to enhance the learning experience of students. It uses natural language processing to summarize study notes, generate practice questions, and provide keyword-based tutoring.

## 🎯 Features

### Core Features
- **📚 Study Material Management**: Upload, organize, and manage your study notes and materials
- **✨ Basic Summaries**: Automatically generate extractive summaries using NLP
- **❓ Practice Questions**: Get NLP-generated practice questions based on content keywords
- **🤖 Keyword-Based Tutor**: Ask questions and get responses based on keyword matching
- **📊 Study Analytics**: Track your study sessions and progress with detailed statistics
- **🔐 Secure User Accounts**: Authentication and personalized dashboards for each user

### Technical Features
- Built with **Django 4.2** for robust backend functionality
- **NLTK** integration for natural language processing
- **Bootstrap 5** responsive design for mobile and desktop
- **SQLite** database (upgradeable to PostgreSQL for production)
- Static file handling with **WhiteNoise** for efficient deployment
- Ready for deployment on **Railway**, **Render**, or **PythonAnywhere**

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- **No external API keys required** - uses built-in NLP processing

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OlebogengRabotapi/studymind.git
   cd studymind
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```
   
   Activate it:
   - **Windows**: `venv\Scripts\activate`
   - **macOS/Linux**: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

7. **Run development server**
   ```bash
   python manage.py runserver
   ```
   
   Visit `http://localhost:8000` in your browser.

## 📖 Usage Guide

### Creating Study Materials
1. Log in to your account
2. Click "New Study Material"
3. Enter a title and paste your notes
4. Click "Create Material"

### Generating Summaries
1. Go to your study material
2. Click the "Generate Summary" button
3. The app will create a basic NLP summary with key points
4. Note: summary quality is basic and may be less polished than advanced AI systems

### Generating Practice Questions
1. In your study material
2. Click "Generate Questions"
3. Get 5 NLP-generated practice questions with difficulty levels
4. Click "Show Answer" to reveal the answer

### Keyword-Based Tutor
1. Navigate to the "AI Tutor" tab
2. Ask a question about your material
3. The app will try to match keywords from your question to the study text
4. View chat history anytime

> This project started with a plan to build its own full AI tutor, but that was not possible in this scope. Instead, it was improvised using local NLP techniques so the app can still summarize notes, generate practice questions, and answer basic keyword-based queries without external API calls.

### Tracking Progress
1. Go to "Statistics" in the navigation
2. View your study sessions, time spent, and AI-generated content
3. Monitor your learning journey

## 🤖 NLP Integration Details

### NLTK Usage
StudyMind uses NLTK (Natural Language Toolkit) for basic text processing:

- **Summaries**: Extractive summarization using sentence scoring based on word frequencies
- **Questions**: Keyword extraction and template-based question generation
- **Tutoring**: Keyword matching to find relevant content sections

### NLP Service Architecture
The `ai_service.py` module provides basic NLP operations:

```python
from studyapp.ai_service import ai_service

# Generate summary
result = ai_service.generate_summary(content, title)

# Generate questions
questions = ai_service.generate_practice_questions(content, title)

# Answer questions
response = ai_service.answer_question(user_question, content, title)
```

### Processing Notes
- Uses frequency analysis for text summarization
- Generates questions from extracted keywords
- Provides keyword-based responses for tutoring
- No external API calls required
- Summary generation is basic and may produce less polished output than advanced AI
- Practice question generation is stronger and works well for review
- **Note**: This is basic NLP processing, not advanced AI. Results are functional but not as sophisticated as LLM-based systems.

## 🗄️ Database Schema

### Models
- **User**: Django's built-in user model
- **UserProfile**: Extended user information and statistics
- **StudyMaterial**: User's study notes and documents
- **Summary**: AI-generated summaries
- **PracticeQuestion**: AI-generated practice questions
- **ChatMessage**: Chat history with AI tutor
- **StudySession**: Track user's study activities and time

## 🚀 Deployment

### Deploying to Railway

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Railway Account**: https://railway.app

3. **Connect GitHub Repository**
   - Create new project
   - Select "Deploy from GitHub repo"
   - Choose your StudyMind repository

4. **Set Environment Variables**
   In Railway dashboard, add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: Your Railway domain

5. **Deploy**
   Railway will automatically deploy when you push to main branch

### Deploying to Render

1. **Create Render Account**: https://render.com

2. **Create New Web Service**
   - Connect GitHub repository
   - Runtime: Python 3.11
   - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn studymind_project.wsgi`

3. **Add Environment Variables**
   - All variables from `.env.example`

4. **Deploy**
   - Click Deploy

### Deploying to PythonAnywhere

1. **Create PythonAnywhere Account**: https://www.pythonanywhere.com

2. **Upload Project**
   - Use git clone or manual upload

3. **Create Web App**
   - Choose Django 4.2
   - Point to your project

4. **Configure WSGI File**
   - Edit WSGI configuration to point to `studymind_project.wsgi`

5. **Set Environment Variables**
   - In web app settings, add environment variables

6. **Reload Web App**
   - Click Reload to apply changes

## 📚 Project Structure

```
studymind/
├── studymind_project/          # Django project settings
│   ├── settings.py             # Configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
├── studyapp/                   # Main application
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── forms.py                # Django forms
│   ├── ai_service.py           # AI integration
│   ├── admin.py                # Admin configuration
│   ├── urls.py                 # App URL routing
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── auth/               # Authentication templates
│   │   ├── material/           # Material templates
│   │   └── chat/               # Chat templates
│   └── static/                 # Static files
│       └── css/
│           └── style.css
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration
├── runtime.txt                 # Python version
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🔧 Technologies Used

- **Backend**: Django 4.2.11
- **Database**: SQLite (development), PostgreSQL (production)
- **NLP**: NLTK 3.8.1 for natural language processing
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Deployment**: Gunicorn, WhiteNoise
- **Environment**: Python-decouple, python-dotenv

## 📋 Dependencies

See `requirements.txt` for complete list. Key packages:
- Django 4.2.11
- nltk 3.8.1
- python-decouple 3.8
- gunicorn 21.2.0
- Pillow 10.0.0
- whitenoise 6.6.0

## 🛡️ Security Features

- Django's built-in CSRF protection
- Secure password hashing
- Environment-based configuration (secrets not in code)
- SQL injection prevention through ORM
- HTTPS enforcement in production

## 🐛 Troubleshooting

### Database Errors
- Run `python manage.py migrate` if you see migration errors
- Delete `db.sqlite3` and re-migrate for a fresh database in development

### Static Files Not Loading
- Run `python manage.py collectstatic` in production
- Check `STATIC_ROOT` configuration in settings.py

### Port Already in Use
- Change port: `python manage.py runserver 8001`
- Or kill the process using port 8000

## 📈 Future Enhancements

- [ ] Image recognition for handwritten notes
- [ ] Collaborative study groups
- [ ] Study schedule recommendations
- [ ] Export summaries as PDF
- [ ] Mobile application
- [ ] Google Drive integration
- [ ] Advanced spaced repetition system
- [ ] Real-time collaborative editing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Django
- Powered by NLTK for natural language processing
- UI Framework: Bootstrap 5
- Icons: Font Awesome

## 👨‍💻 Author

**[Olebogeng Rabotapi]**
- GitHub: [@OlebogengRabotapi](https://github.com/OlebogengRabotapi)
- LinkedIn: [www.linkedin.com/in/olebogeng-rabotapi]

## 💬 Support

For issues and questions:
1. Check existing issues on GitHub
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

---

**Happy Learning with StudyMind!** 🚀
