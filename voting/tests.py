from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import User, Poll, Option, Vote

class PollTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.poll = Poll.objects.create(
            title='Test Poll',
            description='Test Description',
            creator=self.user,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(days=1)
        )
        self.option = Option.objects.create(
            poll=self.poll,
            text='Test Option'
        )

    def test_poll_list_view(self):
        response = self.client.get(reverse('poll_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Poll')

    def test_poll_vote(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('poll_detail', args=[self.poll.id]),
            {'option': self.option.id}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Vote.objects.filter(
            user=self.user,
            poll=self.poll,
            option=self.option
        ).exists()) 