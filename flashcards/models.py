from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

# Custom User Model
class User(AbstractUser):
    """
    Extends the default Django user model to include an admin flag.
    """
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# FlashCard Model
class FlashCard(models.Model):
    """
    Represents a flashcard with a question, answer and difficulty level.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES)
    is_shared = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='flashcards'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    @property
    def average_rating(self):
        """
        Calculates the average rating for the flashcard.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return None


# Collection Model
class Collection(models.Model):
    """
    Represents a collection of flashcards owned by a user.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcards = models.ManyToManyField(FlashCard, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.collection.name}"


# Daily Limit Model
class DailyLimit(models.Model):
    """
    Specifies daily limits for creating flashcards and collections.
    """
    max_flashcards = models.PositiveIntegerField(default=20)
    max_collections = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"Daily Limit: {self.max_flashcards} Flashcards, {self.max_collections} Collections"


# Hidden FlashCard Model
class HiddenFlashCard(models.Model):
    """
    Tracks flashcards hidden by a user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hidden_flashcards'
    )
    flashcard = models.ForeignKey(
        FlashCard,
        on_delete=models.CASCADE,
        related_name='hidden_by_users'
    )
    hidden_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'flashcard')

    def __str__(self):
        return f"{self.user.username} - Hidden: {self.flashcard.question}"


# Collection Limit Model
class CollectionLimit(models.Model):
    """
    Tracks the daily collection limit for a specific user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    daily_limit = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.user.username}'s Collection Limit: {self.daily_limit}"


# Rating Model
class Rating(models.Model):
    """
    Stores user ratings for flashcards.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'flashcard')

    def __str__(self):
        return f"{self.user.username} rated {self.flashcard.question} - {self.rating}"


# Telemetry Model
class Telemetry(models.Model):
    """
    Tracks study attempts for flashcards, including start and end times, and success status.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(FlashCard, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField()

    def __str__(self):
        return f"Telemetry for {self.flashcard.question} by {self.user.username}"
