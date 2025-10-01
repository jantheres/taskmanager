from django import forms
from accounts.models import User, Roles
from tasks.models import Task, TaskStatus

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'assigned_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only Admins are allowed as assigned_admin
        self.fields['assigned_admin'].queryset = User.objects.filter(role=Roles.ADMIN)
        self.fields['assigned_admin'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data['password']
        user.set_password(pwd)
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['email', 'role', 'assigned_admin', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_admin'].queryset = User.objects.filter(role=Roles.ADMIN)
        self.fields['assigned_admin'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user

class AssignUserToAdminForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(role=Roles.USER))
    admin = forms.ModelChoiceField(queryset=User.objects.filter(role=Roles.ADMIN))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if request:
            user = request.user
            if user.role == Roles.ADMIN:
                self.fields['assigned_to'].queryset = User.objects.filter(assigned_admin=user, role=Roles.USER)
            elif user.role == Roles.SUPERADMIN:
                self.fields['assigned_to'].queryset = User.objects.filter(role=Roles.USER)
        self.fields['completion_report'].required = False
        self.fields['worked_hours'].required = False

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get('status')
        report = cleaned.get('completion_report')
        hours = cleaned.get('worked_hours')
        if status == TaskStatus.COMPLETED:
            if not report or hours is None:
                raise forms.ValidationError('When marking as COMPLETED, report and worked hours are required.')
            try:
                if float(hours) < 0:
                    raise forms.ValidationError('worked_hours must be zero or positive.')
            except Exception:
                raise forms.ValidationError('worked_hours must be numeric.')
        return cleaned