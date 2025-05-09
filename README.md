# ProCoder - Online Judge Platform

ProCoder is a Django-based online judge platform that allows users to solve programming problems, submit solutions, and get real-time feedback on their code. The platform supports multiple programming languages and provides an interactive coding environment.

## Features

- **Multiple Language Support**: Write solutions in C, C++, Python 2, and Python 3
- **Real-time Code Execution**: Get instant feedback on your code submissions
- **Test Case Validation**: Solutions are tested against multiple test cases
- **User Authentication**: Secure login and registration system
- **Leaderboard**: Track your progress and compare with other users
- **Interactive Code Editor**: Built-in code editor with syntax highlighting
- **Email Verification**: Secure account creation with email verification

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, Bootstrap
- **Code Editor**: CodeMirror
- **Judging System**: Judge0 API
- **Email Service**: Gmail SMTP
- **Deployment**: PythonAnywhere
- **Environment Variables**: python-decouple

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ProCoder.git
cd ProCoder
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add the following variables:
```
DEBUG=True
SECRET_KEY=your_secret_key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
JUDGE0_API_URL=your_judge0_api_url
```

5. Run migrations:
```bash
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

1. Register a new account or login with existing credentials
2. Browse available programming problems
3. Select a problem and write your solution in the code editor
4. Choose your programming language
5. Submit your solution and get instant feedback
6. View test case results and debug your code if needed
7. Check the leaderboard to see your ranking

## Contributing

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Judge0](https://judge0.com/) for the code execution API
- [CodeMirror](https://codemirror.net/) for the code editor
- [Bootstrap](https://getbootstrap.com/) for the UI components

## Contact

For any questions or suggestions, please open an issue in the GitHub repository or contact the maintainers.

## Live Demo

Visit the live demo at: [ProCoder Demo](https://your-demo-url.com) 