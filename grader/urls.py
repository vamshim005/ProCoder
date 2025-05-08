from django.urls import path
from . import views

app_name = 'grader'

urlpatterns = [
    # Add your URL patterns here
    path('run/<str:code>/', views.run_code, name='run_code'),
    path('results/<str:code>/', views.run_results, name='run_results'),
    path('submit/<str:code>/', views.submit_solution, name='submit'),
] 