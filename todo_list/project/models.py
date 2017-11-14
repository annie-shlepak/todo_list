from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save

# from .utils import unique_slug_generator


# Create your models here.
class Project(models.Model):
    class Meta:
        db_table = "project"

    project_title = models.CharField(max_length=200)

    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now)

    slug = models.SlugField(null=True, blank=True)

    @property
    def title(self):
        return self.project_title   # obj.title

    def __str__(self):
        return self.project_title

# signal
# def project_pre_save(sender, instance, *args, **kwargs):
#     print('Saving..')
#     print(instance.timestamp)
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
# pre_save.connect(project_pre_save, sender=Project)


class Task(models.Model):
    class Meta:
        db_table = "task"

    STATUS = (
        ('DONE', 'Done Task'),
        ('NOTDONE', 'Not Done Task')
    )

    task_title = models.CharField(max_length=200)
    task_day = models.DateField()
    task_time = models.TimeField()
    task_status = models.CharField(max_length=7, choices=STATUS, default='NOTDONE')

    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now)

    task_project = models.ForeignKey(Project)

    def __str__(self):
        return self.task_title

    @property
    def title(self):
        return self.task_title  # obj.title
