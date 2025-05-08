from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from questions.models import Question
from .forms import SubmissionForm
from .models import Submission
from .judge0_api import judge_with_judge0

# Create your views here.

@login_required
def submit_solution(request, code):
    question = get_object_or_404(Question, code=code)
    verdict = None
    details = None
    can_submit = False
    code_text = ''
    language = ''
    # Pre-fill code/language if coming from 'Try Again'
    if request.method == 'GET':
        code_text = request.GET.get('code_text', '')
        language = request.GET.get('language', '')
        form = SubmissionForm(initial={'code_text': code_text, 'language': language})
        return render(request, 'grader/submit_solution.html', {
            'form': form, 'question': question, 'verdict': verdict, 'details': details, 'can_submit': can_submit
        })
    if request.method == 'POST':
        if 'run' in request.POST:
            form = SubmissionForm(request.POST)
            if form.is_valid():
                code_text = form.cleaned_data['code_text']
                language = form.cleaned_data['language']
                # Gather all test case inputs for the question
                testcases = [tc.input_text for tc in question.test_cases.all()]
                results = judge_with_judge0(
                    source_code=code_text,
                    language=language,
                    testcases=testcases
                )
                # Determine overall verdict
                all_accepted = all(
                    res.get('status', {}).get('description', '') == 'Accepted'
                    for res in results
                )
                if all_accepted:
                    verdict = 'Accepted'
                    can_submit = True
                else:
                    verdict = next(
                        (res.get('status', {}).get('description', 'Unknown') for res in results if res.get('status', {}).get('description', '') != 'Accepted'),
                        'Unknown'
                    )
                details = [
                    {
                        'index': i+1,
                        'status': res.get('status', {}).get('description', 'Unknown'),
                        'output': res.get('stdout', ''),
                        'error': res.get('stderr', '')
                    }
                    for i, res in enumerate(results)
                ]
                # Store code and language in session for submit/try again
                request.session['pending_code'] = code_text
                request.session['pending_language'] = language
                request.session['pending_verdict'] = verdict
                request.session['pending_details'] = details
                request.session['pending_question'] = question.code
                return redirect('grader:run_results', code=question.code)
            # If form is not valid, re-render the question page with errors and user input
            return render(request, 'grader/submit_solution.html', {
                'form': form, 'question': question, 'verdict': None, 'details': None, 'can_submit': False
            })
        else:
            form = SubmissionForm()
    # Ensure form is always defined
    if 'form' not in locals():
        form = SubmissionForm()
    return render(request, 'grader/submit_solution.html', {
        'form': form, 'question': question, 'verdict': verdict, 'details': details, 'can_submit': can_submit
    })

@login_required
def run_results(request, code):
    question = get_object_or_404(Question, code=code)
    code_text = request.session.get('pending_code', '')
    language = request.session.get('pending_language', '')
    verdict = request.session.get('pending_verdict', None)
    details = request.session.get('pending_details', None)
    can_submit = verdict == 'Accepted'
    if request.method == 'POST':
        if 'submit' in request.POST and can_submit:
            submission = Submission(
                user=request.user,
                question=question,
                code_text=code_text,
                language=language,
                verdict='Accepted',
                details='All test cases passed.'
            )
            submission.save()
            # Clean up session
            for key in ['pending_code', 'pending_language', 'pending_verdict', 'pending_details', 'pending_question']:
                if key in request.session:
                    del request.session[key]
            return redirect('account:leaderboard')
        elif 'try_again' in request.POST:
            # Redirect back to question page with code/language pre-filled
            return redirect(f"/questions/{question.code}/?code_text={code_text}&language={language}")
    return render(request, 'grader/run_results.html', {
        'question': question,
        'code_text': code_text,
        'language': language,
        'verdict': verdict,
        'details': details,
        'can_submit': can_submit
    })

@login_required
def run_code(request, code):
    question = get_object_or_404(Question, code=code)
    if request.method == 'POST':
        code_text = request.POST.get('code_text', '')
        language = request.POST.get('language', '')
        # Gather all test case inputs for the question
        testcases = [tc.input_text for tc in question.test_cases.all()]
        results = judge_with_judge0(
            source_code=code_text,
            language=language,
            testcases=testcases
        )
        # Determine overall verdict
        all_accepted = all(
            res.get('status', {}).get('description', '') == 'Accepted'
            for res in results
        )
        if all_accepted:
            verdict = 'Accepted'
            can_submit = True
        else:
            verdict = next(
                (res.get('status', {}).get('description', 'Unknown') for res in results if res.get('status', {}).get('description', '') != 'Accepted'),
                'Unknown'
            )
            can_submit = False
        details = [
            {
                'index': i+1,
                'status': res.get('status', {}).get('description', 'Unknown'),
                'output': res.get('stdout', ''),
                'error': res.get('stderr', '')
            }
            for i, res in enumerate(results)
        ]
        # Store code and language in session for submit/try again
        request.session['pending_code'] = code_text
        request.session['pending_language'] = language
        request.session['pending_verdict'] = verdict
        request.session['pending_details'] = details
        request.session['pending_question'] = question.code
        return redirect('grader:run_results', code=question.code)
    return redirect('questions:detail', code=code)
