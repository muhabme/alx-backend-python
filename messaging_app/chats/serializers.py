from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'full_name']
        read_only_fields = ['user_id', 'full_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at', 'sender']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        source='participants',
        required=True
    )
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at', 'updated_at', 'participant_count']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at', 'participants', 'messages']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_participant_ids(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("A conversation must have at least one participant.")
        for user_id in value:
            if not User.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError(f"User with ID {user_id} does not exist.")
        return value

    def create(self, validated_data):
        participant_ids = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        for user_id in participant_ids:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
        if self.context['request'].user.is_authenticated:
            conversation.participants.add(self.context['request'].user)
        return conversation