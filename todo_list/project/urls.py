from django.conf.urls import url
from django.contrib import admin
from project import views
from .views import TodayTasksView, NextDaysTasksView, ProjectTasksView, ArchiveView, \
    AddTaskView, AddProjectView, DeleteTaskView


urlpatterns = [
    url(r'^today/$', TodayTasksView.as_view(), name='today-tasks'),
    url(r'^next_days/$', NextDaysTasksView.as_view(), name='next-days-tasks'),
    url(r'^project_tasks/(?P<project_id>\d+)/$', ProjectTasksView.as_view(), name="project-tasks"),
    url(r'^archive/$', ArchiveView, name="archive"),
    url(r'^add_task/$', AddTaskView.as_view(), name='add-today-task'),
    url(r'^add_project/$', AddProjectView.as_view(), name='add-project'),
    url(r'^add_task/(?P<project_id>\d+)/$', AddTaskView.as_view(), name='add-project-task'),
    url(r'^edit_task/(?P<slug>[\w-]+)/$', views.edit_task, name='edit-task'),
    url(r'^edit_project/(?P<project_id>\d+)$', views.edit_project, name='edit-project'),
    url(r'^delete_task/(?P<slug>[\w-]+)/$', DeleteTaskView.as_view(), name="delete-task"),
    url(r'^delete_project/(?P<project_id>\d+)/$', views.delete_project, name="delete-project"),
    url(r'^finish_task/(?P<slug>[\w-]+)/$', views.finish_task, name='finish-task'),
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit-profile'),
    url(r'^', TodayTasksView.as_view(), name='today-tasks'),
]
