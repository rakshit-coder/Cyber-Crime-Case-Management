from django.contrib import admin
from .models import Complaint, Evidence, Remark, ComplaintAttachment


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'title', 'category', 'status', 'priority', 'complainant', 'assigned_officer', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at', 'assigned_officer')
    search_fields = ('case_number', 'title', 'complainant__username', 'assigned_officer__username')
    readonly_fields = ('case_number', 'integrity_hash', 'created_at', 'updated_at', 'resolved_at')
    fieldsets = (
        ('Case Information', {'fields': ('case_number', 'title', 'description', 'category')}),
        ('Status', {'fields': ('status', 'priority', 'assigned_officer')}),
        ('Incident Details', {'fields': ('incident_date', 'incident_location', 'affected_system')}),
        ('Complainant', {'fields': ('complainant',)}),
        ('Security', {'fields': ('integrity_hash', 'encrypted_evidence_summary'), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'resolved_at'), 'classes': ('collapse',)}),
    )


@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'complaint', 'file_type', 'file_size', 'uploaded_by', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at', 'complaint__status')
    search_fields = ('original_filename', 'complaint__case_number')
    readonly_fields = ('file_hash', 'file_size', 'uploaded_at')


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'author', 'is_internal', 'is_encrypted', 'created_at')
    list_filter = ('is_internal', 'is_encrypted', 'created_at', 'author')
    search_fields = ('complaint__case_number', 'author__username', 'content')
    readonly_fields = ('remark_hash', 'created_at', 'updated_at')


@admin.register(ComplaintAttachment)
class ComplaintAttachmentAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'attachment_type', 'is_encrypted', 'created_at')
    list_filter = ('attachment_type', 'is_encrypted', 'created_at')
    search_fields = ('complaint__case_number',)
