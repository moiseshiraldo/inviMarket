# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from inviMarket.models import Profile, Website, Offer

class SearchTestCase(TestCase):
    def setUp(self):
        Website.objects.create(name='Forum', url='http://www.forum.com',
            webType='FO', category='GEN')
        Website.objects.create(name='Tracker', url='http://www.tracker.com',
            webType='TR', category='MMD')
        self.client = Client()

    def test_filter_search(self):
        """Filter search results"""
        response = self.client.get(reverse('sites'), {
            'types': ['FO', 'TR'],
            'categories': ['GEN'],
            'order': 'PO'
            })
        site = Website.objects.get(name='Forum')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the the search result is correct
        self.assertTrue(site in response.context['sites'])

    def test_query_search(self):
        """Simple query search"""
        response = self.client.get(reverse('sites'), {'q': 'Tracker'})
        site = Website.objects.get(name='Tracker')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check there is only one result
        self.assertEqual(len(response.context['sites']), 1)
        # Check the the search result is correct
        self.assertTrue(site in response.context['sites'])

    def test_long_query(self):
        """Too long query search"""
        query = "abcdefghijklmnopqrstuvwxyz"
        response = self.client.get(reverse('sites'), {'q': query})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the warning message is OK
        self.assertEqual(response.context['message'], "The query is too long:")

    def test_no_results(self):
        """No results search"""
        response= self.client.get(reverse('sites'), {
            'q': 'Tracker',
            'categories': ['GEN'],
            'types': [],
            'order': 'PO'
            })

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check there is no results
        self.assertEqual(len(response.context['sites']), 0)

class OfferTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username='alice', password='qwerty')
        Profile.objects.create(user=alice, lang='en')
        Website.objects.create(name='Forum', url='http://www.forum.com',
            webType='FO', category='MMD')
        Website.objects.create(name='Referral', url='http://www.referral.com',
            refvalidator="http://www.referral.com/user/\d+",
            webType='FO', category='RE')
        self.client = Client()

    def test_offer(self):
        """Test a simple offer"""
        site = Website.objects.get(name='Forum')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}), {'number': 2, 'to_donate': 1})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the offer was stored
        self.assertTrue(alice.offer_set.filter(website__name='Forum').exists())
        self.assertEqual(alice.offer_set.get(website__name='Forum').number, 2)

    def test_error(self):
        """Offer more donations than the total number"""
        site = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}), {'number': 1, 'to_donate': 2})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the offer was stored
        self.assertEqual(
            response.context['offer_form'].errors['to_donate'][0],
            "The number of invites to donate can't be greater than the total "
            "offered number.")

    def test_delete(self):
        """Test offer deletion"""
        site = Website.objects.get(name='Forum')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('offer', kwargs={'site_id': site.id}),
          {'number': 2, 'to_donate': 1})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}), {'number': 0, 'to_donate': 0})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the offer was deleted
        self.assertFalse(alice.offer_set.filter(website__name='Forum').exists())

    def test_referral(self):
        """Test a referral link offer"""
        site = Website.objects.get(name='Referral')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}),
            {'number': 0, 'to_donate': 1,
            'referral': "http://www.referral.com/user/1234"})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the offer was stored
        self.assertTrue(alice.offer_set.filter(
            website__name='Referral').exists())

    def test_invalid_link(self):
        """Test a invalid referral link offer"""
        site = Website.objects.get(name='Referral')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}),
            {'number': 0, 'to_donate': 1,
            'referral': "http://www.referral.com/abcd"})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 200)
        # Check the offer was stored
        self.assertEqual(response.context['error'], "The referral link is not "
            "valid. Check it and try again.")

    def test_delete_link(self):
        """Test referral link deletion"""
        site = Website.objects.get(name='Referral')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('offer', kwargs={'site_id': site.id}),
          {'number': 0, 'to_donate': 1,
          'referral': "http://www.referral.com/user/1234"})
        response = self.client.post(reverse('offer',
            kwargs={'site_id': site.id}),
            {'number': 0, 'to_donate': 1, 'referral': ""})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the offer was deleted
        self.assertFalse(alice.offer_set.filter(
            website__name='Referral').exists())

    def test_create_chain(self):
        """Test referral chain creation"""
        site = Website.objects.get(name='Referral')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        self.client.post(reverse('offer', kwargs={'site_id': site.id}),
            {'number': 0, 'to_donate': 1,
            'referral': "http://www.referral.com/user/1234"})
        response = self.client.post(reverse('chain',
            kwargs={'site_id': site.id}), {'jumps': 2, 'password1': 'qwerty',
            'password2': 'qwerty'})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the chain and primary link have been created
        self.assertTrue(alice.chain_set.filter(
            website__name='Referral').exists())
        self.assertTrue(alice.link_set.filter(counter=2).exists())

class RequestTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username='alice', password='qwerty')
        bob = User.objects.create_user(username='bob')
        Profile.objects.create(user=alice, lang='en')
        Website.objects.create(name='Forum', url='http://www.forum.com',
            webType='FO', category='MMD')
        site = Website.objects.create(name='Referral',
            url='http://www.referral.com', webType='FO', category='RE')
        Offer.objects.create(user=alice, website=site, to_donate=1,
            referral="http://www.referral.com/alice", weight=40)
        Offer.objects.create(user=bob, website=site, to_donate=1,
            referral="http://www.referral.com/bob", weight=20)
        self.client = Client()

    def test_request(self):
        """Test a simple request"""
        site = Website.objects.get(name='Forum')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        response = self.client.get(reverse('request',
            kwargs={'site_id': site.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the request was stored
        self.assertTrue(alice.request_set.filter(website__name='Forum').exists())

    def test_delete(self):
        """Test request deletion"""
        site = Website.objects.get(name='Forum')
        alice = User.objects.get(username="alice")
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.get(reverse('request', kwargs={'site_id': site.id}))
        response = self.client.get(reverse('del_request',
            kwargs={'site_id': site.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check the request was deleted
        self.assertFalse(alice.request_set.filter(
            website__name='Forum').exists())

    def test_getreflink(self):
        """Get referral link several times and check probabilities"""
        site = Website.objects.get(name='Referral')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        n_bob = n_alice = 0
        for i in range(100):
            response = self.client.get(reverse('request',
                kwargs={'site_id': site.id}))
            if response.context['offer'].user.username == 'bob':
                n_bob += 1
            else:
                n_alice += 1
        p_bob = n_bob/100.
        p_alice = n_alice/100.

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Print results
        print( ("Alice's link probability %f" % p_alice) )
        print( ("Bob's link probability %f" % p_bob) )