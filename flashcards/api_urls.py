from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FlashCardViewSet, CollectionViewSet
from django.urls import path
from .views import CollectionLimitView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'flashcards', FlashCardViewSet, basename='flashcard')
router.register(r'collections', CollectionViewSet, basename='collection')


urlpatterns = [
    path('collections/', CollectionLimitView.as_view(), name='collection_limit'),
]


urlpatterns = router.urls
