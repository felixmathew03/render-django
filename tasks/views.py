from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, SignUpForm
from django.contrib.auth import login

def signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)  
        return redirect('task_list')
    return render(request, 'tasks/signup.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user = request.user)
    return render(request, 'tasks/task_list.html', {'tasks':tasks})

@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('task_list')
    return render(request, 'tasks/task_form.html', {'form':form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('task_list')
    return render(request, 'task/task_form.html',{'form':form})

@login_required
def task_delete(request,pk):
    task = get_object_or_404(Task,pk=pk, user=request.user)
    task.delete()
    return redirect('task_list')


