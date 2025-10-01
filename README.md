Task Management App (Django + DRF + JWT)
Enhancement: When users complete a task, they must submit a short report and worked hours. Admins and SuperAdmins can review these reports via API and in a custom Admin Panel.

Tech:

Django 5

Django REST Framework

SimpleJWT

SQLite (default)

Features

Roles: SUPERADMIN, ADMIN, USER

JWT auth for API

User APIs:

GET /api/tasks/ → Only tasks for the logged-in user
PUT /api/tasks/{id}/ → Update status; when status=COMPLETED, must include completion_report + worked_hours

Admin-only API:
GET /api/tasks/{id}/report/ → Admin/SuperAdmin only, and only for COMPLETED tasks

Custom Admin Panel (HTML templates):

SuperAdmin:
Manage users and admins (create/delete/assign roles)
Assign users to admins
Manage all tasks; view reports

Admin:
Manage tasks for their assigned users
View completion reports with worked hours
