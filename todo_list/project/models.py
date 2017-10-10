from django.db import models
from datetime import date
from django.utils import timezone


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
    project_color = models.CharField(max_length=1, choices=COLORS)

    def __str__(self):
        return self.project_title


class Task(models.Model):
    class Meta:
        db_table = "task"

    PRIORITY = (
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low')
    )
    STATUS = (
        ('DONE', 'Done Task'),
        ('NOTDONE', 'Not Done Task')
    )

    # @staticmethod
    # def default_status():
    #     return 'Not Done Task'

    task_title = models.CharField(max_length=200)
    task_priority = models.CharField(max_length=1, choices=PRIORITY)
    task_day = models.DateField()
    task_time = models.TimeField()
    task_status = models.CharField(max_length=7, choices=STATUS, default='NOTDONE')
    task_project = models.ForeignKey(Project)

    def __str__(self):
        return self.task_title
