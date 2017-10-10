from django.contrib import admin
from .models import Project, Task

# Register your models here.
class ProjectInlne(admin.StackedInline):
    model = Task
    extra = 1

class ProjectAdmin(admin.ModelAdmin):
    #fields we want to display
    fields = ['project_title', 'project_color']
    inlines = [ProjectInlne]

    #!!!!!
    #list_filter = ['task_deadline']

admin.site.register(Project, ProjectAdmin)
