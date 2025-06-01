from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        # Handle nested route: filter by conversation_id if provided
        conversation_id = self.kwargs.get('conversation_conversation_id')
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        # Set the sender to the authenticated user
        # For nested routes, use conversation_id from URL
        conversation_id = self.kwargs.get('conversation_conversation_id')
        if conversation_id:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            serializer.save(sender=self.request.user, conversation=conversation)
        else:
            serializer.save(sender=self.request.user)