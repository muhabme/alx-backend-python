from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', email='sender@example.com', password='testpass')
        self.receiver = User.objects.create_user(username='receiver', email='receiver@example.com', password='testpass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello")
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)

    def test_notification_not_created_on_message_update(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Initial message')
        message.content = 'Updated message'
        message.save()
        self.assertEqual(Notification.objects.count(), 1)

    def test_multiple_notifications(self):
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="Message 1")
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="Message 2")
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 2)