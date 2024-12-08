from rest_framework import serializers
from .models import User, FlashCard, Collection, CollectionLimit


# Collection Limit Serializer
class CollectionLimitSerializer(serializers.ModelSerializer):
    """
    Serializer for managing user-specific collection limits.
    """
    class Meta:
        model = CollectionLimit
        fields = ['daily_limit']


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'admin']  


# FlashCard Serializer
class FlashCardSerializer(serializers.ModelSerializer):
    """
    Serializer for flashcard details.
    """
    class Meta:
        model = FlashCard
        fields = ['id', 'question', 'answer', 'difficulty', 'created_at']


# Collection Serializer
class CollectionSerializer(serializers.ModelSerializer):
    """
    Serializer for collections.
    """
    flashcards = FlashCardSerializer(many=True, read_only=True) 

    class Meta:
        model = Collection
        fields = ['id', 'name', 'user', 'flashcards', 'created_at']
