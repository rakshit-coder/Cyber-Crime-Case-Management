"""
Django models for the Cases application.
"""
from django.db import models
from complaints.models import Complaint
from users.models import CustomUser
from utils.security import IntegrityManager


class CaseWorkflow(models.Model):
    """Track case workflow transitions."""
    
    ACTION_CHOICES = (
        ('created', 'Created'),
        ('assigned', 'Assigned to Officer'),
        ('in_investigation', 'Under Investigation'),
        ('evidence_collected', 'Evidence Collected'),
        ('analysis_done', 'Analysis Completed'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    )
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='workflow_history')
    action = models.CharField(max_length=25, choices=ACTION_CHOICES)
    performed_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    notes = models.TextField(blank=True, null=True)
    action_hash = models.CharField(max_length=64, help_text="SHA-256 hash for integrity")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'case_workflow'
        verbose_name_plural = 'Case Workflows'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['complaint', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.complaint.case_number} - {self.get_action_display()}"
    
    def save(self, *args, **kwargs):
        """Generate integrity hash."""
        hash_string = f"{self.complaint_id}{self.action}{self.performed_by_id}{self.created_at}"
        self.action_hash = IntegrityManager.calculate_hash(hash_string)
        super().save(*args, **kwargs)


class CaseReport(models.Model):
    """Generate and store investigation reports."""
    
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='report')
    report_title = models.CharField(max_length=150)
    investigation_summary = models.TextField()
    findings = models.TextField()
    recommendations = models.TextField()
    generated_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    report_hash = models.CharField(max_length=64, help_text="SHA-256 hash for integrity")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'case_reports'
        verbose_name_plural = 'Case Reports'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report - {self.complaint.case_number}"
    
    def save(self, *args, **kwargs):
        """Generate integrity hash."""
        hash_string = f"{self.complaint_id}{self.investigation_summary}{self.findings}{self.generated_by_id}"
        self.report_hash = IntegrityManager.calculate_hash(hash_string)
        super().save(*args, **kwargs)


class CaseStatistics(models.Model):
    """Dashboard statistics."""
    
    total_complaints = models.IntegerField(default=0)
    pending_complaints = models.IntegerField(default=0)
    in_progress_complaints = models.IntegerField(default=0)
    resolved_complaints = models.IntegerField(default=0)
    closed_complaints = models.IntegerField(default=0)
    
    total_users = models.IntegerField(default=0)
    total_officers = models.IntegerField(default=0)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'case_statistics'
        verbose_name_plural = 'Case Statistics'
    
    def __str__(self):
        return "System Statistics"
