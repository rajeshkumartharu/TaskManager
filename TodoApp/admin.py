from django.contrib import admin
from .models import TasksModel

class TasksModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'due_date', 'status', 'created_at')  # use correct fields
    list_filter = ('status', 'due_date')  # filter by existing fields
    search_fields = ('title', 'description')
    ordering = ('due_date',)  # order by an existing field
    list_editable = ('status',)  # allow inline editing for status only

admin.site.register(TasksModel, TasksModelAdmin)
