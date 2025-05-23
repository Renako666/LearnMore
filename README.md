# Django Learning Platform

A modern online learning platform built with Django + Next.js full-stack technology stack, providing rich online learning features and excellent user experience.

## Technology Stack

### Backend
- Django 4.x - Python Web Framework
- Django REST Framework - RESTful API Support
- SQLite - Development Database
- Django Authentication - User Authentication System

### Frontend
- Next.js 14 - React Framework
- TypeScript - Type-safe JavaScript Superset
- Tailwind CSS - Utility-first CSS Framework
- Shadcn/ui - Modern UI Component Library

## Project Structure

```
django-learning-platform/
├── accounts/           # User Account Management App
├── courses/           # Course Management App
├── dashboard/         # Dashboard App
├── learning_platform/ # Django Project Configuration
├── app/              # Next.js App Directory
├── components/       # React Components
├── hooks/           # React Custom Hooks
├── lib/             # Utility Functions Library
├── public/          # Static Assets
├── styles/          # Style Files
└── templates/       # Django Templates
```

## Main Features

### 1. User System
- User Registration and Login
- Profile Management
- Role-based Access Control (Student/Teacher/Admin)

### 2. Course Management
- Course Creation and Editing
- Course Categories and Tags
- Course Content Management (Videos, Documents, Quizzes, etc.)
- Course Progress Tracking

### 3. Learning Features
- Online Video Playback
- Document Reading
- Online Quizzes
- Learning Progress Tracking
- Notes and Comments System

### 4. Dashboard
- Learning Statistics
- Progress Reports
- Grade Analysis
- Learning Recommendations

## Development Environment Setup

1. Clone Project
```bash
git clone [project-url]
cd django-learning-platform
```

2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database migration
python manage.py migrate

# Run development server
python manage.py runserver
```

3. Frontend Setup
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

## Project Features

1. **Modern Architecture**
   - Frontend-Backend Separation
   - RESTful API Interface
   - Type-safe TypeScript
   - Responsive UI Design

2. **User Experience**
   - Intuitive Navigation System
   - Responsive Design, Multi-device Support
   - Smooth Animation Effects
   - Clear Visual Hierarchy

3. **Performance Optimization**
   - Code Splitting
   - Static Resource Optimization
   - Database Query Optimization
   - Caching Strategy

4. **Security**
   - CSRF Protection
   - XSS Protection
   - SQL Injection Protection
   - Secure Authentication System

## Development Guidelines

1. **Code Style**
   - Follow PEP 8 (Python)
   - ESLint + Prettier (JavaScript/TypeScript)
   - Component-based Development
   - Comment Standards

2. **Git Workflow**
   - Main Branch: main
   - Development Branch: develop
   - Feature Branch: feature/*
   - Commit Message Standards

## Todo List

- [ ] Complete User Authentication System
- [ ] Implement Course Content Management System
- [ ] Add Online Quiz Feature
- [ ] Optimize Mobile Experience
- [ ] Add Data Analysis Features
- [ ] Implement Real-time Notification System

## Contributing Guidelines

Issues and Pull Requests are welcome to help improve the project. Before submitting a PR, please ensure:

1. Code follows project standards
2. Necessary tests are added
3. Related documentation is updated
4. Commit messages are clear and specific

## License

MIT License 