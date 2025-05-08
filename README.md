# Code Warrior

An online judge platform with support for languages C, C++, and Python.

## Features

- Support for multiple programming languages (C, C++, Python)
- User authentication and registration
- Code submission and evaluation
- Real-time feedback on submissions
- Leaderboard system
- Email notifications

## Tools Used

- **Python** - Django web framework
- **Bootstrap** - Frontend styling
- **Amazon Web Services** - Cloud hosting
- **PythonAnywhere** - Python hosting platform
- **SendGrid** - Email service

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/yourusername/Code-Warrior.git
cd Code-Warrior
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file
```bash
cp .env-sample .env
```
Then edit the .env file with your actual credentials:
- Generate a new Django secret key
- Add your SendGrid credentials
- Configure other environment variables as needed

5. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to access the application.

## Project Structure

- `accounts/` - User authentication and management
- `grader/` - Code evaluation system
- `judge/` - Core application logic
- `questions/` - Problem statements and test cases
- `session/` - Session management
- `static_files/` - CSS, JavaScript, and other static assets
- `templates/` - HTML templates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 