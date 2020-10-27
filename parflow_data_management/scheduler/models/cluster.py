from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class Cluster(TimeStampedModel, models.Model):
    name = CharField(_("Name of Cluster"), blank=True, max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="clusters")
    # TODO: more fields

@receiver(models.signals.post_save, sender=Cluster)
def _cluster_post_save(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("scheduler.change_cluster", instance.user, instance)
        assign_perm("scheduler.delete_cluster", instance.user, instance)
        assign_perm("scheduler.view_cluster", instance.user, instance)
        # TODO: group permissions