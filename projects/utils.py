from .models import ActivityLog

def log_activity(user, project, action):
    ActivityLog.objects.create(
        user=user,
        project=project,
        action=action
    )
