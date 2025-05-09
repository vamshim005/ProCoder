from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from urllib.parse import unquote_plus

from .models import Question


@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})


@login_required
def question_detail(request, code):
    question = get_object_or_404(Question, code=code)
    test_cases = question.test_cases.all()
    test_cases_with_outputs = []
    for test_case in test_cases:
        test_cases_with_outputs.append({
            'input': test_case.input_text,
            'output': test_case.output_text,
        })
    code_text = unquote_plus(request.GET.get('code_text', ''))
    language = request.GET.get('language', '')
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'test_cases': test_cases,
        'test_cases_with_outputs': test_cases_with_outputs,
        'code_text': code_text,
        'language': language,
    }) 