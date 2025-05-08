from django.contrib.auth.mixins import LoginRequiredMixin as BaseLoginRequiredMixin
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme


class LoginRequiredMixin(BaseLoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'next'


class AnonymousRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super(AnonymousRequiredMixin, self).dispatch(request, *args, **kwargs)


class RequestFormAttachMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormAttachMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class NextUrlMixin(object):
    default_next = '/'

    def get_next_url(self):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        if url_has_allowed_host_and_scheme(redirect_path, self.request.get_host()):
            return redirect_path
        return self.default_next 