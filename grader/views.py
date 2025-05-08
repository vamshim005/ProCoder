from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from questions.models import Question
from .forms import SubmissionForm
from .models import Submission
from .judge0_api import judge_with_judge0
from questions.models import ExpectedOutput

# Create your views here.

@login_required
def submit_solution(request, code):
    question = get_object_or_404(Question, code=code)
    verdict = None
    details = None
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.question = question
            submission.save()
            # Gather all test case inputs for the question
            testcases = [tc.file.open('r').read() for tc in question.testcase_set.all()]
            # Call the Judge0 API
            results = judge_with_judge0(
                source_code=submission.code_text,
                language=submission.language,
                testcases=testcases
            )
            # Determine overall verdict
            all_accepted = all(
                res.get('status', {}).get('description', '') == 'Accepted'
                for res in results
            )
            if all_accepted:
                verdict = 'Accepted'
            else:
                verdict = next(
                    (res.get('status', {}).get('description', 'Unknown') for res in results if res.get('status', {}).get('description', '') != 'Accepted'),
                    'Unknown'
                )
            details = '\n'.join([
                f"Test case {i+1}: {res.get('status', {}).get('description', 'Unknown')}\nOutput: {res.get('stdout', '')}\nError: {res.get('stderr', '')}"
                for i, res in enumerate(results)
            ])
            submission.verdict = verdict
            submission.details = details
            submission.save()
            return render(request, 'grader/submit_solution.html', {'form': form, 'question': question, 'verdict': verdict, 'details': details})
    else:
        form = SubmissionForm()
    return render(request, 'grader/submit_solution.html', {'form': form, 'question': question, 'verdict': verdict, 'details': details})
