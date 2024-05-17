from django.db import models

class Project(models.Model):
    """A project within which tasks are organized."""
    name = models.CharField(
        max_length=50,
        help_text="The name of the project."
    )

    def __str__(self):
        return self.name
    

class Task(models.Model):
    """A task that belongs to a project"""
    description = models.CharField(
        max_length=500,
        help_text="The task to be accomplished"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        help_text="The project this task belongs to."
    )

    def __str__(self):
        return self.description
