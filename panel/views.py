from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LoginView, LogoutView

from accounts.models import User, Roles
from tasks.models import Task, TaskStatus
from .forms import UserCreateForm, UserUpdateForm, AssignUserToAdminForm, TaskForm


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('panel_login')
            if request.user.role not in roles:
                return HttpResponseForbidden('You do not have access to this page.')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


class PanelLoginView(LoginView):
    template_name = 'panel/login.html'


class PanelLogoutView(LogoutView):
    next_page = '/panel/login/'
    # Allow GET to avoid 405 when using a link or typing the URL
    http_method_names = ['get', 'post', 'options', 'head', 'trace']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def dashboard(request):
    if request.user.role == Roles.SUPERADMIN:
        context = {
            'users_count': User.objects.count(),
            'tasks_count': Task.objects.count(),
        }
        return render(request, 'panel/dashboard.html', context)

    if request.user.role == Roles.ADMIN:
        context = {
            'users_count': User.objects.filter(assigned_admin=request.user).count(),
            'tasks_count': Task.objects.filter(assigned_to__assigned_admin=request.user).count(),
        }
        return render(request, 'panel/dashboard.html', context)

    # Non-admins: show a friendly page
    return render(request, 'panel/forbidden.html', status=403)

@role_required(Roles.SUPERADMIN)
def users_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'panel/users_list.html', {'users': users})


@role_required(Roles.SUPERADMIN)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_users')
    else:
        form = UserCreateForm()
    return render(request, 'panel/user_form.html', {'form': form, 'title': 'Create User'})


@role_required(Roles.SUPERADMIN)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('panel_users')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'panel/user_form.html', {'form': form, 'title': f'Edit {user.username}'})


@role_required(Roles.SUPERADMIN)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('panel_users')
    return render(request, 'panel/user_form.html', {'title': f'Delete {user.username}', 'delete': True})


@role_required(Roles.SUPERADMIN)
def assign_user_to_admin(request):
    if request.method == 'POST':
        form = AssignUserToAdminForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            admin = form.cleaned_data['admin']
            user.assigned_admin = admin
            user.save()
            return redirect('panel_users')
    else:
        form = AssignUserToAdminForm()
    return render(request, 'panel/assign_user.html', {'form': form})


@role_required(Roles.SUPERADMIN, Roles.ADMIN)
def tasks_list(request):
    if request.user.role == Roles.SUPERADMIN:
        qs = Task.objects.select_related('assigned_to').order_by('-id')
    else:
        qs = Task.objects.select_related('assigned_to').filter(assigned_to__assigned_admin=request.user).order_by('-id')
    return render(request, 'panel/tasks_list.html', {'tasks': qs})


@role_required(Roles.SUPERADMIN, Roles.ADMIN)
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('panel_tasks')
    else:
        form = TaskForm(request=request)
    return render(request, 'panel/task_form.html', {'form': form, 'title': 'Create Task'})


@role_required(Roles.SUPERADMIN, Roles.ADMIN)
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role == Roles.ADMIN and task.assigned_to.assigned_admin_id != request.user.id:
        return HttpResponseForbidden('You cannot edit this task.')
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, request=request)
        if form.is_valid():
            form.save()
            return redirect('panel_tasks')
    else:
        form = TaskForm(instance=task, request=request)
    return render(request, 'panel/task_form.html', {'form': form, 'title': f'Edit Task #{task.id}'})


@role_required(Roles.SUPERADMIN, Roles.ADMIN)
def task_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.role == Roles.ADMIN and task.assigned_to.assigned_admin_id != request.user.id:
        return HttpResponseForbidden('You cannot view this task report.')
    if task.status != TaskStatus.COMPLETED:
        return HttpResponseForbidden('Report only available for completed tasks.')
    return render(request, 'panel/task_report.html', {'task': task})