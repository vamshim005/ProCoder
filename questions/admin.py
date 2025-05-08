from django.contrib import admin

from .models import Question, TestCase, ExpectedOutput


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'time_limit', 'timestamp')
    search_fields = ('code', 'title')
    list_filter = ('timestamp',)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('question', 'filename', 'timestamp')
    search_fields = ('question__code', 'question__title', 'file')
    list_filter = ('timestamp',)


@admin.register(ExpectedOutput)
class ExpectedOutputAdmin(admin.ModelAdmin):
    list_display = ('question', 'test_case', 'filename', 'timestamp')
    search_fields = ('question__code', 'question__title', 'test_case__file', 'file')
    list_filter = ('timestamp',) 