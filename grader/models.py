from django.db import models
from django.conf import settings
from questions.models import Question

# Create your models here.

LANGUAGE_CHOICES = [
    ('c', 'C'),
    ('cpp', 'C++'),
    ('python2', 'Python 2'),
    ('python3', 'Python 3'),
    ('java', 'Java'),
]

class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code_file = models.FileField(upload_to='submissions/')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verdict = models.CharField(max_length=20, blank=True)  # e.g., Accepted, Wrong Answer, Time Limit Exceeded
    details = models.TextField(blank=True)  # Store error messages or test case results
    code_text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user} - {self.question.code} - {self.language} - {self.submitted_at}'
