from django.conf.urls import url
from django.contrib import admin
from project import views


urlpatterns = [
    url(r'^today/$', views.get_today_task, name='get_today_task'),
    url(r'^next_days/$', views.get_next_days_task, name='get_next_days_task'),
    url(r'^project_tasks/(?P<project_id>\d+)/$', views.get_project_tasks, name="get_project_tasks"),
    url(r'^archive/$', views.get_archive, name="get_archive"),
    url(r'^add_task/$', views.add_today_task, name='add_today_task'),
    url(r'^add_project/$', views.add_project, name='add_project'),
    url(r'^add_task/(?P<project_id>\d+)/$', views.add_project_task, name='add_project_task'),
    url(r'^edit_task/(?P<slug>[\w-]+)/$', views.edit_task, name='edit_task'),
    url(r'^edit_project/(?P<project_id>\d+)$', views.edit_project, name='edit_project'),
    url(r'^delete_task/(?P<slug>[\w-]+)/$', views.delete_task, name="delete_task"),
    url(r'^delete_project/(?P<project_id>\d+)/$', views.delete_project, name="delete_project"),
    url(r'^finish_task/(?P<slug>[\w-]+)/$', views.finish_task, name='finish_task'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^', views.get_today_task, name='get_today_task'),
]
