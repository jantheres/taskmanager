Task Management App (Django + DRF + JWT)

Enhancement: When users complete a task, they must submit a short report and worked hours. Admins and SuperAdmins can review these reports via API and in a custom Admin Panel.

Tech

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


Recommended demo credentials (add to README)

SuperAdmin: admin / Admin@123
Admin: an_admin / Admin@123
User: jan@31 / User@123
If you didn’t create these exact accounts, put the ones you used instead. You can also seed them quickly with:

python manage.py createsuperuser
Or use the panel to create Admin/User and assign.


Install

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Migrate

python manage.py makemigrations
python manage.py migrate

Create SuperAdmin

python manage.py createsuperuser

Run

python manage.py runserver
