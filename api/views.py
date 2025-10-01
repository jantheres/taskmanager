from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import get_object_or_404

from tasks.models import Task, TaskStatus
from api.serializers import TaskSerializer, TaskUpdateSerializer, TaskReportSerializer
from api.permissions import IsAdminOrSuperAdmin
from accounts.models import Roles, User

# JWT endpoints are provided by SimpleJWT; we just route them in urls.py

class MyTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by('-id')

class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow updating tasks assigned to the requester
        return Task.objects.filter(assigned_to=self.request.user)

    def update(self, request, *args, **kwargs):
        # Only allow updating status and (conditionally) report/hours
        return super().update(request, *args, **kwargs)

class TaskReportView(generics.RetrieveAPIView):
    serializer_class = TaskReportSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    lookup_url_kwarg = 'pk'

    def get_object(self):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        if task.status != TaskStatus.COMPLETED:
            # Only available for completed tasks
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Report available only for completed tasks.')

        user = self.request.user
        if user.role == Roles.SUPERADMIN:
            return task
        # Admin can only view tasks of their managed users
        if user.role == Roles.ADMIN and task.assigned_to.assigned_admin_id == user.id:
            return task

        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied('Not allowed to view this task report.')