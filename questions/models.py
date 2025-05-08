import os

from django.db import models
from django.urls import reverse


def upload_question_image_location(instance, filename):
    file, ext = os.path.splitext(filename)
    location = 'questions/{code}{extension}'.format(code=instance.code, extension=ext)
    return location


class QuestionManager(models.Manager):
    def get_by_code(self, code):
        qs = self.get_queryset().filter(code=code)
        if qs.count() == 1:
            return qs.first()
        return None


class Question(models.Model):
    code = models.CharField(unique=True, max_length=10)
    title = models.CharField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    time_limit = models.IntegerField(default=1)
    sample_input = models.TextField(blank=True, help_text="Sample input for the problem")
    sample_output = models.TextField(blank=True, help_text="Sample output for the problem")
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('questions:detail', kwargs={'code': self.code})

    def get_submit_url(self):
        return reverse('grader:submit', kwargs={'code': self.code})


def upload_test_case_file_location(instance, filename):
    location = 'test_cases/{code}/inputs/'.format(code=instance.question.code)
    return location + filename


class TestCaseQuerySet(models.query.QuerySet):
    def get_by_question(self, question_code):
        return self.filter(question__code=question_code)


class TestCaseManager(models.Manager):
    def get_queryset(self):
        return TestCaseQuerySet(self.model, using=self._db)

    def get_by_question(self, question_code):
        return self.get_queryset().get_by_question(question_code)


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_cases')
    input_text = models.TextField(help_text="Input for this test case")
    output_text = models.TextField(help_text="Expected output for this test case")
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TestCaseManager()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.question.code} - TestCase {self.id}" 