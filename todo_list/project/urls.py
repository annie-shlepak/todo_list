from django.conf.urls import url
from django.contrib import admin
from project import views


urlpatterns = [
    url(r'^today/$', views.today, name='today'),
    url(r'^next_days/$', views.next_days, name='next_days'),
    url(r'^project_tasks/(?P<project_id>\d+)/$', views.project_tasks, name="project_tasks"),
    url(r'^archive/$', views.archive, name="archive"),
    url(r'^addtask/$', views.addtask_today, name='addtask_today'),
    url(r'^addproject/$', views.addproject, name='addproject'),
    url(r'^addtask/(?P<project_id>\d+)/$', views.addtask_project, name='addtask_project'),
    url(r'^edit_task/(?P<task_id>\d+)$', views.edit_task, name='edit_task'),
    url(r'^edit_project/(?P<project_id>\d+)$', views.edit_project, name='edit_project'),
    url(r'^delete_task/(?P<task_id>\d+)/$', views.delete_task, name="delete_task"),
    url(r'^delete_project/(?P<project_id>\d+)/$', views.delete_project, name="delete_project"),
    url(r'^finish_task/(?P<task_id>\d+)/$', views.finish_task, name='finish_task'),
    url(r'^', views.today, name='today'),

]
