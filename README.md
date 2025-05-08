# ProCoder

ProCoder is a modern online judge platform that allows users to solve programming problems in C, C++, Python, and Java. It features user authentication, a leaderboard, problem management, and secure code execution via the Judge0 API.

## Features
- User registration, login, and email verification
- Problem listing and detailed problem view
- Code submission via an in-browser editor (CodeMirror)
- Supports C, C++, Python 2, Python 3, and Java
- Secure code execution using the Judge0 API (no local Docker required)
- Leaderboard with scoring based on accepted solutions
- Django admin for problem and test case management
- Responsive UI with Bootstrap

## Tech Stack
- Python, Django
- Judge0 API (via RapidAPI)
- Bootstrap 5, CodeMirror
- PostgreSQL or SQLite (development)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/ProCoder.git
   cd ProCoder
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   - `SECRET_KEY`: Your Django secret key
   - `JUDGE0_API_KEY`: Your Judge0 RapidAPI key
   - (Optionally use a `.env` file with `python-decouple`)

5. **Run migrations and collect static files:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the app:**
   - Go to `http://127.0.0.1:8000/` in your browser
   - Log in, register, and start solving problems!

## Deployment
- ProCoder can be deployed to PythonAnywhere, Heroku, or any VPS/cloud server.
- For Judge0 API integration, no Docker is required on your server.
- See the deployment section in this README or ask for a step-by-step guide.

## License
MIT License

---

**ProCoder** — The modern, secure, and extensible online judge platform. 