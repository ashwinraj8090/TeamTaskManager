from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Project, Membership, ActivityLog
from tasks.models import Task
from .forms import ProjectForm
from .utils import log_activity

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer

from django.conf import settings
User = __import__('django.contrib.auth', fromlist=['get_user_model']).get_user_model()


def is_project_admin(user, project):
    return Membership.objects.filter(
        user=user, project=project, role=Membership.ADMIN
    ).exists()


@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            Membership.objects.get_or_create(
                user=request.user,
                project=project,
                defaults={'role': Membership.ADMIN}
            )
            messages.success(request, f'Project "{project.title}" created. You are now the ADMIN.')
            log_activity(request.user, project, f'created project "{project.title}"')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@login_required
def project_list_view(request):
    member_project_ids = Membership.objects.filter(
        user=request.user
    ).values_list('project_id', flat=True)

    projects = Project.objects.filter(
        Q(owner=request.user) | Q(id__in=member_project_ids)
    ).distinct()

    query = request.GET.get('q')
    if query:
        projects = projects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    active_projects = projects.filter(is_completed=False)
    completed_projects = projects.filter(is_completed=True)

    def get_project_data(qs):
        data = []
        for project in qs:
            membership = Membership.objects.filter(user=request.user, project=project).first()
            data.append({
                'project': project,
                'role': membership.role if membership else None,
                'is_admin': membership.role == Membership.ADMIN if membership else False,
            })
        return data

    return render(request, 'project_list.html', {
        'active_project_data': get_project_data(active_projects),
        'completed_project_data': get_project_data(completed_projects),
        'query': query
    })


@login_required
def toggle_project_completion_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    membership = Membership.objects.filter(user=request.user, project=project).first()

    if not membership or membership.role != Membership.ADMIN:
        messages.error(request, "Only project admins can change completion status.")
        return redirect('project_detail', project_id=project_id)

    project.is_completed = not project.is_completed
    project.save()

    status = "completed" if project.is_completed else "restored"
    messages.success(request, f'Project "{project.title}" has been {status}.')
    log_activity(request.user, project, f'marked project as {status}')

    return redirect('project_detail', project_id=project_id)


@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    membership = Membership.objects.filter(user=request.user, project=project).first()
    if not membership and project.owner != request.user:
        messages.error(request, 'You do not have access to this project.')
        return redirect('project_list')

    tasks = Task.objects.filter(project=project).select_related('assignee')
    members = Membership.objects.filter(project=project).select_related('user').order_by('role', 'user__email')

    role = membership.role if membership else None
    is_admin = role == Membership.ADMIN
    
    recent_activity = project.activity_logs.select_related('user').order_by('-timestamp')[:3]

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'members': members,
        'role': role,
        'is_admin': is_admin,
        'recent_activity': recent_activity,
    })


@login_required
def add_member_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if not is_project_admin(request.user, project):
        messages.error(request, 'Only project admins can add members.')
        return redirect('project_detail', project_id=project_id)

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        role = request.POST.get('role', Membership.MEMBER)

        if role not in [Membership.ADMIN, Membership.MEMBER]:
            role = Membership.MEMBER

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, f'No user found with email "{email}".')
            return redirect('add_member', project_id=project_id)

        if user == request.user:
            messages.warning(request, 'You are already a member of this project.')
            return redirect('project_detail', project_id=project_id)

        membership, created = Membership.objects.get_or_create(
            user=user,
            project=project,
            defaults={'role': role}
        )

        if created:
            messages.success(request, f'{user.username} added as {role}.')
            log_activity(request.user, project, f'added {user.username} as {role}')
        else:
            messages.warning(request, f'{user.username} is already a member (role: {membership.role}).')

        return redirect('project_detail', project_id=project_id)

    members = Membership.objects.filter(project=project).select_related('user')
    return render(request, 'add_member.html', {'project': project, 'members': members})


@login_required
def remove_member_view(request, project_id, membership_id):
    project = get_object_or_404(Project, id=project_id)

    if not is_project_admin(request.user, project):
        messages.error(request, 'Only project admins can remove members.')
        return redirect('project_detail', project_id=project_id)

    membership = get_object_or_404(Membership, id=membership_id, project=project)

    admin_count = Membership.objects.filter(project=project, role=Membership.ADMIN).count()
    if membership.role == Membership.ADMIN and admin_count <= 1:
        messages.error(request, 'Cannot remove the last ADMIN. Promote another member first.')
        return redirect('project_detail', project_id=project_id)

    username = membership.user.username
    membership.delete()
    messages.success(request, f'{username} has been removed from the project.')
    log_activity(request.user, project, f'removed {username} from the project')
    return redirect('project_detail', project_id=project_id)


@login_required
def change_role_view(request, project_id, membership_id):
    project = get_object_or_404(Project, id=project_id)

    if not is_project_admin(request.user, project):
        messages.error(request, 'Only project admins can change roles.')
        return redirect('project_detail', project_id=project_id)

    membership = get_object_or_404(Membership, id=membership_id, project=project)

    if membership.role == Membership.ADMIN:
        admin_count = Membership.objects.filter(project=project, role=Membership.ADMIN).count()
        if admin_count <= 1:
            messages.error(request, 'Cannot demote the last ADMIN. Promote another member first.')
            return redirect('project_detail', project_id=project_id)
        membership.role = Membership.MEMBER
    else:
        membership.role = Membership.ADMIN

    membership.save()
    messages.success(request, f'{membership.user.username} is now {membership.role}.')
    log_activity(request.user, project, f'changed {membership.user.username}\'s role to {membership.role}')
    return redirect('project_detail', project_id=project_id)


@api_view(['GET'])
def project_api_view(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)