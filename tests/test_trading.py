# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth.models import User
from inviMarket.models import Profile, Website, Offer, Request, Trade
from django.conf import settings
from django.core import management
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import datetime

class SearchTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username='alice', password='qwerty')
        bob = User.objects.create_user(username='bob', password='qwerty')
        Profile.objects.create(user=alice, lang='en')
        Profile.objects.create(user=bob, lang='en')
        forum = Website.objects.create(
            name='Forum',
            url='http://www.forum.com',
            webType='FO',
            category='GEN'
            )
        cloud = Website.objects.create(
            name='CloudService',
            url='http://www.cloud.com',
            webType='CS',
            category='COM'
            )
        tracker = Website.objects.create(
            name='Tracker',
            url='http://www.tracker.com',
            webType='TR',
            category='MMD',
            protected=True
            )
        Offer.objects.create(user=alice, website=forum, number=1, to_donate=0)
        Offer.objects.create(user=alice, website=cloud, number=2, to_donate=1)
        Request.objects.create(user=bob, website=forum)
        Request.objects.create(user=bob, website=cloud)
        Offer.objects.create(user=bob, website=tracker, number=2, to_donate=0)
        Request.objects.create(user=alice, website=tracker)
        self.client = Client()

    def test_default_matchup(self):
        """Default trading match up"""
        alice = User.objects.get(username='alice')
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        response = self.client.post(reverse('trading'), {'request-sites': [],
            'show': 'ALL', 'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is one result.
        self.assertEqual(len(response.context['users']), 1)
        # Check the correct user is in the results.
        self.assertTrue(alice in response.context['users'])

    def test_simple_search(self):
        """Filter trading search by sites"""
        forum = Website.objects.get(name='Forum')
        alice = User.objects.get(username='alice')
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        response = self.client.get(reverse('trading'), {
            'request-sites': [str(forum.id)], 'show': 'ALL', 'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is one result.
        self.assertEqual(len(response.context['users']), 1)
        # Check the correct user is in the results.
        self.assertTrue(alice in response.context['users'])

    def test_donation_search(self):
        """Show only donations"""
        alice = User.objects.get(username='alice')
        cloud = Website.objects.get(name='CloudService')
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        response = self.client.get(reverse('trading'), {
            'request-sites': [str(cloud.id)], 'show': 'DON', 'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is one result.
        self.assertEqual(len(response.context['users']), 1)
        # Check the correct user is in the results.
        self.assertTrue(alice in response.context['users'])

    def test_donation_unavailable(self):
        """No available donations"""
        forum = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        response = self.client.get(reverse('trading'), {
            'request-sites': [str(forum.id)], 'show': 'DON', 'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is no results.
        self.assertEqual(len(response.context['users']), 0)

    def test_protected_search(self):
        """Search invites to a protected site"""
        tracker = Website.objects.get(name='Tracker')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('trading'), {
            'request-sites': [str(tracker.id)], 'show': 'ALL',
            'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is no results.
        self.assertEqual(len(response.context['users']), 0)

    def test_partner_search(self):
        """Search invites to a protected site offered by a partner"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        tracker = Website.objects.get(name='Tracker')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('trading'), {
            'request-sites': [str(tracker.id)], 'show': 'ALL',
            'offer-sites': []})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that there is one result.
        self.assertEqual(len(response.context['users']), 1)
        # Check that the partner is in the results.
        self.assertTrue(bob in response.context['users'])

class ProposeTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username='alice', password='qwerty')
        bob = User.objects.create_user(username='bob', password='qwerty')
        Profile.objects.create(user=alice, lang='en')
        Profile.objects.create(user=bob, lang='en')
        forum = Website.objects.create(
            name='Forum',
            url='http://www.forum.com',
            webType='FO',
            category='GEN'
            )
        cloud = Website.objects.create(
            name='CloudService',
            url='http://www.cloud.com',
            webType='CS',
            category='COM'
            )
        tracker = Website.objects.create(
            name='Tracker',
            url='http://www.tracker.com',
            webType='TR',
            category='MMD',
            protected=True
            )
        Offer.objects.create(user=alice, website=forum, number=1, to_donate=0)
        Offer.objects.create(user=alice, website=cloud, number=2, to_donate=1)
        Request.objects.create(user=bob, website=forum)
        Request.objects.create(user=bob, website=cloud)
        Offer.objects.create(user=bob, website=tracker, number=2, to_donate=0)
        Request.objects.create(user=alice, website=tracker)
        self.client = Client()

    def test_get_form(self):
        """Check that the proposal form is generated correctly"""
        bob = User.objects.get(username='bob')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('propose',
            kwargs={'receptor_id': bob.id}),)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the protected site is not available.
        self.assertEqual(
            len(response.context['request_form'].fields['sites'].choices), 0)
        # Check that the other sites are presented in the form.
        self.assertEqual(
            len(response.context['offer_form'].fields['sites'].choices), 2)

    def test_partner_form(self):
        """Check that the proposal form is generated correctly"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('propose',
            kwargs={'receptor_id': bob.id}),)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the protected site is now available.
        self.assertEqual(
            len(response.context['request_form'].fields['sites'].choices), 1)

    def test_donation_request(self):
        """Request a unavailable donation"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        tracker = Website.objects.get(name='Tracker')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.post(reverse('propose',
            kwargs={'receptor_id': bob.id}),
            {'request-sites': [str(tracker.id)]})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the error message is correct.
        self.assertEqual(response.context['error'], "Donations not available "
            "for the selected request.")
        # Check that no trade was created.
        self.assertFalse(alice.proposed_trades.exists())

    def test_existing_trade(self):
        """Existing pending trade proposed by the user"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        Trade.objects.create(proposer=alice, receptor=bob)
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('propose',
            kwargs={'receptor_id': bob.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the error message has been shown.
        self.assertEqual(response.context['error'], "You have already made the "
            "user a trade proposal.")

    def test_max_trades(self):
        """The receptor has reached the maximum pending trade proposals"""
        bob = User.objects.get(username='bob')
        for i in range(0, settings.MAX_TRADES):
            user = User.objects.create_user(username='user'+str(i))
            Trade.objects.create(proposer=user, receptor=bob)
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        response = self.client.get(reverse('propose',
            kwargs={'receptor_id': bob.id}))

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the error message has been shown.
        self.assertEqual(response.context['error'], "The user have reached the "
            "maximum number of pending proposals.")

    def test_send_proposal(self):
        """Request a unavailable donation"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        tracker = Website.objects.get(name='Tracker')
        forum = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        response = self.client.post(reverse('propose',
            kwargs={'receptor_id': bob.id}), {
            'request-sites': [str(tracker.id)],
            'offer-sites': [str(forum.id)]
            })

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check that the email has been sent.
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Trade proposal')
        # Check the receptor has received a notification
        self.assertTrue(bob.notification_set.filter(sender=alice).exists())
        # Check the trade is correct.
        self.assertTrue(
            alice.proposed_trades.get(receptor=bob).requests.count(), 1)
        self.assertTrue(
            alice.proposed_trades.get(receptor=bob).offers.count(), 1)

    def test_reject_proposal(self):
        """Request a unavailable donation"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        tracker = Website.objects.get(name='Tracker')
        forum = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        self.client.post(reverse('propose', kwargs={'receptor_id': bob.id}), {
            'request-sites': [str(tracker.id)],
            'offer-sites': [str(forum.id)]
            })
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        trade = alice.proposed_trades.get(receptor=bob)
        response = self.client.post(reverse('trade',
            kwargs={'trade_id': trade.id}), {'Reject_proposal': 'Reject'})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check the trade and notification have been deleted.
        self.assertFalse(alice.proposed_trades.filter(receptor=bob).exists())
        self.assertFalse(bob.notification_set.filter(sender=alice).exists())

    def test_accept_proposal(self):
        """Request a unavailable donation"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        alice.profile.partners.add(bob)
        bob.profile.partners.add(alice)
        tracker = Website.objects.get(name='Tracker')
        forum = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('propose', kwargs={'receptor_id': bob.id}), {
            'request-sites': [str(tracker.id)],
            'offer-sites': [str(forum.id)]
            })
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
            'password': 'qwerty'})
        trade = alice.proposed_trades.get(receptor=bob)
        response = self.client.post(reverse('trade',
            kwargs={'trade_id': trade.id}), {'Accept_proposal': 'Reject'})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check that the email has been sent.
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Accepted proposal')
        # Check the proposer has received a notification
        self.assertTrue(alice.notification_set.filter(sender=bob).exists())
        self.assertFalse(bob.notification_set.filter(sender=alice).exists())
        # Check the trade is accepted.
        self.assertTrue(alice.proposed_trades.get(receptor=bob).accepted)
        self.assertTrue(alice.request_set.get(website=tracker).traded)
        self.assertEqual(bob.offer_set.get(website=tracker).number, 1)
        self.assertTrue(bob.request_set.get(website=forum).traded)
        self.assertEqual(alice.offer_set.get(website=forum).number, 0)

    def test_expired_trade(self):
        """Clean expired trades"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        forum = Website.objects.get(name='Forum')
        self.client.post(reverse('login'), {'username': 'alice',
            'password': 'qwerty'})
        self.client.post(reverse('propose', kwargs={'receptor_id': bob.id}),
            {'offer-sites': [str(forum.id)]} )
        date = timezone.now() - datetime.timedelta(settings.TRADE_EXPIRATION+1)
        alice.proposed_trades.filter(receptor=bob).update(date=date)
        management.call_command('clean_trades', verbosity=0)

        # Check that the trade has been deleted
        self.assertFalse (alice.proposed_trades.exists())
        self.assertFalse(bob.notification_set.filter(sender=alice).exists())

class ChainTestCase(TestCase):
    def setUp(self):
        alice = User.objects.create_user(username='alice', password='qwerty')
        bob = User.objects.create_user(username='bob', password='qwerty')
        Profile.objects.create(user=alice, lang='en')
        Profile.objects.create(user=bob, lang='en')
        refsite = Website.objects.create(
            name='Refsite',
            url='http://www.refsite.com',
            webType='PTC',
            category='RE'
            )
        Offer.objects.create(user=alice, website=refsite, number=0, to_donate=1,
            referral='http://www.refsite.com/u/alice')
        self.client = Client()

    def test_chain_creation(self):
        """Create a referral chain"""
        alice = User.objects.get(username='alice')
        refsite = Website.objects.get(name='Refsite')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        response = self.client.post(reverse('chain',
            kwargs={'site_id': refsite.id}), {'jumps': 2})

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check that the referral chain has been created.
        self.assertTrue(alice.chain_set.filter(website=refsite))
        self.assertEqual(alice.chain_set.get(website=refsite).jumps, 2)
        # Check that the first link is active and marked as last one
        self.assertTrue(alice.link_set.get(counter=2).active)
        self.assertTrue(alice.link_set.get(counter=2).last_link)

    def test_wrong_password(self):
        """Join chain with a wrong password"""
        alice = User.objects.get(username='alice')
        refsite = Website.objects.get(name='Refsite')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('chain',
            kwargs={'site_id': refsite.id}), {'jumps': 2, 'password': 'abc'})
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
          'password': 'qwerty'})
        chain = alice.chain_set.get(website=refsite)
        cidb64 = urlsafe_base64_encode(force_bytes(chain.id))
        response = self.client.post(reverse('join_chain',
            kwargs={'cidb64': cidb64, 'token': chain.url_hash}),
            {'password': 'cba'} )

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the received error is correct.
        self.assertEqual(response.context['error'], "Invalid password.")

    def test_join_chain(self):
        """Join chain with a wrong password"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        refsite = Website.objects.get(name='Refsite')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('chain',
            kwargs={'site_id': refsite.id}), {'jumps': 2, 'password': 'abc'})
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
          'password': 'qwerty'})
        chain = alice.chain_set.get(website=refsite)
        alice_link = alice.link_set.get(chain=chain)
        cidb64 = urlsafe_base64_encode(force_bytes(chain.id))
        response = self.client.post(reverse('join_chain',
            kwargs={'cidb64': cidb64, 'token': chain.url_hash}),
            {'password': 'abc'} )

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the response contains the referral link
        self.assertEqual(response.context['referral'],
            alice.offer_set.get(website=refsite).referral)
        # Check that the new link has been created correctly
        self.assertTrue(bob.link_set.filter(chain=chain).exists())
        self.assertEqual(bob.link_set.get(chain=chain).source_link,
            alice_link)
        self.assertFalse(bob.link_set.get(chain=chain).active)
        self.assertFalse(bob.link_set.get(chain=chain).last_link)

    def test_add_link(self):
        """Add link to the chain"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        refsite = Website.objects.get(name='Refsite')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('chain',
            kwargs={'site_id': refsite.id}), {'jumps': 2, 'password': 'abc'})
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
          'password': 'qwerty'})
        chain = alice.chain_set.get(website=refsite)
        cidb64 = urlsafe_base64_encode(force_bytes(chain.id))
        self.client.post(reverse('join_chain',
            kwargs={'cidb64': cidb64, 'token': chain.url_hash}),
            {'password': 'abc'} )
        response = self.client.post(reverse('offer',
            kwargs={'site_id': refsite.id}),
            {'referral': 'http://www.refsite.com/u/alice'})
        alice_link = alice.link_set.get(chain=chain)
        bob_link = bob.link_set.get(chain=chain)

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check that the new link has been added correctly to the chain
        self.assertEqual(alice_link.next_link, bob_link)
        self.assertTrue(alice_link.active)
        self.assertFalse(bob_link.active)
        self.assertEqual(alice_link.counter, 1)
        self.assertFalse(alice_link.last_link)
        self.assertTrue(bob_link.last_link)

    def test_link_jump(self):
        """Add link to the chain and jump to the next one"""
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        refsite = Website.objects.get(name='Refsite')
        self.client.post(reverse('login'), {'username': 'alice',
          'password': 'qwerty'})
        self.client.post(reverse('chain',
            kwargs={'site_id': refsite.id}), {'jumps': 1, 'password': 'abc'})
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'bob',
          'password': 'qwerty'})
        chain = alice.chain_set.get(website=refsite)
        cidb64 = urlsafe_base64_encode(force_bytes(chain.id))
        self.client.post(reverse('join_chain',
            kwargs={'cidb64': cidb64, 'token': chain.url_hash}),
            {'password': 'abc'} )
        response = self.client.post(reverse('offer',
            kwargs={'site_id': refsite.id}),
            {'referral': 'http://www.refsite.com/u/alice'})
        alice_link = alice.link_set.get(chain=chain)
        bob_link = bob.link_set.get(chain=chain)

        # Check that the response is a redirection.
        self.assertEqual(response.status_code, 302)
        # Check that the new link has been added correctly to the chain
        self.assertEqual(alice_link.next_link, bob_link)
        self.assertFalse(alice_link.active)
        self.assertTrue(bob_link.active)
        self.assertEqual(alice_link.counter, 0)
        self.assertEqual(bob_link.counter, 1)
        self.assertFalse(alice_link.last_link)
        self.assertTrue(bob_link.last_link)