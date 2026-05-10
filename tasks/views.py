from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import Task
from .forms import TaskForm, TaskUpdateForm, TaskStatusUpdateForm
from projects.models import Membership, Project
from projects.utils import log_activity


@login_required
def create_task_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            project = form.cleaned_data['project']
            is_admin = Membership.objects.filter(
                user=request.user, project=project, role='ADMIN'
            ).exists()
            if not is_admin:
                return render(request, 'error.html', {
                    'message': 'Only project admins can create tasks.'
                })
            task = form.save()
            messages.success(request, f'Task "{task.title}" created.')
            log_activity(request.user, project, f'created task "{task.title}"')
            return redirect('project_detail', project_id=project.id)
    else:
        project_id = request.GET.get('project')
        form = TaskForm(user=request.user, initial={'project': project_id} if project_id else {})

    return render(request, 'create_task.html', {'form': form})


@login_required
def update_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = task.project

    membership = Membership.objects.filter(user=request.user, project=project).first()
    if not membership:
        return render(request, 'error.html', {'message': 'You are not a member of this project.'})

    is_admin = membership.role == Membership.ADMIN
    is_assigned = task.assignee == request.user

    if not is_admin and not is_assigned:
        messages.error(request, "You can only view this task or update it if it's assigned to you.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        if is_admin:
            form = TaskUpdateForm(request.POST, instance=task, project=project)
        else:
            form = TaskStatusUpdateForm(request.POST, instance=task)

        if form.is_valid():
            if not is_admin and form.cleaned_data.get('status') == Task.COMPLETED:
                messages.error(request, "Only admins can mark tasks as completed.")
                return redirect('project_detail', project_id=project.id)
            
            form.save()
            messages.success(request, f'Task "{task.title}" updated.')
            log_activity(request.user, project, f'updated task "{task.title}" ({task.status})')
            return redirect('project_detail', project_id=project.id)
    else:
        if is_admin:
            form = TaskUpdateForm(instance=task, project=project)
        else:
            form = TaskStatusUpdateForm(instance=task)

    return render(request, 'update_task.html', {
        'form': form,
        'task': task,
        'project': project,
        'is_admin': is_admin,
    })


@login_required
def task_action_view(request, task_id, action):
    task = get_object_or_404(Task, id=task_id)
    project = task.project
    membership = Membership.objects.filter(user=request.user, project=project, role=Membership.ADMIN).first()

    if not membership:
        messages.error(request, "Only project admins can perform this action.")
        return redirect('project_detail', project_id=project.id)

    if action == 'approve':
        task.status = Task.COMPLETED
        messages.success(request, f'Task "{task.title}" approved and completed.')
        log_activity(request.user, project, f'approved task "{task.title}"')
    elif action == 'reject':
        task.status = Task.PENDING
        messages.warning(request, f'Task "{task.title}" rejected and reopened.')
        log_activity(request.user, project, f'rejected and reopened task "{task.title}"')

    task.save()
    return redirect('project_detail', project_id=project.id)


@login_required
def task_list_view(request):
    member_project_ids = Membership.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)

    tasks = Task.objects.filter(
        Q(project__owner=request.user) | Q(project__id__in=member_project_ids)
    ).distinct().select_related('project', 'assignee')

    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def get_members_api(request):
    project_id = request.GET.get("project_id")
    if not project_id:
        return JsonResponse({"members": []})
    
    members = Membership.objects.filter(project_id=project_id).select_related("user")
    member_data = [
        {"id": m.user.id, "username": m.user.username}
        for m in members
    ]
    return JsonResponse({"members": member_data})
