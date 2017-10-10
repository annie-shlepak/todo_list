from datetime import datetime, date, time, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from .models import Project, Task
from .forms import TaskForm, ProjectForm
from django.contrib import auth, messages


def today(request):
    task_form = TaskForm
    project_form = ProjectForm
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_day=date.today(), task_status='NOTDONE').order_by('task_time'),
        'form': task_form,
        'form_p': project_form,
        'username': auth.get_user(request).username
    }
    context.update(csrf(request))
    return render(request, 'today.html', context)


def next_days(request):
    task_form = TaskForm
    project_form = ProjectForm
    day = date.today()
    period = day + timedelta(days=7)
    period.strftime('%Y-%m-%d')
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_status='NOTDONE').extra(
            select={'in_future': "task_day <= {}".format(period)}),
        'form': task_form,
        'form_p': project_form,
        'username': auth.get_user(request).username
    }
    return render(request, 'next_days.html', context)


def project_tasks(request, project_id=None):
    task_form = TaskForm
    project_form = ProjectForm
    context = {
        'projects': Project.objects.all(),
        'project': Project.objects.get(id=project_id),
        'tasks': Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'),
        'form': task_form,
        'form_p': project_form,
        'username': auth.get_user(request).username
    }
    return render(request, 'project_tasks.html', context)


def archive(request):
    project_form = ProjectForm
    context = {
        'projects': Project.objects.all(),
        'tasks': Task.objects.filter(task_status='DONE'),
        'form_p': project_form,
        'username': auth.get_user(request).username
    }
    return render(request, 'archive.html', context)


def addtask_today(request):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Added.')
        else:
            messages.error(request, 'Not Successfully Added.')
    return redirect('/')


def addtask_project(request, project_id):
    if request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            # task = form.save(commit=False)
            # task.task_project = Project.objects.get(id=project_id)
            form.save()
    return redirect('/project_tasks/{}/'.format(project_id))


def addproject(request):
    if request.POST:
        print('is posted')
        form_p = ProjectForm(request.POST)
        # form = TaskForm(request.POST)
        if form_p.is_valid():
            print('is valid')
            new_instance = form_p.save(commit=False)
            new_instance.save()
            # form_p.save_m2m()
            return redirect('/')
    else:
        form_p = ProjectForm()
        # form = TaskForm()
    context = {
        'projects': Project.objects.all(),
        "form_p": form_p,
        # 'form': form,
        'username': auth.get_user(request).username,

    }
    return render(request, 'index.html', context)


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


def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('/')


def delete_project(request, project_id):
    Project.objects.get(id=project_id)
    if Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'):
        # messages.info(request, 'You CAN NOT delete projects with unfinished tasks!')
        return redirect('/')
    else:
        Project.objects.get(id=project_id).delete()
        return redirect('/')


def finish_task(request, task_id):
    Task.objects.select_related().filter(id=task_id).update(task_status='DONE')
    return redirect('/')