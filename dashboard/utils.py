from .models import NotificationModel  # Adjust based on your Notification model

def notifications(request):
    if request.user.is_authenticated:
        return {
            'notifications': NotificationModel.objects.filter(user=request.user).order_by('-created_at')[:6],
            'unread_notifications_count': NotificationModel.objects.filter(user=request.user, is_read=False).count(),
        }
    return {
        'notifications': [],
        'unread_notifications_count': 0,
    }