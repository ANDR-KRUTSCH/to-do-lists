from django.core.management import BaseCommand
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings

User = get_user_model()

def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('email')

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)