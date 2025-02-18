# Core Django Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.db import models
from django.db.models import Q, Avg
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView  
from django.http import Http404

# Forms
from .forms import (
    FlashCardForm,
    CollectionForm,
    CommentForm,
    CustomUserCreationForm
)

# Models
from .models import (
    FlashCard,
    HiddenFlashCard,
    Collection,
    CollectionLimit,
    DailyLimit,
    Rating,
    Telemetry,
    Comment,
    User
)

# REST Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import (
    UserSerializer,
    FlashCardSerializer,
    CollectionSerializer,
    CollectionLimitSerializer
)

# Additional Imports
import json
from datetime import timedelta, datetime

# Collection Limit API View
class CollectionLimitView(APIView):
    """
    API View to manage collection limits for users.
    """
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        """
        Retrieve or create a collection limit for the authenticated user.
        """
        limit, _ = CollectionLimit.objects.get_or_create(user=request.user)
        serializer = CollectionLimitSerializer(limit)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        """
        Update the collection limit for the authenticated user.
        """
        limit, _ = CollectionLimit.objects.get_or_create(user=request.user)
        serializer = CollectionLimitSerializer(limit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# Collection Flashcards View
@login_required
def collection_flashcards(request, pk):
    """
    Display all flashcards associated with a specific collection.
    """
    collection = get_object_or_404(Collection, pk=pk, user=request.user)
    flashcards = collection.flashcards.all()
    return render(request, 'flashcards/collection_flashcards.html', {
        'flashcards': flashcards,
        'collection': collection
    })


# User Management API
class UserViewSet(ModelViewSet):
    """
    API ViewSet for user management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profile View
@login_required
def profile(request):
    """
    Display the user's profile.
    """
    return render(request, 'flashcards/profile.html', {'user': request.user})


# User Registration View
def register(request):
    """
    Register a new user.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in automatically
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'flashcards/register.html', {'form': form})

# Custom Login View
def custom_login(request):
    """
    Handle user login with form validation.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form validation failed.")
    else:
        form = AuthenticationForm()
    return render(request, 'flashcards/login.html', {'form': form})

# FlashCard API ViewSet
class FlashCardViewSet(ModelViewSet):
    """
    API ViewSet to handle CRUD operations for flashcards.
    """
    queryset = FlashCard.objects.all()
    serializer_class = FlashCardSerializer

@login_required
def flashcard_create(request):
    """
    Create a new flashcard for the user.
    """
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            today = now().date()
            daily_flashcard_count = FlashCard.objects.filter(created_by=request.user, created_at__date=today).count()
            daily_limit = DailyLimit.objects.first()


            # Check daily limit
            if daily_flashcard_count >= daily_limit.max_flashcards:
                messages.error(request, f"You've reached the daily limit of {daily_limit.max_flashcards} flashcards.")
                return redirect('flashcards:flashcard_create')


            # Save the flashcard
            flashcard = form.save(commit=False)
            flashcard.created_by = request.user
            flashcard.save()
            messages.success(request, "Flashcard created successfully!")
            return redirect('flashcards:flashcard_list')
    else:
        form = FlashCardForm()
    return render(request, 'flashcards/flashcard_create.html', {'form': form})




@login_required
def flashcard_delete(request, pk):
    """
    Delete a specific flashcard created by the user.
    """
    flashcard = get_object_or_404(FlashCard, pk=pk, created_by=request.user)
    if request.method == "POST":
        flashcard.delete()
        messages.success(request, "Flashcard deleted successfully!")
        return redirect('flashcards:flashcard_list')
    return render(request, 'flashcards/flashcard_delete.html', {'flashcard': flashcard})


@login_required
def flashcard_toggle_share(request, pk):
    """
    Toggle the shared status of a flashcard.
    """
    flashcard = get_object_or_404(FlashCard, pk=pk, created_by=request.user)
    if request.method == 'POST':
        flashcard.is_shared = not flashcard.is_shared
        flashcard.save()
        messages.success(request, f"Flashcard {'shared' if flashcard.is_shared else 'unshared'} successfully!")
        return redirect('flashcards:flashcard_list')
    return HttpResponseForbidden("You are not allowed to perform this action.")

@login_required
def flashcard_toggle_hidden(request, pk):
    """
    Toggle the hidden status of a flashcard for the user.
    """
    flashcard = get_object_or_404(FlashCard, pk=pk)
    hidden_entry, created = HiddenFlashCard.objects.get_or_create(user=request.user, flashcard=flashcard)
    if not created:
        hidden_entry.delete()
        return JsonResponse({'hidden': False})
    return JsonResponse({'hidden': True})

@login_required
def flashcard_list(request):
    """
    List all flashcards created by the user.
    """
    flashcards = FlashCard.objects.filter(created_by=request.user)
    hidden_ids = HiddenFlashCard.objects.filter(user=request.user).values_list('flashcard_id', flat=True)
    return render(request, 'flashcards/flashcard_list.html', {'flashcards': flashcards, 'hidden_ids': hidden_ids})
# Shared Flashcards Views
@login_required
def shared_flashcards(request):
    """
    Display all shared flashcards ordered by average rating.
    """
    flashcards = FlashCard.objects.filter(is_shared=True).annotate(
        avg_rating=models.Avg('ratings__rating')
    ).order_by('-avg_rating')
    return render(request, 'flashcards/shared_flashcards.html', {'flashcards': flashcards})


@login_required
def add_shared_flashcard(request, pk):
    """
    Copy a shared flashcard to the user's collection if it doesn't already exist.
    """
    flashcard = get_object_or_404(FlashCard, id=pk, is_shared=True)
    if not FlashCard.objects.filter(question=flashcard.question, created_by=request.user).exists():
        FlashCard.objects.create(
            question=flashcard.question,
            answer=flashcard.answer,
            difficulty=flashcard.difficulty,
            created_by=request.user,
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "exists"})


# FlashCard Rating API
@csrf_exempt
@login_required
def rate_flashcard(request, pk):
    """
    Rate a flashcard on a scale of 1 to 5.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating_value = int(data.get('rating', 0))
            if rating_value < 1 or rating_value > 5:
                return JsonResponse({'error': 'Invalid rating value'}, status=400)

            flashcard = FlashCard.objects.get(pk=pk)
            rating, _ = Rating.objects.get_or_create(user=request.user, flashcard=flashcard)
            rating.rating = rating_value
            rating.save()

            return JsonResponse({'success': True, 'new_average': flashcard.average_rating}, status=200)
        except FlashCard.DoesNotExist:
            return JsonResponse({'error': 'Flashcard not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Homepage View
@login_required
def index(request):
    """
    Display a random selection of shared flashcards on the homepage.
    """
    flashcards_shared_random = FlashCard.objects.filter(is_shared=True).order_by('?')[:3]
    return render(request, 'flashcards/index.html', {'flashcards_shared_random': flashcards_shared_random})

# Collection ViewSet for API
class CollectionViewSet(ModelViewSet):
    """
    API ViewSet to handle CRUD operations for collections.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

# Views for Collection Management
@login_required
def collection_create(request):
    """
    Create a new collection for the user.
    Validates the daily collection limit before saving.
    """
    if request.method == 'POST':
        form = CollectionForm(request.POST, user=request.user)
        if form.is_valid():
            today = now().date()
            daily_collection_count = Collection.objects.filter(user=request.user, created_at__date=today).count()
            daily_limit = DailyLimit.objects.first()

            # Check daily limit
            if daily_collection_count >= daily_limit.max_collections:
                messages.error(request, f"You've reached the daily limit of {daily_limit.max_collections} collections.")
                return redirect('flashcards:collection_create')

            # Save the collection
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, "Collection created successfully!")
            return redirect('flashcards:collection_list')
    else:
        form = CollectionForm(user=request.user)
    return render(request, 'flashcards/collection_create.html', {'form': form})

@login_required
def collection_list(request):
    """
    List all collections created by the logged-in user.
    """
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'flashcards/collection_list.html', {'collections': collections})

@login_required
def collection_delete(request, pk):
    """
    Delete a specific collection owned by the user.
    """
    collection = get_object_or_404(Collection, pk=pk, user=request.user)
    if request.method == "POST":
        collection.delete()
        messages.success(request, "Collection deleted successfully!")
    return redirect('flashcards:collection_list')

@login_required
def shared_collections(request):
    """
    Display all shared collections.
    """
    collections = Collection.objects.annotate(
        avg_rating=Avg('flashcards__ratings__rating')  
    ).order_by('-created_at') 
    return render(request, 'flashcards/shared_collections.html', {'collections': collections})

@login_required
def shared_collection_view(request, pk):
    """
    Display a shared collection and its flashcards, and handle comments.
    """
    collection = get_object_or_404(Collection, pk=pk)

    flashcards = collection.flashcards.all()

    comments = collection.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.collection = collection
            comment.user = request.user
            comment.save()
            return redirect('flashcards:shared_collection_view', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'flashcards/shared_collection_view.html', {
        'collection': collection,
        'flashcards': flashcards,
        'comments': comments,
        'form': form,
    })


@login_required
def collection_flashcards(request, pk):
    """
    Display all flashcards in a collection and handle comments.
    """
    collection = get_object_or_404(Collection, pk=pk)
    flashcards = collection.flashcards.all()
    comments = collection.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.collection = collection
            comment.user = request.user
            comment.save()
            return redirect('flashcards:collection_flashcards', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'flashcards/collection_flashcards.html', {
        'collection': collection,
        'flashcards': flashcards,
        'comments': comments,
        'form': form,
    })

@login_required
@csrf_exempt
def add_collection(request, pk):
    """
    Add a shared collection to the user's collections.
    """
    if request.method == 'POST':
        try:

            shared_collection = get_object_or_404(Collection, pk=pk)

 
            new_collection, created = Collection.objects.get_or_create(
                name=shared_collection.name,
                user=request.user,
            )

            if created:

                new_collection.flashcards.set(shared_collection.flashcards.all())
                new_collection.save()

                return JsonResponse({'status': 'success', 'message': 'Collection added successfully!'}, status=200)
            else:
                return JsonResponse({'status': 'exists', 'message': 'You already have this collection.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# Telemetry Views
@login_required
def start_attempt(request, flashcard_id):
    """
    Start an attempt for a specific flashcard.
    """
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    telemetry = Telemetry.objects.create(
        user=request.user,
        flashcard=flashcard,
        start_time=now()  # Record the start time
    )
    return JsonResponse({"telemetry_id": telemetry.id})


@login_required
def end_attempt(request, telemetry_id):
    """
    End an attempt for a specific telemetry entry.
    """
    telemetry = get_object_or_404(Telemetry, id=telemetry_id, user=request.user)
    telemetry.end_time = now()  # Record the end time
    telemetry.success = request.POST.get('success', 'false') == 'true'  # Determine success based on POST data
    telemetry.save()
    return JsonResponse({"status": "success"})


@login_required
def telemetry_report(request):
    """
    Display a telemetry report for the user.
    """
    telemetries = Telemetry.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'flashcards/telemetry_report.html', {'telemetries': telemetries})

 #  STUDY MODE
@login_required
def study_mode(request):
    """
    Renders a template showing all collections owned by the logged-in user.
    """
    collections = Collection.objects.filter(user=request.user)
    return render(request, 'flashcards/study_mode.html', {'collections': collections})


@login_required
def start_study(request, collection_id):
    """
    Clears previous telemetry data from the session and redirects the user
    to the first question of the selected collection.
    """
    request.session.pop('telemetry', None)

    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    return redirect('flashcards:study_question', collection_id=collection.id, question_index=0)


@login_required
def study_question(request, collection_id, question_index):
    """
    Validates the question index, retrieves the current question, and processes
    user answers. Redirects to the next question or study results upon completion.
    """
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)
    flashcards = list(collection.flashcards.all())
    total_questions = len(flashcards)

    if question_index < 0 or question_index >= total_questions:
        return redirect('flashcards:study_results', collection_id=collection_id)

    question = flashcards[question_index]

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '').strip()
        elapsed_time = float(request.POST.get('elapsed_time', '0'))  

        telemetry = request.session.get('telemetry', {})
        telemetry[str(question_index)] = {
            'question_id': question.id,
            'user_answer': user_answer,
            'correct': user_answer.lower() == question.answer.lower(),
            'time_taken': elapsed_time,
        }
        request.session['telemetry'] = telemetry

        if question_index + 1 < total_questions:
            return redirect('flashcards:study_question', collection_id=collection_id, question_index=question_index + 1)
        else:
            return redirect('flashcards:study_results', collection_id=collection_id)

    return render(request, 'flashcards/study_question.html', {
        'collection': collection,
        'question': question,
        'total_questions': total_questions,
        'question_index': question_index,
        'current_question_number': question_index + 1,
    })


@login_required
def study_results(request, collection_id):
    """
    Display the results of a completed study session.

    Calculates statistics such as accuracy, total time taken, and performance
    for each question. Renders the study results template with these details.
    """
    collection = get_object_or_404(Collection, id=collection_id, user=request.user)

    telemetry_data = request.session.get('telemetry', {})
    total_questions = len(telemetry_data)
    correct_answers = sum(1 for entry in telemetry_data.values() if entry['correct'])
    accuracy = round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0

    question_times = [
        {
            'question': get_object_or_404(FlashCard, id=entry['question_id']).question,
            'time': round(entry['time_taken'], 2),
            'success': entry['correct'],
        }
        for entry in telemetry_data.values()
    ]
    total_time = round(sum(entry['time_taken'] for entry in telemetry_data.values()), 2)

    return render(request, "flashcards/study_results.html", {
        "collection": collection,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "accuracy": accuracy,
        "total_time": total_time,
        "question_times": question_times,
    })

# Password Change
class CustomPasswordChangeView(PasswordChangeView):
    """
    Handles user password changes.
    """
    template_name = 'flashcards/change_password.html'
    success_url = reverse_lazy('flashcards:profile')
    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed!")
        return super().form_valid(form)
