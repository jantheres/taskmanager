from django.urls import path
from .views import (
    PanelLoginView, PanelLogoutView, dashboard,
    users_list, user_create, user_edit, user_delete, assign_user_to_admin,
    tasks_list, task_create, task_edit, task_report
)

urlpatterns = [
    path('login/', PanelLoginView.as_view(), name='panel_login'),
    path('logout/', PanelLogoutView.as_view(), name='panel_logout'),  # uses the subclass above
    path('', dashboard, name='panel_dashboard'),
    path('users/', users_list, name='panel_users'),
    path('users/create/', user_create, name='panel_user_create'),
    path('users/<int:user_id>/edit/', user_edit, name='panel_user_edit'),
    path('users/<int:user_id>/delete/', user_delete, name='panel_user_delete'),
    path('assign/', assign_user_to_admin, name='panel_assign_user'),
    path('tasks/', tasks_list, name='panel_tasks'),
    path('tasks/create/', task_create, name='panel_task_create'),
    path('tasks/<int:task_id>/edit/', task_edit, name='panel_task_edit'),
    path('tasks/<int:task_id>/report/', task_report, name='panel_task_report'),
]