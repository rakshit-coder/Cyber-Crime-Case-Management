"""
Django models for the Complaints application.
"""
from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import CustomUser
from utils.security import EncryptionManager, IntegrityManager


class Complaint(models.Model):
    """Main complaint/case model."""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    )
    
    APPROVAL_STATUS_CHOICES = (
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    COMPLAINT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('near_to_close', 'Near to Close'),
        ('closed', 'Closed'),
    )
    
    CATEGORY_CHOICES = (
        ('phishing', 'Phishing'),
        ('identity_theft', 'Identity Theft'),
        ('online_fraud', 'Online Fraud'),
        ('cyberbullying', 'Cyberbullying'),
        ('hacking', 'Hacking'),
        ('ransomware', 'Ransomware'),
        ('data_breach', 'Data Breach'),
        ('other', 'Other'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    # Case Information
    case_number = models.CharField(max_length=30, unique=True, editable=False)
    complainant = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='complaints')
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    # Status Management
    status = models.CharField(max_length=15, choices=COMPLAINT_STATUS_CHOICES, default='pending')
    approval_status = models.CharField(max_length=17, choices=APPROVAL_STATUS_CHOICES, default='pending_approval')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    assigned_officer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                        null=True, blank=True, 
                                        limit_choices_to={'role': 'officer'},
                                        related_name='assigned_complaints')
    
    # Incident Details
    incident_date = models.DateTimeField(help_text="When the incident occurred")
    incident_location = models.CharField(max_length=30, blank=True, null=True)
    affected_system = models.CharField(max_length=30, blank=True, null=True, help_text="e.g., Email, Bank Account, Social Media")
    
    # Encryption of sensitive details
    encrypted_evidence_summary = models.TextField(blank=True, null=True, help_text="Encrypted summary of sensitive evidence")
    
    # Approval Tracking
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, 
                                   null=True, blank=True, 
                                   related_name='approved_complaints',
                                   help_text="Admin who approved the complaint")
    approval_date = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin's reason for rejection or approval notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    # Integrity
    integrity_hash = models.CharField(max_length=64, help_text="SHA-256 hash for integrity")
    
    class Meta:
        db_table = 'complaints'
        verbose_name_plural = 'Complaints'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['case_number']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['assigned_officer', 'status']),
            models.Index(fields=['complainant', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.case_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        """Generate case number and integrity hash."""
        if not self.case_number:
            # Generate case number: C-YYYY-MM-XXXXX
            from datetime import datetime
            year_month = datetime.now().strftime('%Y%m')
            last_complaint = Complaint.objects.filter(case_number__startswith=f'C-{year_month}').order_by('case_number').last()
            
            if last_complaint:
                last_number = int(last_complaint.case_number.split('-')[-1])
                new_number = f"{last_number + 1:05d}"
            else:
                new_number = "00001"
            
            self.case_number = f"C-{year_month}-{new_number}"
        
        # Generate integrity hash
        hash_string = f"{self.case_number}{self.complainant_id}{self.title}{self.description}{self.category}"
        self.integrity_hash = IntegrityManager.calculate_hash(hash_string)
        
        super().save(*args, **kwargs)


class Evidence(models.Model):
    """File uploads for complaints."""
    
    FILE_TYPE_CHOICES = (
        ('screenshot', 'Screenshot'),
        ('document', 'Document'),
        ('email', 'Email'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    )
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='evidence_files')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file = models.FileField(
        upload_to='evidence/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'txt', 'mp4', 'mp3'])]
    )
    original_filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="File size in bytes")
    file_hash = models.CharField(max_length=64, help_text="SHA-256 hash of the file")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'evidence'
        verbose_name_plural = 'Evidence Files'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['complaint', '-uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.original_filename} - {self.complaint.case_number}"
    
    def save(self, *args, **kwargs):
        """Calculate file hash and size."""
        if self.file:
            self.file_size = self.file.size
            self.original_filename = self.file.name
            # File hash will be calculated during upload
        super().save(*args, **kwargs)


class Remark(models.Model):
    """Officer remarks/comments on complaints."""
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='remarks')
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    content = models.TextField()
    is_internal = models.BooleanField(default=False, help_text="Internal remarks not visible to complainant")
    is_encrypted = models.BooleanField(default=False)
    encrypted_content = models.TextField(blank=True, null=True)
    remark_hash = models.CharField(max_length=64, help_text="SHA-256 hash for integrity")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'remarks'
        verbose_name_plural = 'Remarks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['complaint', '-created_at']),
        ]
    
    def __str__(self):
        return f"Remark by {self.author.username} on {self.complaint.case_number}"
    
    def save(self, *args, **kwargs):
        """Encrypt sensitive remarks and generate hash."""
        # Encrypt internal remarks
        if self.is_internal and not self.is_encrypted:
            self.encrypted_content = EncryptionManager.encrypt_data(self.content)
            self.is_encrypted = True
        
        # Generate integrity hash
        hash_string = f"{self.complaint_id}{self.author_id}{self.content}{self.created_at}"
        self.remark_hash = IntegrityManager.calculate_hash(hash_string)
        
        super().save(*args, **kwargs)


class ComplaintAttachment(models.Model):
    """Additional attachments for complaints (phone numbers, email addresses, URLs)."""
    
    ATTACHMENT_TYPE_CHOICES = (
        ('phone', 'Phone Number'),
        ('email', 'Email Address'),
        ('url', 'URL/Website'),
        ('social_media', 'Social Media Account'),
        ('bank_details', 'Bank Details'),
        ('other', 'Other'),
    )
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments')
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES)
    value = models.TextField()
    is_encrypted = models.BooleanField(default=False)
    encrypted_value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'complaint_attachments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_attachment_type_display()} - {self.complaint.case_number}"
    
    def save(self, *args, **kwargs):
        """Encrypt sensitive attachment data."""
        if not self.is_encrypted:
            self.encrypted_value = EncryptionManager.encrypt_data(self.value)
            self.is_encrypted = True
        super().save(*args, **kwargs)


class AdminNotification(models.Model):
    """Notifications for admin approval of new complaints."""
    
    NOTIFICATION_TYPE_CHOICES = (
        ('new_complaint', 'New Complaint'),
        ('complaint_approved', 'Complaint Approved'),
        ('complaint_rejected', 'Complaint Rejected'),
        ('urgent_case', 'Urgent Case'),
    )
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='notifications')
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_notifications',
                             limit_choices_to={'role': 'admin'})
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'admin_notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['admin', 'is_read', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.notification_type} - {self.complaint.case_number}"
