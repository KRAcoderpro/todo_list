from celery import shared_task
from .models import Task
from .services import send_telegram_message


@shared_task
def notify_task(task_id):
    try:
        task = Task.objects.get(id=task_id)

        if task.finished:
            return

        send_telegram_message(
            task.user.telegram_id,
            f"🔔 Подошла дата выполнения задачи '{task.title}'!"
        )

        task.finished = True
        task.save()

    except Task.DoesNotExist:
        return
