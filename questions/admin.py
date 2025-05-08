from django.contrib import admin

from .models import Question, TestCase


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1
    fields = ('input_text', 'output_text')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'time_limit', 'timestamp')
    search_fields = ('code', 'title')
    list_filter = ('timestamp',)
    fields = ('code', 'title', 'description', 'time_limit')
    inlines = [TestCaseInline] 