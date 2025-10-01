from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import MyTasksListView, TaskUpdateView, TaskReportView

urlpatterns = [
    # Auth (JWT)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Tasks
    path('tasks/', MyTasksListView.as_view(), name='my_tasks'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/report/', TaskReportView.as_view(), name='task_report'),
]