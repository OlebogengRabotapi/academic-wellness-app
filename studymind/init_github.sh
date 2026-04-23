#!/bin/bash
# GitHub Setup Script

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: StudyMind - AI-Powered Study Assistant

- Django 4.2 application with OpenAI integration
- AI-powered summaries, questions, and tutoring
- User authentication and study tracking
- Ready for deployment to Railway/Render/PythonAnywhere"

# Add GitHub remote (update with your GitHub username and repo name)
# git remote add origin https://github.com/YOUR_USERNAME/studymind.git

# Create main branch and push
# git branch -M main
# git push -u origin main

echo "✅ Git repository initialized!"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub (https://github.com/new)"
echo "2. Copy the repository URL"
echo "3. Run: git remote add origin <your-github-url>"
echo "4. Run: git push -u origin main"
echo ""
echo "Then you can deploy to Railway:"
echo "1. Go to https://railway.app"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select your StudyMind repository"
echo "4. Set environment variables:"
echo "   - OPENAI_API_KEY"
echo "   - SECRET_KEY"
echo "   - DEBUG=False"
echo "   - ALLOWED_HOSTS=your-railway-domain"
echo ""
echo "Happy coding! 🚀"
