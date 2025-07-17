from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST
# Create your views here.
from .forms import TaskForm

def index(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TaskForm()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'form': form,
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request,task_id):
    try:
        task=Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context ={
        'task':task,
    }
    return render(request,'todo/detail.html',context)

def close (request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    task.delete()
    return redirect(index)

def update(request,task_id):
    try:
        task=Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method=='POST':
        task.title=request.POST['title']
        task.due_at=make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect('detail',task_id=task.pk)

    context ={
        'task':task,
    }
    return render(request,'todo/edit.html',context)

@require_POST
def toggle(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.completed = 'completed' in request.POST
    task.save()
    return redirect('index')
