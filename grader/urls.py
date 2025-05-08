from django.urls import path
from . import views

app_name = 'grader'

urlpatterns = [
    # Add your URL patterns here
    path('submit/<str:code>/', views.submit_solution, name='submit'),
] 