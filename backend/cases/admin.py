from django.contrib import admin
from .models import CaseWorkflow, CaseReport, CaseStatistics


@admin.register(CaseWorkflow)
class CaseWorkflowAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'action', 'performed_by', 'created_at')
    list_filter = ('action', 'created_at', 'performed_by')
    search_fields = ('complaint__case_number', 'performed_by__username')
    readonly_fields = ('action_hash', 'created_at')


@admin.register(CaseReport)
class CaseReportAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'report_title', 'generated_by', 'created_at')
    list_filter = ('created_at', 'generated_by')
    search_fields = ('complaint__case_number', 'report_title')
    readonly_fields = ('report_hash', 'created_at', 'updated_at')


@admin.register(CaseStatistics)
class CaseStatisticsAdmin(admin.ModelAdmin):
    list_display = ('total_complaints', 'pending_complaints', 'resolved_complaints', 'updated_at')
    readonly_fields = ('updated_at',)
