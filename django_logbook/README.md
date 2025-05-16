# Django Logbook System

A comprehensive logbook management system built with Django, featuring user authentication, log entry management, search functionality, and user preferences.

## Features

- User Authentication
  - Login/Register
  - Password Reset via Email
  - Profile Management
  - Account Settings

- Log Management
  - Create, Read, Update, Delete (CRUD) Operations
  - Date and Time Tracking
  - Tagging System
  - Search Functionality

- User Interface
  - Responsive Design
  - Dark/Light Theme Support
  - Multiple Language Support
  - Customizable Settings

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd django_logbook
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=3306
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Log in with your credentials or register a new account
3. Use the navigation menu to:
   - View and search logs
   - Create new log entries
   - Manage your profile
   - Adjust settings

## Project Structure

```
django_logbook/
├── logbook/
│   ├── static/
│   │   └── logbook/
│   │       ├── css/
│   │       ├── js/
│   │       └── img/
│   ├── templates/
│   │   └── logbook/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── config/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 