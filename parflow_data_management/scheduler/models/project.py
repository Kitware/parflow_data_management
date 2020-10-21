from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from guardian.shortcuts import assign_perm


class Project(TimeStampedModel, models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="projects")
    # TODO: more fields

@receiver(models.signals.post_save, sender=Project)
def _project_post_save(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("scheduler.change_project", instance.owner, instance)
        assign_perm("scheduler.delete_project", instance.owner, instance)
        assign_perm("scheduler.view_project", instance.owner, instance)
        # TODO: group permissions
