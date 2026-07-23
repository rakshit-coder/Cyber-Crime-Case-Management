"""
Email utilities for sending notifications.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class EmailManager:
    """Handles secure email communication."""
    
    @staticmethod
    def send_registration_email(user_email: str, user_name: str, activation_token: str):
        """Send registration confirmation email."""
        subject = 'Welcome to Cyber Crime System - Verify Your Email'
        activation_link = f'{settings.BASE_URL}/verify-email/{activation_token}/'
        
        context = {
            'user_name': user_name,
            'activation_link': activation_link,
        }
        
        html_message = render_to_string('emails/registration.html', context)
        
        send_mail(
            subject,
            f'Please verify your email by clicking: {activation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_complaint_confirmation(user_email: str, user_name: str, complaint_id: str, complaint_title: str):
        """Send complaint submission confirmation."""
        subject = f'Complaint Submitted - Case #{complaint_id}'
        
        context = {
            'user_name': user_name,
            'complaint_id': complaint_id,
            'complaint_title': complaint_title,
        }
        
        html_message = render_to_string('emails/complaint_confirmation.html', context)
        
        send_mail(
            subject,
            f'Your complaint "{complaint_title}" has been received.',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_complaint_update(user_email: str, user_name: str, complaint_id: str, update_message: str):
        """Send complaint status update."""
        subject = f'Update on Your Case #{complaint_id}'
        
        context = {
            'user_name': user_name,
            'complaint_id': complaint_id,
            'update_message': update_message,
        }
        
        html_message = render_to_string('emails/complaint_update.html', context)
        
        send_mail(
            subject,
            update_message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_assignment_notification(officer_email: str, officer_name: str, complaint_id: str, complaint_title: str):
        """Send case assignment notification to officer."""
        subject = f'New Case Assignment - Case #{complaint_id}'
        
        context = {
            'officer_name': officer_name,
            'complaint_id': complaint_id,
            'complaint_title': complaint_title,
        }
        
        html_message = render_to_string('emails/case_assignment.html', context)
        
        send_mail(
            subject,
            f'You have been assigned a new case: {complaint_title}',
            settings.DEFAULT_FROM_EMAIL,
            [officer_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_case_assigned_notification(user_email: str, user_name: str, complaint_id: str, complaint_title: str, officer_name: str):
        """Send case assignment notification to complainant."""
        subject = f'Your Case Has Been Assigned - Case #{complaint_id}'
        
        context = {
            'user_name': user_name,
            'complaint_id': complaint_id,
            'complaint_title': complaint_title,
            'officer_name': officer_name,
        }
        
        html_message = render_to_string('emails/case_assigned_to_user.html', context)
        
        send_mail(
            subject,
            f'Your case "{complaint_title}" has been assigned to Investigating Officer {officer_name}.',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_email(user_email: str, user_name: str, otp: str):
        """Send password reset OTP via email."""
        subject = 'Password Reset OTP - Cyber Crime System'
        
        context = {
            'user_name': user_name,
            'otp': otp,
            'otp_expiry': '15 minutes',
        }
        
        html_message = render_to_string('emails/password_reset_otp.html', context)
        
        send_mail(
            subject,
            f'Your password reset OTP is: {otp}. This OTP is valid for 15 minutes. Do not share this OTP with anyone.',
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_test_email(to_email: str):
        """Send a test email to verify configuration."""
        subject = 'Cyber Crime System - Test Email'
        message = '''This is a test email from Cyber Crime System.

If you received this email, your email configuration is working correctly!

Configuration Details:
- Email Host: {}
- Email Port: {}
- TLS Enabled: {}

Best regards,
Cyber Crime System
'''.format(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_USE_TLS)
        
        html_message = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }}
        .container {{ background-color: white; max-width: 600px; margin: 20px auto; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
        .content {{ padding: 20px; }}
        .success {{ background-color: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 4px; color: #155724; margin: 15px 0; }}
        .footer {{ background-color: #f5f5f5; text-align: center; padding: 20px; border-top: 1px solid #e9ecef; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✓ Test Email Successful</h1>
        </div>
        <div class="content">
            <div class="success">
                <strong>Congratulations!</strong> Your email configuration is working correctly.
            </div>
            <p>This is a test email from the Cyber Crime System.</p>
            <h3>Configuration Details:</h3>
            <ul>
                <li><strong>Email Host:</strong> {host}</li>
                <li><strong>Email Port:</strong> {port}</li>
                <li><strong>TLS Enabled:</strong> {tls}</li>
            </ul>
        </div>
        <div class="footer">
            <p>&copy; 2024 Cyber Crime System. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''.format(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT, tls=settings.EMAIL_USE_TLS)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
