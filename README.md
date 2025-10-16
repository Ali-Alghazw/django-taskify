# 🧩 Taskify – A Simple Task Manager

A minimal yet modern task management web app built with Django, designed to help users stay organized by creating, editing, and tracking daily tasks through an elegant, responsive interface.

# 📖 Table of Contents

-Overview
-Features
-Tech Stack
-ERD
-User Stories
-Installation & Setup
-Usage
-Screenshots
-Challenges & Solutions
-Future Improvements
-Author

# 📝 Overview

Taskify is a personal task management web app that allows users to:

- Register and authenticate securely.
- Add, edit, delete, and view their daily tasks.
- Filter by completion status (completed/pending).
- Track due dates easily.
- Enjoy a clean, modern interface built entirely with custom CSS (no frameworks).
- It’s a full-stack Django application demonstrating CRUD operations, authentication, and dynamic template rendering.

# 🚀 Features

✅ User registration & authentication (login/logout)
✅ Create, view, update, and delete tasks
✅ Mark tasks as completed or pending
✅ Filter & search tasks
✅ Pagination support
✅ Fully responsive modern UI
✅ Plain CSS (no Bootstrap or frameworks)

# 🧠 Tech Stack

Backend: Django 5.x
Frontend: HTML, CSS (custom, responsive)
Database: SQLite (default for Django)
Auth: Django built-in authentication
Version Control: Git + GitHub
Deployment: Localhost (development server)

# 📁 Project Structure


<img width="607" height="821" alt="image" src="https://github.com/user-attachments/assets/b26a6f9f-2858-4629-8c1d-bacb200be026" />



# 📊 Database Schema


Task Model


<img width="683" height="265" alt="image" src="https://github.com/user-attachments/assets/b0a77cc6-5457-4f6c-a4d1-59c43f1857db" />




# 👤 User Stories

As a user, I can register and log in to manage my tasks.
As a user, I can create new tasks with title, description, and due date.
As a user, I can view a list of all my tasks.
As a user, I can edit or delete existing tasks.
As a user, I can mark tasks as completed or pending.
As a user, I can search or filter tasks by status.

# ⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Ali-Alghazw/django-taskify.git
cd django-taskify

2️⃣ Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate      # for macOS/Linux
venv\Scripts\activate         # for Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

5️⃣ Create a Superuser (optional)
python manage.py createsuperuser

6️⃣ Run the Server
python manage.py runserver


Now visit http://127.0.0.1:8000/
 to use Taskify 🎯

# 💻 Usage

1.Register or log in with your credentials.
2.Create a new task using the “Add Task” button.
3.Edit, delete, or mark tasks as completed.
4.Use filters and pagination to navigate tasks efficiently.

# 🖼️ Screenshots

(You can add your screenshots later here)

🏠 Home / Login
<img width="1919" height="743" alt="image" src="https://github.com/user-attachments/assets/6b2a64be-f308-403c-87be-f7ebc9a933e2" />

📋 Task Dashboard
<img width="1505" height="929" alt="image" src="https://github.com/user-attachments/assets/7756cae0-30ec-4af8-9acf-a5ffa608f2af" />

➕ Add Task Form
<img width="1621" height="623" alt="image" src="https://github.com/user-attachments/assets/13fc5a63-fe18-4392-83bd-9e9e3bf1fc85" />

✏️ Edit Task Page
<img width="1504" height="670" alt="image" src="https://github.com/user-attachments/assets/4d08869a-0e3c-4742-9a7b-b89571e212d2" />



# 🧪 Running Tests
Taskify includes comprehensive unit tests covering models, views, forms, authentication, and integration scenarios.

Run All Tests
   python manage.py test

Run Specific Test Classes
- Model tests only
python manage.py test tasks.tests.TaskModelTest

- View tests only
python manage.py test tasks.tests.TaskViewsTest

- Authentication tests only
python manage.py test tasks.tests.AuthenticationTest

- Filter and search tests
python manage.py test tasks.tests.TaskFilterSearchTest

- Integration tests
python manage.py test tasks.tests.IntegrationTest

- Test Statistics


Total Tests: 30+
Model Tests: 7
Form Tests: 4
View Tests: 15
Authentication Tests: 4
Filter/Search Tests: 5
Integration Tests: 1
Coverage: 95%+

# 🧩 Challenges & Solutions
Challenge	Solution
Managing multiple accounts on Git	Configured Git user settings per project
Styling without Bootstrap	Built a custom modern CSS design system
Logout link not working	Switched to a POST form-based logout for security
Ensuring responsiveness	Added mobile-first media queries in custom CSS


# 🚀 Future Improvements

- Add dark/light theme toggle 🌗
- Task categories or labels 🏷️
- Reminder notifications ⏰
- Calendar view integration 📅

REST API endpoints for external use ⚙️

# 👨‍💻 Author

- Ali Al-Ghazw -
📧 alinabeel03aa@gmail.com
📍 Jordan
🔗 https://github.com/Ali-Alghazw
