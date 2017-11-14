from datetime import date, timedelta

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf

from .models import Project, Task
from .forms import TaskForm, ProjectForm


@login_required(login_url='/auth/login/')
def get_today_task(request):
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_day=date.today(), task_status='NOTDONE').order_by('task_time'),
        'form': TaskForm,
        'form_p': ProjectForm,
        'username': auth.get_user(request).username
    }
    context.update(csrf(request))
    return render(request, 'today.html', context)


@login_required(login_url='/auth/login/')
def get_next_days_task(request):
    day = date.today()
    period = day + timedelta(days=7)
    period.strftime('%Y-%m-%d')
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_status='NOTDONE').extra(
            where=['task_day > %s', 'task_day <= %s'], params=[day, period]),
        'form': TaskForm,
        'form_p': ProjectForm,
        'username': auth.get_user(request).username
    }
    return render(request, 'next_days.html', context)


@login_required(login_url='/auth/login/')
def get_project_tasks(request, project_id=None):
    context = {
        'projects': Project.objects.all(),
        'project': Project.objects.get(id=project_id),
        'tasks': Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'),
        'form': TaskForm,
        'form_p': ProjectForm,
        'username': auth.get_user(request).username
    }
    return render(request, 'project_tasks.html', context)


@login_required(login_url='/auth/login/')
def get_archive(request):
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_status='DONE'),
        'form_p': ProjectForm,
        'username': auth.get_user(request).username
    }
    return render(request, 'archive.html', context)


@login_required(login_url='/auth/login/')
def add_today_task(request):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Added.')
        else:
            messages.error(request, 'Not Successfully Added.')
    return redirect('/')


@login_required(login_url='/auth/login/')
def add_project_task(request, project_id):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('/project_tasks/{}/'.format(project_id))


@login_required(login_url='/auth/login/')
def add_project(request):
    if request.POST:
        form_p = ProjectForm(request.POST)
        if form_p.is_valid():
            new_instance = form_p.save(commit=False)
            new_instance.save()
            return redirect('/')
    else:
        form_p = ProjectForm()
    context = {
        'projects': Project.objects.all(),
        "form_p": form_p,
        'username': auth.get_user(request).username,

    }
    return render(request, 'index.html', context)


@login_required(login_url='/auth/login/')
def edit_task(request, task_id):
    instance = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST or None, instance=instance)
    form_p = ProjectForm(request.POST or None)
    if form.is_valid():
        new_instance = form.save(commit=False)
        instance.save()
        new_instance.save()
        return HttpResponseRedirect('/today/')

    context = {
        "projects": Project.objects.all(),
        'username': auth.get_user(request).username,
        "form": form,
        "form_p": form_p,
        "instance": instance,
    }
    return render(request, 'edit_task.html', context)


@login_required(login_url='/auth/login/')
def edit_project(request, project_id):
    instance = get_object_or_404(Project, id=project_id)
    form_p = ProjectForm(request.POST or None, instance=instance)
    if form_p.is_valid():
        new_instance = form_p.save(commit=False)
        instance.save()
        new_instance.save()
        messages.success(request, 'Successfully Edited.')
        return HttpResponseRedirect('/')
    else:
        messages.error(request, 'Not Successfully Edited.')
    context = {
        "projects": Project.objects.all(),
        'username': auth.get_user(request).username,
        "form_p": form_p,
        "instance": instance,
    }
    return render(request, 'edit_project.html', context)


@login_required(login_url='/auth/login/')
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('/')


@login_required(login_url='/auth/login/')
def delete_project(request, project_id):
    Project.objects.get(id=project_id)
    if Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'):
        return redirect('/')
    else:
        Project.objects.get(id=project_id).delete()
        return redirect('/')


@login_required(login_url='/auth/login/')
def finish_task(request, task_id):
    Task.objects.select_related().filter(id=task_id).update(task_status='DONE')
    return redirect('/')


@login_required(login_url='/auth/login')
def view_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/auth/login')
def edit_profile(request):
    if request.method.POST:
        form = UserChangeForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = UserChangeForm(instance=request.u)
        context = {
            'form': form
        }
        return render(request, 'edit_profile.html', context)