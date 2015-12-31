# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import datetime
from django.contrib.auth.models import User
from inviMarket.models import Profile
from django.core import management

class RegisterTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="duplicate", email="duplicate@domain.com")
        self.client = Client()

    def test_valid_username(self):
        """Invalid email adress not allowed for username"""
        response = self.client.post(reverse('register'), {
            'username': '..test',
            'first_name': 'Name',
            'email': 'user@domain.com',
            'password1': 'test',
            'password2': 'test'
            })

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the form raises an error
        self.assertFormError(response, 'form', 'username', "This value may not "
            "start with, end with or contain two consecutive '.'")

    def test_duplicate(self):
        """Check duplicate username and email"""
        response = self.client.post(reverse('register'), {
            'username': 'duplicate',
            'first_name': 'Name',
            'email': 'duplicate@domain.com',
            'password1': 'test',
            'password2': 'test'
            })

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the form raises the errors
        self.assertFormError(response, 'form', 'username', "A user with that "
            "username already exists.")
        self.assertFormError(response, 'form', 'email', "A user with that "
            "email already exists.")

    def test_registered(self):
        """Successful registration"""
        response = self.client.post(reverse('register'), {
            'username': 'test',
            'first_name': 'Name',
            'email': 'user@domain.com',
            'password1': 'test',
            'password2': 'test',
            'terms': 'selected'
            })

        # Check that the response is a redirection and the new user exists
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='test').exists())
        # Check that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Account activation')

    def test_expired_activation_key(self):
        """Activation with expired key"""
        self.client.post('/register/', {
            'username': 'test',
            'first_name': 'Name',
            'email': 'user@domain.com',
            'password1': 'test',
            'password2': 'test',
            'terms': 'selected'
            })
        user = User.objects.get(username='test')
        user.profile.key_expires = (user.profile.key_expires -
                                    datetime.timedelta(4))
        user.profile.save()
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        response = self.client.get(reverse('confirm', kwargs={'uidb64': uidb64,
            'key': user.profile.activation_key}))
        user = User.objects.get(username='test')

        # Check that the response is 200 OK and user still inactive
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['confirm'])
        self.assertFalse(user.is_active)

    def test_clean_users(self):
        """Clean users with expired activation key"""
        self.client.post('/register/', {
            'username': 'test',
            'first_name': 'Name',
            'email': 'user@domain.com',
            'password1': 'test',
            'password2': 'test',
            'terms': 'selected'
            })
        user = User.objects.get(username='test')
        user.profile.key_expires = (user.profile.key_expires -
                                    datetime.timedelta(4))
        user.profile.save()
        management.call_command('clean_users', verbosity=0)

        # Check that the user has been deleted
        self.assertFalse(User.objects.filter(username='test').exists())

    def test_activation(self):
        """User activation"""
        self.client.post('/register/', {
            'username': 'test',
            'first_name': 'Name',
            'email': 'user@domain.com',
            'password1': 'test',
            'password2': 'test',
            'terms': 'selected'
            })
        user = User.objects.get(username='test')
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        response = self.client.get(reverse('confirm', kwargs={'uidb64': uidb64,
            'key': user.profile.activation_key}))
        user = User.objects.get(username='test')

        # Check that the response is 200 OK and user is active
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['confirm'])
        self.assertTrue(user.is_active)

class LoginTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username="alice",
            email="alice@domain.com", password="qwerty")
        Profile.objects.create(user=alice, lang='en')
        self.client = Client()

    def test_username_login(self):
        """Successful login with username"""
        response = self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        alice = User.objects.get(username="alice")

        # Check that the response is a redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['_auth_user_id'], str(alice.pk))

    def test_email_login(self):
        """Successful login with email"""
        response = self.client.post(reverse('login'),
            {'username': 'alice@domain.com', 'password': 'qwerty'})
        alice = User.objects.get(username="alice")

        # Check that the response is a redirection
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['_auth_user_id'], str(alice.pk))


class PartnerTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username="alice", password="qwerty")
        Profile.objects.create(user=alice)
        bob = User.objects.create_user(username="bob", password="qwerty")
        Profile.objects.create(user=bob)
        self.client = Client()

    def test_add_partner(self):
        """Partnership request"""
        bob = User.objects.get(username="bob")
        self.client.post(reverse('login'),
            {'username': 'alice', 'password': 'qwerty'})
        response = self.client.get(reverse('add_partner',
            kwargs={'partner_id': bob.id}))
        alice = User.objects.get(username="alice")

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check email notification has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Partnership request')
        # Check the receptor has received a notification.
        self.assertTrue(bob.notification_set.filter(sender=alice).exists())
        # Check the user is in the partners list.
        self.assertTrue(alice.profile.partners.filter(pk=bob.id).exists())

    def test_reject_partner(self):
        """Reject partnership request"""
        bob = User.objects.get(username="bob")
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'),
            {'username': 'alice', 'password': 'qwerty'})
        response = self.client.get(reverse('add_partner',
            kwargs={'partner_id': bob.id}))
        self.client.logout()
        self.client.post(reverse('login'),
            {'username': 'bob', 'password': 'qwerty'})
        response = self.client.get(reverse('del_partner',
            kwargs={'partner_id': alice.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the notification has been deleted.
        self.assertFalse(bob.notification_set.filter(sender=alice).exists())
        # Check the user is no longer in the partners list.
        self.assertFalse(alice.profile.partners.filter(pk=bob.id).exists())

    def test_accept_partner(self):
        """Accept partnership request"""
        bob = User.objects.get(username="bob")
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'),
            {'username': 'alice', 'password': 'qwerty'})
        response = self.client.get(reverse('add_partner',
            kwargs={'partner_id': bob.id}))
        self.client.logout()
        self.client.post(reverse('login'),
            {'username': 'bob', 'password': 'qwerty'})
        response = self.client.get(reverse('add_partner',
            kwargs={'partner_id': alice.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the notification has been deleted.
        self.assertFalse(bob.notification_set.filter(sender=alice).exists())
        # Check both users are in each other partners list.
        self.assertTrue(alice.profile.partners.filter(pk=bob.id).exists())
        self.assertTrue(bob.profile.partners.filter(pk=alice.id).exists())