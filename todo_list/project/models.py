from datetime import datetime

from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator

# Create your models here.
class Project(models.Model):
    class Meta:
        db_table = "project"

    COLORS = (
        ('R', 'Red'),
        ('B', 'Blue'),
        ('G', 'Green'),
        ('Y', 'Yellow')
    )
    project_title = models.CharField(max_length=200)

    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now)

    slug = models.SlugField(null=True, blank=True)
    # project_color = models.CharField(max_length=1, choices=COLORS)

    @property
    def title(self):
        return self.project_title   # obj.title

    def __str__(self):
        return self.project_title

# signal
def project_pre_save(sender, instance, *args, **kwargs):
    print('Saving..')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(project_pre_save, sender=Project)


class Task(models.Model):
    class Meta:
        db_table = "task"

    # PRIORITY = (
    #     ('H', 'High'),
    #     ('M', 'Medium'),
    #     ('L', 'Low')
    # )

    STATUS = (
        ('DONE', 'Done Task'),
        ('NOTDONE', 'Not Done Task')
    )

    task_title = models.CharField(max_length=200)
    # task_priority = models.CharField(max_length=1, choices=PRIORITY)
    task_day = models.DateField()
    task_time = models.TimeField()
    task_status = models.CharField(max_length=7, choices=STATUS, default='NOTDONE')

    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now)

    slug = models.SlugField(null=True, blank=True)

    task_project = models.ForeignKey(Project)

    def __str__(self):
        return self.task_title

    @property
    def title(self):
        return self.task_title  # obj.title

# signal
def task_pre_save(sender, instance, *args, **kwargs):
    print('Saving..')
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(task_pre_save, sender=Task)
