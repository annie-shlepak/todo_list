from datetime import date, timedelta

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf

from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Project, Task
from .forms import TaskForm, ProjectForm


class TodayTasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'projects': Project.objects.all(),
            'tasks': Task.objects.filter(task_day=date.today(), task_status='NOTDONE').order_by('task_time'),
            'form': TaskForm,
            'form_p': ProjectForm,
            'username': auth.get_user(request).username
        }
        return render(request, 'today.html', context)


class NextDaysTasksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        period = date.today() + timedelta(days=7)
        period.strftime('%Y-%m-%d')
        context = {
            'projects': Project.objects.all(),
            'tasks': Task.objects.filter(task_status='NOTDONE').extra(
                where=['task_day > %s', 'task_day <= %s'], params=[date.today(), period]),
            'form': TaskForm,
            'form_p': ProjectForm,
            'username': auth.get_user(request).username
        }
        return render(request, 'next_days.html', context)


class ProjectTasksView(LoginRequiredMixin, View):
    def get(self, request, project_id, *args, **kwargs):
        context = {
            'projects': Project.objects.all(),
            'project': Project.objects.get(id=project_id),
            'tasks': Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'),
            'form': TaskForm,
            'form_p': ProjectForm,
            'username': auth.get_user(request).username
        }
        return render(request, 'project_tasks.html', context)


class ArchiveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwaqrgs):
        context = {
            'projects': Project.objects.all(),
            'tasks': Task.objects.filter(task_status='DONE'),
            'form_p': ProjectForm,
            'username': auth.get_user(request).username
        }
        return render(request, 'archive.html', context)


class AddTaskView(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    success_url = '/'


class AddProjectView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    success_url = '/'


@login_required(login_url='/auth/login/')
def edit_task(request, slug):
    instance = get_object_or_404(Task, slug=slug)
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


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    form_class = TaskForm
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('today-tasks')

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Task, slug=slug)
        return obj

    def get(self, request, *args, **kwargs):
        context = {
            "projects": Project.objects.all(),
            'username': auth.get_user(request).username,
        }
        return render(request, self.template_name, context)


@login_required(login_url='/auth/login/')
def delete_project(request, project_id):
    Project.objects.get(id=project_id)
    if Task.objects.filter(task_project_id=project_id, task_status='NOTDONE'):
        return redirect('/')
    else:
        Project.objects.get(id=project_id).delete()
        return redirect('/')


@login_required(login_url='/auth/login/')
def finish_task(request, slug):
    Task.objects.select_related().filter(slug=slug).update(task_status='DONE')
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
        form = UserChangeForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'edit_profile.html', context)
