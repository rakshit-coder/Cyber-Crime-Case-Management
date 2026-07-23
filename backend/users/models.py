"""
Django models for the Users application.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.security import PasswordManager, IntegrityManager


class CustomUser(AbstractUser):
    """Custom user model with role-based access control."""
    
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('officer', 'Cybercrime Officer'),
        ('admin', 'Administrator'),
    )
    
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True, help_text="For officers: Department name")
    badge_number = models.CharField(max_length=30, blank=True, null=True, help_text="For officers: Badge number")
    is_active = models.BooleanField(default=True)
    password_needs_reset = models.BooleanField(default=False, help_text="User must reset password to meet CERT-IN 16-21 character requirement")
    
    # OTP for password reset
    password_reset_otp = models.CharField(max_length=6, blank=True, null=True, help_text="6-digit OTP for password reset")
    password_reset_otp_expiry = models.DateTimeField(blank=True, null=True, help_text="OTP expiry timestamp (15 minutes)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    
    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def set_password(self, raw_password):
        """Set password using Django's default hashing."""
        super().set_password(raw_password)
    
    def check_password(self, raw_password):
        """Check password using Django's default verification."""
        return super().check_password(raw_password)


class ActivityLog(models.Model):
    """Log user activities for audit trail."""
    
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create_complaint', 'Create Complaint'),
        ('update_complaint', 'Update Complaint'),
        ('view_complaint', 'View Complaint'),
        ('assign_case', 'Assign Case'),
        ('add_remark', 'Add Remark'),
        ('upload_evidence', 'Upload Evidence'),
        ('export_report', 'Export Report'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    action_hash = models.CharField(max_length=64, help_text="SHA-256 hash for integrity")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_logs'
        verbose_name_plural = 'Activity Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        """Generate integrity hash before saving."""
        hash_string = f"{self.user_id}{self.action}{self.description}{self.created_at}"
        self.action_hash = IntegrityManager.calculate_hash(hash_string)
        super().save(*args, **kwargs)


class SessionManagement(models.Model):
    """Track user sessions for security."""
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    logged_in_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    logged_out_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'session_management'
        verbose_name_plural = 'Session Managements'
        ordering = ['-last_activity']
    
    def __str__(self):
        return f"{self.user.username} - {self.logged_in_at}"
