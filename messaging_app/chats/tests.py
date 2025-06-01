from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Conversation, Message

class ChatsModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)
        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user,
            content='Test message'
        )

    def test_message_content(self):
        self.assertEqual(self.message.content, 'Test message')