from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.models import Todo
from django.http import Http404


def index(request):
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)
        context = { 'todos': todos }
        return render(request, 'main/index.html', context=context)
    else:
        return render(request, 'main/index.html')


def todos(request):
    if request.method == 'GET':
        return render(request, 'main/todo.html')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        user = request.user
        todo = Todo(title=title, description=description, user=user)
        todo.save()
        messages.success(request, 'Todo created successfully!')
        return redirect('index')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.html')
    elif request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return redirect('index')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Create a new user if it doesn't exist
            user = User.objects.create_user(username=username, password=password)
            user.save()
            # Authenticate and login the new user
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

@login_required
def todo_detail(request, pk):
    if request.method == 'GET':
        try:
            todo = Todo.objects.get(id=pk)
            title = todo.title
            description = todo.description
            id = todo.id
            context = {'title': title, 'description': description, 'id': id}
            return render(request, 'main/todo_detail.html', context=context)
        except Todo.DoesNotExist:
            raise Http404("Todo does not exist")
    elif request.method == 'POST':
        try:
            todo = Todo.objects.get(id=pk)
            todo.delete()
            return redirect('index')
        except Todo.DoesNotExist:
            raise Http404("Todo does not exist")
        except:
            return redirect('todo_detail', pk=pk)

