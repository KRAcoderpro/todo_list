from django.db import models
from django.utils.timezone import now
import hashlib


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=16, editable=False)
    telegram_id = models.CharField(
        null=False, blank=False, unique=True, editable=False
    )

    def save(self, *args, **kwargs):
        if not self.id:
            raw = f"{self.telegram_id}_{now().isoformat()}"
            self.id = hashlib.sha256(raw.encode()).hexdigest()[:16]
        super().save(*args, **kwargs)


class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=16, editable=False)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            raw = f"{self.name}_{now().isoformat()}"
            self.id = hashlib.sha256(raw.encode()).hexdigest()[:16]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.CharField(primary_key=True, max_length=16, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    due_date = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            raw = f"{self.title}_{now().isoformat()}"
            self.id = hashlib.sha256(raw.encode()).hexdigest()[:16]
        super().save(*args, **kwargs)
