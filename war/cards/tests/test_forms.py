from unittest import TestCase
from django.core import mail
from django.core.exceptions import ValidationError
from ..forms import EmailUserCreationForm
from ..models import Player

__author__ = 'danielsiker'


class FormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FormTestCase, cls).setUpClass()

    def test_clean_username_exception(self):
        # Create a player so that this username we're testing is already taken
        Player.objects.create_user(username='test-user')

        # set up the form for testing
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        # use a context manager to watch for the validation error being raised
        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username_pass(self):
        # Create a unique player
        Player.objects.create_user(username='hi')

        # create a different user
        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'unique'}

        # clean that shit out
        form.clean_username()

    def test_register_sends_email(self):
        form = EmailUserCreationForm()
        form.cleaned_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': 'test-pw',
            'password2': 'test-pw',
        }
        form.save()
        # Check there is an email to send
        self.assertEqual(len(mail.outbox), 1)
        # Check the subject is what we expect
        self.assertEqual(mail.outbox[0].subject, 'Welcome!')

    @classmethod
    def tearDownClass(cls):
        super(FormTestCase, cls).tearDownClass()
