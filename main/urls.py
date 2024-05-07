from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todo/', views.todos, name='todos'),
    path('login/', views.login_view, name='login'),
    path('todo/<int:pk>', views.todo_detail, name='todo_detail'),
]