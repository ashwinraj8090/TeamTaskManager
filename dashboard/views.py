from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tasks.models import Task
from projects.models import Membership

from django.utils.timezone import now

@login_required
def dashboard_view(request):

    member_project_ids = Membership.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)

    tasks = Task.objects.filter(
        Q(project__owner=request.user) | Q(project__id__in=member_project_ids)
    ).distinct()

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status='COMPLETED'
    ).count()

    pending_tasks = tasks.filter(
        status='PENDING'
    ).count()

    overdue_list = tasks.filter(
        due_date__lt=now().date(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).select_related('project')
    overdue_tasks = overdue_list.count()

    from projects.models import ActivityLog
    recent_activity = ActivityLog.objects.filter(
        project__id__in=member_project_ids
    ).select_related('user', 'project').order_by('-timestamp')[:3]

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'overdue_list': overdue_list,
        'recent_activity': recent_activity,
    }

    return render(
        request,
        'dashboard.html',
        context
    )