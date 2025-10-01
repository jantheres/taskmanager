from rest_framework import serializers
from tasks.models import Task, TaskStatus

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date', 'status', 'completion_report', 'worked_hours']
        read_only_fields = ['id', 'assigned_to', 'completion_report', 'worked_hours']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, attrs):
        status = attrs.get('status', getattr(self.instance, 'status', None))
        report = attrs.get('completion_report', getattr(self.instance, 'completion_report', None))
        hours = attrs.get('worked_hours', getattr(self.instance, 'worked_hours', None))

        if status == TaskStatus.COMPLETED:
            if not report or hours is None:
                raise serializers.ValidationError('When marking as COMPLETED, completion_report and worked_hours are required.')
            try:
                if float(hours) < 0:
                    raise serializers.ValidationError('worked_hours must be zero or positive.')
            except (TypeError, ValueError):
                raise serializers.ValidationError('worked_hours must be a number.')
        return attrs

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'assigned_to', 'status', 'completion_report', 'worked_hours']
        read_only_fields = fields