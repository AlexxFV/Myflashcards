from django.contrib import admin
from .models import FlashCard, Collection, DailyLimit


@admin.register(FlashCard)
class FlashCardAdmin(admin.ModelAdmin):
    """
    Admin interface for managing FlashCards.
    Includes filtering, search, and detailed list display.
    """
    list_display = ['question', 'created_by', 'difficulty', 'created_at']
    search_fields = ['question']  # Enable search by question
    list_filter = ['difficulty', 'created_at']  # Enable filtering by difficulty and creation date


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Collections.
    Includes filtering, search, and detailed list display.
    """
    list_display = ['name', 'user', 'created_at']
    search_fields = ['name', 'user__username']  # Enable search by collection name and username
    list_filter = ['created_at']  # Enable filtering by creation date


@admin.register(DailyLimit)
class DailyLimitAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Daily Limits.
    Allows inline editing and clickable fields for quick updates.
    """
    list_display = ['max_flashcards', 'max_collections']
    list_display_links = ['max_flashcards']  # Make 'max_flashcards' clickable to edit the record
    list_editable = ['max_collections']  # Enable inline editing for 'max_collections'
