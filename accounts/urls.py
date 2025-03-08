from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('', include('django.contrib.auth.urls')),

    # Switch the default landing page to be a search page
    # path('', views.dashboard, name='dashboard')
]
