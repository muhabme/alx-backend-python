from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# main router
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# nested router for messages under conversations
conversations_router = NestedDefaultRouter(
    parent_router=router,
    parent_prefix=r'conversations',
    lookup='conversation'
)
conversations_router.register(
    r'messages',
    MessageViewSet,
    basename='conversation-messages'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]