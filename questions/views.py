from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Question, ExpectedOutput


@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {'questions': questions})


@login_required
def question_detail(request, code):
    question = get_object_or_404(Question, code=code)
    test_cases = question.testcase_set.all()
    test_cases_with_outputs = []
    for test_case in test_cases:
        # Read test case input
        input_content = ''
        if test_case.file:
            try:
                input_content = test_case.file.open('r').read()
            except Exception:
                input_content = ''
        # Get expected output
        expected_output_obj = test_case.expectedoutput_set.first()
        output_content = ''
        if expected_output_obj and expected_output_obj.file:
            try:
                output_content = expected_output_obj.file.open('r').read()
            except Exception:
                output_content = ''
        test_cases_with_outputs.append({
            'input': input_content,
            'output': output_content,
        })
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'test_cases': test_cases,
        'test_cases_with_outputs': test_cases_with_outputs,
    }) 