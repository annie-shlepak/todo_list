from django.contrib import admin
from .models import Project, Task

# Register your models here.


class ProjectInlne(admin.StackedInline):
    model = Task
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fields = ['project_title']
    inlines = [ProjectInlne]


admin.site.register(Project, ProjectAdmin)
