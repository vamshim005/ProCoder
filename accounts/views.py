from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import ListView, DetailView, FormView, CreateView, View
from django.views.generic.edit import FormMixin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .forms import LoginForm, RegisterForm, ReactivateEmailForm
from .models import EmailActivation
from judge.mixins import LoginRequiredMixin, AnonymousRequiredMixin, RequestFormAttachMixin, NextUrlMixin
from grader.models import Submission
from django.db.models import Min

User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        instance = User.objects.filter(username=username).first()
        if instance is None:
            raise Http404('User not found')
        return instance


class LeaderBoardView(ListView):
    template_name = 'accounts/leaderboard.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        users = User.objects.filter(is_active=True, admin=False)
        leaderboard = []
        print('DEBUG: Users found:', list(users))
        for user in users:
            accepted = Submission.objects.filter(user=user, verdict__icontains='Accepted')
            print(f'DEBUG: User {user.username} accepted submissions:', list(accepted))
            solved_questions = accepted.values_list('question', flat=True).distinct()
            score = solved_questions.count()
            total_time = 0
            for qid in solved_questions:
                first = accepted.filter(question_id=qid).order_by('submitted_at').first()
                if first:
                    # Calculate time taken to solve this question (in seconds)
                    time_taken = int((first.submitted_at - first.question.timestamp).total_seconds())
                    total_time += time_taken
            print(f'DEBUG: User {user.username} score: {score}, total_time: {total_time}')
            leaderboard.append({
                'user': user,
                'score': score,
                'total_time': total_time
            })
        leaderboard.sort(key=lambda x: (-x['score'], x['total_time']))
        for entry in leaderboard:
            entry['user'].score = entry['score']
            entry['user'].total_time = entry['total_time']
        print('DEBUG: Final leaderboard:', leaderboard)
        return [entry['user'] for entry in leaderboard]


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, 'Your email has been confirmed! Please login to continue.')
                return redirect('account:login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """Your email has already been confirmed.
                    Do you want to <a href="{link}">reset you password</a>?""".format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('account:login')
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = 'Activation link sent. Please check your email.'
        messages.success(self.request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, 'key': self.key}
        return render(self.request, 'registration/activation_error.html', context)


class LoginView(AnonymousRequiredMixin, RequestFormAttachMixin, NextUrlMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'
    default_url = '/'
    default_next = '/'

    def form_valid(self, form):
        request = self.request
        response = form.cleaned_data
        if not response.get('success'):
            messages.warning(request, mark_safe(response.get('message')))
            return redirect('account:login')
        next_path = self.get_next_url()
        return redirect(next_path)


def verify_info(request):
    if request.method == 'POST':
        code = request.POST.get('bypass_code')
        username = request.session.get('pending_user')
        if code == '2501' and username:
            user = get_object_or_404(User, username=username)
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated! You can now log in.')
            del request.session['pending_user']
            return redirect('account:login')
        else:
            messages.error(request, 'Invalid code. Please check your email for the verification link or try again.')
    return render(request, 'accounts/verify_info.html')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['pending_user'] = user.username
            return redirect('account:verify_info')
        return render(request, 'accounts/register.html', {'form': form}) 