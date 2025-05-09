from rest_framework.permissions import BasePermission
from .models import User


class TelegramIDAuth(BasePermission):
    def has_permission(self, request, view):
        telegram_id = request.headers.get("X-Telegram-ID")
        if telegram_id:
            try:
                user = User.objects.get(telegram_id=telegram_id)
                request.user = user
                return True
            except User.DoesNotExist:
                return False
        return False
