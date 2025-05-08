from django.urls import path

from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list, name='list'),
    path('<str:code>/', views.question_detail, name='detail'),
] 