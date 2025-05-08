from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone


class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            active_sessions = Session.objects.filter(
                expire_date__gt=timezone.now()
            ).exclude(session_key=current_session_key)

            for session in active_sessions:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(request.user.id):
                    session.delete()

        response = self.get_response(request)
        return response 