from unittest.mock import Mock, patch, call

from django.test import TestCase

from accounts.models import Token

class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self) -> None:
        response = self.client.post(path='/accounts/send_login_email', data={'email': 'andr.krutsch@gmail.com'})
        
        self.assertRedirects(response=response, expected_url='/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail: Mock) -> None:
        self.client.post(path='/accounts/send_login_email', data={'email': 'andr.krutsch@gmail.com'})

        self.assertEqual(mock_send_mail.called, True)

        args, kwargs = mock_send_mail.call_args
        
        self.assertEqual(kwargs.get('subject'), 'Your login link for Superlists')
        self.assertEqual(kwargs.get('from_email'), 'andr.krutsch@gmail.com')
        self.assertEqual(kwargs.get('recipient_list'), ['andr.krutsch@gmail.com'])

    def test_adds_success_message_with_mock(self) -> None:
        response = self.client.post(path='/accounts/send_login_email', data={'email': 'andr.krutsch@gmail.com'}, follow=True)

        message = list(response.context.get('messages'))[0]

        self.assertEqual(message.message, 'Check your email, we sent link, use this link to log in.')

    def test_creates_token_associate_with_email(self) -> None:
        self.client.post(path='/accounts/send_login_email', data={'email': 'andr.krutsch@gmail.com'})
        
        token = Token.objects.first()
        
        self.assertEqual(token.email, 'andr.krutsch@gmail.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_uid(self, mock_send_mail: Mock) -> None:
        self.client.post(path='/accounts/send_login_email', data={'email': 'andr.krutsch@gmail.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'

        args, kwargs = mock_send_mail.call_args
        message = kwargs.get('message')

        self.assertIn(expected_url, message)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    def test_redirects_to_home_page(self, mock_auth: Mock) -> None:
        response = self.client.get(path='/accounts/login?token=abcd123')
        
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth: Mock) -> None:
        self.client.get(path='/accounts/login?token=abcd123')
        
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='abcd123'))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth: Mock) -> None:
        response = self.client.get(path='/accounts/login?token=abcd123')
        
        self.assertEqual(mock_auth.login.call_args, call(request=response.wsgi_request, user=mock_auth.authenticate.return_value))

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth: Mock) -> None:
        mock_auth.authenticate.return_value = None
        
        self.client.get(path='/accounts/login?token=abcd123')
        
        self.assertEqual(mock_auth.login.called, False)