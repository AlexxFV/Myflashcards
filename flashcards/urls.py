from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import profile, CustomPasswordChangeView

app_name = 'flashcards'

urlpatterns = [
    # FlashCard Management
    path('', views.flashcard_list, name='flashcard_list'),  # List all flashcards
    path('create/', views.flashcard_create, name='flashcard_create'),  # Create a new flashcard
    path('flashcard/<int:pk>/delete/', views.flashcard_delete, name='flashcard_delete'),  # Delete a flashcard
    path('flashcard/<int:pk>/toggle-share/', views.flashcard_toggle_share, name='flashcard_toggle_share'),  # Toggle share
    path('flashcard/<int:pk>/toggle-hidden/', views.flashcard_toggle_hidden, name='flashcard_toggle_hidden'),  # Toggle hidden
    path('shared/', views.shared_flashcards, name='flashcard_shared_list'),  # List shared flashcards
    path('flashcard/<int:pk>/rate/', views.rate_flashcard, name='rate_flashcard'),  # Rate a flashcard
    path('rate/<int:pk>/', views.rate_flashcard, name='rate_flashcard'),  # Alternate route for rating
    path('add/<int:pk>/', views.add_shared_flashcard, name='add_shared_flashcard'),  # Add a shared flashcard

    # Collection Management
    path('collections/', views.collection_list, name='collection_list'),  # List all collections
    path('collections/create/', views.collection_create, name='collection_create'),  # Create a new collection
    path('collections/<int:pk>/delete/', views.collection_delete, name='collection_delete'),  # Delete a collection
    path('collections/<int:pk>/flashcards/', views.collection_flashcards, name='collection_flashcards'),  # View flashcards in a collection
    path('collections/shared/', views.shared_collections, name='shared_collections'), # View shared collection
    path('collections/shared/<int:pk>/', views.shared_collection_view, name='shared_collection_view'), # List shared collection
    path('add_collection/<int:pk>/', views.add_collection, name='add_collection'),# Add a shared collection


    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='flashcards/login.html'), name='login'),  # Login
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout
    path('register/', views.register, name='register'),  # Register a new user
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),  # Change password
    path('profile/', profile, name='profile'),  # View user profile

    # Study Mode
    path('study/', views.study_mode, name='study_mode'),  # List collections for study mode
    path('study/<int:collection_id>/', views.start_study, name='start_study'),  # Start study for a collection
    path('study/<int:collection_id>/question/<int:question_index>/', views.study_question, name='study_question'),  # View a study question
    path('study/<int:collection_id>/results/', views.study_results, name='study_results'),  # View study results

    # Telemetry
    path('telemetry/start/<int:pk>/', views.start_attempt, name='start_attempt'),  # Start telemetry for an attempt
    path('telemetry/end/<int:telemetry_id>/', views.end_attempt, name='end_attempt'),  # End telemetry for an attempt
    path('telemetry/report/', views.telemetry_report, name='telemetry_report'),  # View telemetry report

    # API Routes
    path('api/', include('flashcards.api_urls')),  # Include API routes
]
