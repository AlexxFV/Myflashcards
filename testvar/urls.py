from django.contrib import admin
from django.urls import path, include
from flashcards.views import index, custom_login, collection_list, collection_create
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', index, name='index'),

    # Authentication routes
    path('login/', custom_login, name='login'),  
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    

    # Flashcards app routes
    path('flashcards/', include('flashcards.urls', namespace='flashcards')), 

    # Collection management routes
    path('collections/', collection_list, name='collection_list'),  
    path('collections/create/', collection_create, name='collection_create'), 
        #schema de la API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Swagger-UI
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # API routes
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/', include('flashcards.api_urls')),  
    path('accounts/login/', auth_views.LoginView.as_view(template_name='flashcards/login.html'), name='account_login'),
]


