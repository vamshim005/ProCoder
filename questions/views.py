from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from urllib.parse import unquote
import datetime

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
    code_text = unquote(request.GET.get('code_text', ''))
    language = request.GET.get('language', '')
    # Store start time in session if not already set for this question
    start_times = request.session.get('question_start_times', {})
    if code not in start_times:
        start_times[code] = datetime.datetime.now().isoformat()
        request.session['question_start_times'] = start_times
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'test_cases': test_cases,
        'test_cases_with_outputs': test_cases_with_outputs,
        'code_text': code_text,
        'language': language,
    }) 