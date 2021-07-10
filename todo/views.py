from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

# Create your views here.


def home(request):
    return render(request, 'todo/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'username and password did not match!'})
        else:
            login(request,user)
            return redirect('currenttodos')






def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                {'form': UserCreationForm(), 'error': 'Username already exists!'})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'Passwords did not match!'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')




def create(request):
    if request.method == 'GET':
        return render(request,'todo/create.html', {'form': TodoForm()})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit = False)
        newtodo.user = request.user
        newtodo.save()
        return render(request,'todo/currenttodos.html')

def currenttodos(request):
        todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
        return render(request, 'todo/currenttodos.html', {'todos': todos})


def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk=todo_pk)
    if request.method == 'GET':
        form = TodoForm(instance = todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form':form})
    else:
        form = TodoForm(request.POST, instance = todo)
        form.save()
        return redirect('currenttodos')