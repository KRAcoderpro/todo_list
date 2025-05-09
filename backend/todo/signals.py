from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task
from .tasks import notify_task


@receiver(post_save, sender=Task)
def schedule_notification(sender, instance, created, **kwargs):
    if instance.due_date:
        delay = (instance.due_date - timezone.now()).total_seconds()

        if delay > 0:
            notify_task.apply_async(args=[instance.id], countdown=delay)
