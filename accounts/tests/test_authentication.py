from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Token
from accounts.authentication import PasswordlessAuthenticationBackend

User = get_user_model()

class AuthenticateTest(TestCase):
    
    def test_returns_None_if_no_such_token(self) -> None:
        result = PasswordlessAuthenticationBackend().authenticate(uid='no-such-token')
        
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self) -> None:
        email = 'andr.krutsch@gmail.com'
        
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(uid=token.uid)
        new_user = User.objects.get(email=email)
        
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self) -> None:
        email = 'andr.krutsch@gmail.com'
        
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(uid=token.uid)
        
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self) -> None:
        User.objects.create(email='another@gmail.com')
        desired_user = User.objects.create(email='edith@gmail.com')
        found_user = PasswordlessAuthenticationBackend().get_user(email='edith@gmail.com')
        
        self.assertEqual(desired_user, found_user)

    def test_returns_None_if_no_user_with_that_email(self) -> None:
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user(email='edith@gmail.com'))