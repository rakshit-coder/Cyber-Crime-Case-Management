"""
Views for the Users application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from utils.security import PasswordManager
from utils.email_manager import EmailManager
from utils.validators import CERTINPasswordValidator, InputSanitizer, AccessControlValidator
from utils.captcha import CodeCaptcha, PasswordStrengthMeter
from .models import CustomUser, ActivityLog, SessionManagement
import uuid
import json


def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # Validation
            if not all([username, email, password, first_name, last_name]):
                messages.error(request, 'All fields are required.')
                return render(request, 'auth/register.html')
            
            # Input sanitization
            try:
                username = InputSanitizer.sanitize(username)
                first_name = InputSanitizer.sanitize(first_name)
                last_name = InputSanitizer.sanitize(last_name)
                if phone:
                    InputSanitizer.validate_phone(phone)
                InputSanitizer.validate_email(email)
            except ValidationError as e:
                messages.error(request, str(e.message))
                return render(request, 'auth/register.html')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'auth/register.html')
            
            # CERT-IN Password Policy Validation (16-21 characters)
            password_validator = CERTINPasswordValidator()
            try:
                password_validator.validate(password)
            except ValidationError as e:
                messages.error(request, str(e.message))
                return render(request, 'auth/register.html')
            
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'auth/register.html')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'auth/register.html')
            
            # Create user with bcrypt hashed password
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='user'
            )
            user.set_password(password)
            user.email_verification_token = str(uuid.uuid4())
            user.save()
            
            # Send verification email
            try:
                EmailManager.send_registration_email(email, first_name, user.email_verification_token)
                messages.success(request, 'Registration successful! Check your email to verify your account.')
            except Exception as e:
                messages.warning(request, 'User created but email verification failed. You can still login.')
            
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'auth/register.html')
    
    return render(request, 'auth/register.html')


def login_view(request):
    """Handle user login with CAPTCHA protection."""
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            captcha_code = request.POST.get('captcha_code', '').strip()
            captcha_hash = request.POST.get('captcha_hash', '')
            captcha_timestamp = request.POST.get('captcha_timestamp', '')
            
            if not all([username, password]):
                messages.error(request, 'Username and password are required.')
                captcha = CodeCaptcha.generate_captcha()
                return render(request, 'auth/login.html', {
                    'username': username,
                    'captcha': captcha
                })
            
            # Check if account is locked due to failed attempts
            if PasswordStrengthMeter.is_account_locked(username):
                messages.error(request, 'Account locked due to multiple failed login attempts. Please try again in 15 minutes.')
                captcha = CodeCaptcha.generate_captcha()
                return render(request, 'auth/login.html', {
                    'captcha': captcha
                })
            
            # Verify CAPTCHA
            if not captcha_code or not captcha_hash:
                messages.error(request, 'Please complete the security verification.')
                captcha = CodeCaptcha.generate_captcha()
                return render(request, 'auth/login.html', {
                    'username': username,
                    'captcha': captcha
                })
            
            if not CodeCaptcha.verify_captcha(captcha_code, captcha_hash, int(captcha_timestamp) if captcha_timestamp else 0):
                messages.error(request, 'Incorrect CAPTCHA code. Please try again.')
                captcha = CodeCaptcha.generate_captcha()
                return render(request, 'auth/login.html', {
                    'username': username,
                    'captcha': captcha
                })
            
            user = CustomUser.objects.filter(username=username).first()
            
            if user and user.check_password(password):
                if not user.is_active:
                    messages.error(request, 'This account is inactive.')
                    captcha = CodeCaptcha.generate_captcha()
                    return render(request, 'auth/login.html', {
                        'captcha': captcha
                    })
                
                # Reset failed login attempts on successful login
                PasswordStrengthMeter.reset_failed_attempts(username)
                
                login(request, user)
                
                # Create session record for audit trail
                session_token = str(uuid.uuid4())
                ip_address = get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                
                SessionManagement.objects.create(
                    user=user,
                    session_token=session_token,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                # Log activity
                ActivityLog.objects.create(
                    user=user,
                    action='login',
                    description=f'User logged in from {ip_address}',
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'officer':
                    return redirect('dashboard')
                else:  # user role
                    return redirect('dashboard')
            else:
                # Record failed attempt
                PasswordStrengthMeter.record_failed_attempt(username)
                
                messages.error(request, 'Invalid username or password.')
                captcha = CodeCaptcha.generate_captcha()
                return render(request, 'auth/login.html', {
                    'username': username,
                    'captcha': captcha
                })
        
        except Exception as e:
            messages.error(request, f'Login failed: {str(e)}')
            captcha = CodeCaptcha.generate_captcha()
            return render(request, 'auth/login.html', {
                'captcha': captcha
            })
    
    # GET request: Generate new CAPTCHA for display
    captcha = CodeCaptcha.generate_captcha()
    return render(request, 'auth/login.html', {
        'captcha': captcha
    })


def force_password_reset_view(request):
    """Force user to reset password to meet CERT-IN 16-21 character requirement."""
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user needs password reset
    request.user.refresh_from_db()
    if not request.user.password_needs_reset:
        messages.success(request, 'Password already meets security requirements.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not new_password or not confirm_password:
            messages.error(request, 'Please enter both passwords.')
            return render(request, 'auth/force_reset_password.html')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/force_reset_password.html')
        
        # Validate new password against CERT-IN requirements
        password_validator = CERTINPasswordValidator()
        try:
            password_validator.validate(new_password)
        except ValidationError as e:
            messages.error(request, str(e.message))
            return render(request, 'auth/force_reset_password.html')
        
        # Set new password
        request.user.set_password(new_password)
        request.user.password_needs_reset = False
        request.user.save()
        
        # Log password change activity
        ip_address = get_client_ip(request)
        ActivityLog.objects.create(
            user=request.user,
            action='other',
            description='User updated password to meet CERT-IN requirement',
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        messages.success(request, 'Password updated successfully! Please login again.')
        logout(request)
        return redirect('login')
    
    return render(request, 'auth/force_reset_password.html')


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout."""
    ip_address = get_client_ip(request)
    
    # Log logout activity
    ActivityLog.objects.create(
        user=request.user,
        action='logout',
        description=f'User logged out from {ip_address}',
        ip_address=ip_address,
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')


@login_required(login_url='login')
def dashboard_view(request):
    """Main dashboard - role-based."""
    from complaints.models import Complaint
    
    # Check if user needs to reset password for CERT-IN compliance
    if request.user.password_needs_reset:
        messages.warning(request, 'Your password does not meet the latest security requirements. Please update it now.')
        return redirect('force_reset_password')
    
    context = {'user': request.user}
    
    if request.user.role == 'admin':
        # Admin dashboard context
        total_users = CustomUser.objects.filter(role='user').count()
        total_complaints = Complaint.objects.count()
        pending_count = Complaint.objects.filter(status='open').count()
        total_officers = CustomUser.objects.filter(role='officer').count()
        recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
        
        context.update({
            'total_users': total_users,
            'total_complaints': total_complaints,
            'pending_count': pending_count,
            'total_officers': total_officers,
            'recent_complaints': recent_complaints,
        })
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    elif request.user.role == 'officer':
        # Officer dashboard context
        assigned_cases = Complaint.objects.filter(assigned_officer=request.user).order_by('-created_at')
        assigned_count = assigned_cases.count()
        investigating_count = assigned_cases.filter(status='investigating').count()
        closed_count = assigned_cases.filter(status='closed').count()
        pending_count = assigned_cases.filter(status='assigned').count()
        
        context.update({
            'assigned_cases': assigned_cases[:10],
            'assigned_count': assigned_count,
            'investigating_count': investigating_count,
            'closed_count': closed_count,
            'pending_count': pending_count,
        })
        return render(request, 'dashboard/officer_dashboard.html', context)
    
    else:
        # User dashboard context
        user_complaints = Complaint.objects.filter(complainant=request.user).order_by('-created_at')
        total_complaints = user_complaints.count()
        # Use correct status values: pending, assigned, in_progress, resolved, closed
        pending_count = user_complaints.filter(status__in=['pending', 'assigned']).count()
        investigating_count = user_complaints.filter(status='in_progress').count()
        resolved_count = user_complaints.filter(status__in=['resolved', 'closed']).count()
        
        context.update({
            'complaints': user_complaints[:10],
            'user_complaints': user_complaints[:5],
            'total_complaints': total_complaints,
            'resolved_count': resolved_count,
            'pending_count': pending_count,
            'investigating_count': investigating_count,
        })
        return render(request, 'dashboard/user_dashboard.html', context)


@login_required(login_url='login')
def profile_view(request):
    """User profile page."""
    user = request.user
    
    if request.method == 'POST':
        # Check if user is authorized to update this profile
        # Only the user themselves or admins can update a profile
        if request.user != user and request.user.role != 'admin':
            messages.error(request, 'You do not have permission to edit this profile.')
            return redirect('profile')
        
        try:
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.phone = request.POST.get('phone', user.phone)
            
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            
            user.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description='Updated profile information',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        
        except Exception as e:
            messages.error(request, f'Profile update failed: {str(e)}')
    
    # Check if current user is authorized to edit this profile
    can_edit = (request.user == user) or (request.user.role == 'admin')
    
    context = {'user': user, 'can_edit': can_edit}
    return render(request, 'user/profile.html', context)


def landing_view(request):
    """Landing page."""
    return render(request, 'landing.html')


def cyber_awareness_view(request):
    """Cyber awareness page - accessible to all."""
    return render(request, 'awareness/cyber_awareness.html')


@login_required(login_url='login')
def admin_dashboard_view(request):
    """Admin dashboard view."""
    # Check if user is admin
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('landing')
    
    from complaints.models import Complaint
    from django.views.decorators.http import condition
    
    # Get all statistics with accurate counts
    total_users = CustomUser.objects.filter(role='user').count()
    total_complaints = Complaint.objects.count()
    
    # Count by exact status values from database
    # Use status field values consistently
    pending_count = Complaint.objects.filter(status='pending').count()
    assigned_count = Complaint.objects.filter(status='assigned').count()
    investigating_count = Complaint.objects.filter(status='in_progress').count()
    resolved_count = Complaint.objects.filter(status='resolved').count()
    closed_count = Complaint.objects.filter(status='closed').count()
    
    total_officers = CustomUser.objects.filter(role='officer').count()
    
    # Get recent complaints for display
    recent_complaints = Complaint.objects.all().order_by('-created_at')[:10]
    unassigned_complaints = Complaint.objects.filter(assigned_officer__isnull=True).order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_complaints': total_complaints,
        'pending_count': pending_count,
        'assigned_count': assigned_count,
        'investigating_count': investigating_count,
        'resolved_count': resolved_count,
        'closed_count': closed_count,
        'total_officers': total_officers,
        'recent_complaints': recent_complaints,
        'unassigned_complaints': unassigned_complaints,
    }
    
    response = render(request, 'dashboard/admin_dashboard.html', context)
    
    # Disable caching for this response
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response


@login_required(login_url='login')
def manage_users_view(request):
    """Manage users view."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    from complaints.models import Complaint
    users = CustomUser.objects.filter(role='user').order_by('-created_at')
    
    # Paginate
    from django.core.paginator import Paginator
    paginator = Paginator(users, 10)
    page_num = request.GET.get('page', 1)
    users_page = paginator.get_page(page_num)
    
    # Add complaint count for each user
    user_data = []
    for user in users_page:
        complaint_count = Complaint.objects.filter(complainant=user).count()
        user_data.append({
            'user': user,
            'complaint_count': complaint_count,
        })
    
    context = {
        'users': users_page,
        'user_data': user_data,
        'total': paginator.count,
    }
    return render(request, 'admin/manage_users.html', context)


@login_required(login_url='login')
def manage_officers_view(request):
    """Manage officers view."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    from complaints.models import Complaint
    officers = CustomUser.objects.filter(role='officer').order_by('-created_at')
    
    # Paginate
    from django.core.paginator import Paginator
    paginator = Paginator(officers, 10)
    page_num = request.GET.get('page', 1)
    officers_page = paginator.get_page(page_num)
    
    # Add case info for each officer
    officer_data = []
    for officer in officers_page:
        assigned_cases = Complaint.objects.filter(assigned_officer=officer).count()
        investigating = Complaint.objects.filter(assigned_officer=officer, status__in=['in_progress', 'investigating']).count()
        closed = Complaint.objects.filter(assigned_officer=officer, status__in=['closed', 'resolved']).count()
        officer_data.append({
            'officer': officer,
            'assigned_cases': assigned_cases,
            'investigating': investigating,
            'closed': closed,
        })
    
    context = {
        'officers': officers_page,
        'officer_data': officer_data,
        'total': paginator.count,
    }
    return render(request, 'admin/manage_officers.html', context)


@login_required(login_url='login')
def admin_cases_view(request):
    """Admin view all cases."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    from complaints.models import Complaint
    from django.core.paginator import Paginator
    
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)
    
    # Filter by priority
    priority = request.GET.get('priority')
    if priority:
        complaints = complaints.filter(priority=priority)
    
    # Search
    search = request.GET.get('search')
    if search:
        complaints = complaints.filter(
            case_number__icontains=search
        ) | complaints.filter(
            title__icontains=search
        )
    
    # Paginate
    paginator = Paginator(complaints, 10)
    page_num = request.GET.get('page', 1)
    complaints_page = paginator.get_page(page_num)
    
    context = {
        'complaints': complaints_page,
        'total': paginator.count,
    }
    return render(request, 'admin/cases.html', context)


def get_client_ip(request):
    """Get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required(login_url='login')
def add_user_view(request):
    """Add new user (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone', '')
            
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'admin/add_user.html')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'admin/add_user.html')
            
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='user',
            )
            
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Created new user: {username}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, f'User "{username}" created successfully!')
            return redirect('manage_users')
        
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'admin/add_user.html')


@login_required(login_url='login')
@login_required(login_url='login')
def edit_user_view(request, user_id):
    """Edit user (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        try:
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.email = request.POST.get('email', user.email)
            user.phone = request.POST.get('phone', user.phone)
            
            new_password = request.POST.get('password')
            if new_password:
                # Validate password length (CERT-IN requirement)
                if len(new_password) < 16:
                    messages.error(request, 'Password must be at least 16 characters long (CERT-IN requirement).')
                    context = {'edit_user': user}
                    return render(request, 'admin/edit_user.html', context)
                
                user.set_password(new_password)
            
            user.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Updated user: {user.username}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, f'User "{user.username}" updated successfully!')
            return redirect('manage_users')
        
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    context = {'edit_user': user}
    return render(request, 'admin/edit_user.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def toggle_user_status(request, user_id):
    """Toggle user active status (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if user == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('manage_users')
    
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'deactivated'
    
    ActivityLog.objects.create(
        user=request.user,
        action='other',
        description=f'{status.capitalize()} user: {user.username}',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    messages.success(request, f'User "{user.username}" has been {status}.')
    return redirect('manage_users')


@login_required(login_url='login')
def add_officer_view(request):
    """Add new officer (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone', '')
            badge_number = request.POST.get('badge_number', '')
            department = request.POST.get('department', '')
            
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'admin/add_officer.html')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'admin/add_officer.html')
            
            officer = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role='officer',
                badge_number=badge_number,
                department=department,
            )
            
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Created new officer: {username}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, f'Officer "{first_name} {last_name}" created successfully!')
            return redirect('manage_officers')
        
        except Exception as e:
            messages.error(request, f'Error creating officer: {str(e)}')
    
    return render(request, 'admin/add_officer.html')


@login_required(login_url='login')
def edit_officer_view(request, officer_id):
    """Edit officer (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    officer = get_object_or_404(CustomUser, id=officer_id, role='officer')
    
    if request.method == 'POST':
        try:
            officer.first_name = request.POST.get('first_name', officer.first_name)
            officer.last_name = request.POST.get('last_name', officer.last_name)
            officer.email = request.POST.get('email', officer.email)
            officer.phone = request.POST.get('phone', officer.phone)
            officer.badge_number = request.POST.get('badge_number', officer.badge_number)
            officer.department = request.POST.get('department', officer.department)
            
            new_password = request.POST.get('password')
            if new_password:
                officer.set_password(new_password)
            
            officer.save()
            
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Updated officer: {officer.username}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, f'Officer "{officer.get_full_name()}" updated successfully!')
            return redirect('manage_officers')
        
        except Exception as e:
            messages.error(request, f'Error updating officer: {str(e)}')
    
    context = {'officer': officer}
    return render(request, 'admin/edit_officer.html', context)


@login_required(login_url='login')
def email_settings_view(request):
    """Email settings page (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    from django.conf import settings as django_settings
    
    email_config = {
        'EMAIL_BACKEND': django_settings.EMAIL_BACKEND,
        'EMAIL_HOST': django_settings.EMAIL_HOST,
        'EMAIL_PORT': django_settings.EMAIL_PORT,
        'EMAIL_USE_TLS': django_settings.EMAIL_USE_TLS,
        'EMAIL_HOST_USER': django_settings.EMAIL_HOST_USER,
        'DEFAULT_FROM_EMAIL': django_settings.DEFAULT_FROM_EMAIL,
        'is_console_backend': 'console' in django_settings.EMAIL_BACKEND,
    }
    
    context = {'email_config': email_config}
    return render(request, 'admin/email_settings.html', context)


@login_required(login_url='login')
def send_test_email_view(request):
    """Send a test email (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('landing')
    
    if request.method == 'POST':
        test_email = request.POST.get('test_email', request.user.email)
        
        try:
            EmailManager.send_test_email(test_email)
            messages.success(request, f'Test email sent successfully to {test_email}!')
        except Exception as e:
            messages.error(request, f'Failed to send test email: {str(e)}')
    
    return redirect('email_settings')


def forgot_password_view(request):
    """Handle forgot password request and send OTP."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'auth/forgot_password.html')
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate 6-digit OTP
            import random
            otp = str(random.randint(100000, 999999))
            
            # Set OTP expiry to 15 minutes from now
            from django.utils import timezone
            from datetime import timedelta
            user.password_reset_otp = otp
            user.password_reset_otp_expiry = timezone.now() + timedelta(minutes=15)
            user.save()
            
            # Send OTP via email
            EmailManager.send_password_reset_email(email, user.first_name or user.username, otp)
            
            messages.success(request, 'OTP has been sent to your email. Please check your inbox.')
            return redirect('verify_otp')
        
        except CustomUser.DoesNotExist:
            # Don't reveal if email exists (security best practice)
            messages.success(request, 'If an account with that email exists, you will receive an OTP.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'auth/forgot_password.html')
    
    return render(request, 'auth/forgot_password.html')


def verify_otp_view(request):
    """Verify OTP and allow password reset."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        otp = request.POST.get('otp', '').strip()
        
        if not email or not otp:
            messages.error(request, 'Please enter email and OTP.')
            return render(request, 'auth/verify_otp.html')
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Check if OTP matches
            if user.password_reset_otp != otp:
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, 'auth/verify_otp.html')
            
            # Check if OTP is expired
            from django.utils import timezone
            if timezone.now() > user.password_reset_otp_expiry:
                messages.error(request, 'OTP has expired. Please request a new one.')
                return render(request, 'auth/verify_otp.html')
            
            # OTP is valid - show password reset form
            request.session['otp_verified_email'] = email
            messages.success(request, 'OTP verified! Please set your new password.')
            return redirect('set_new_password')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'auth/verify_otp.html')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'auth/verify_otp.html')
    
    return render(request, 'auth/verify_otp.html')


def set_new_password_view(request):
    """Set new password after OTP verification."""
    # Check if user has verified OTP
    verified_email = request.session.get('otp_verified_email')
    if not verified_email:
        messages.error(request, 'Please verify your OTP first.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'auth/set_new_password.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/set_new_password.html')
        
        try:
            user = CustomUser.objects.get(email=verified_email)
            
            # Validate password strength (CERT-IN: minimum 16 characters)
            if len(password) < 16:
                messages.error(request, 'Password must be at least 16 characters long (CERT-IN requirement).')
                return render(request, 'auth/set_new_password.html')
            
            # Set new password
            user.set_password(password)
            user.password_reset_otp = ''  # Clear OTP after use
            user.password_reset_otp_expiry = None
            user.password_needs_reset = False
            user.save()
            
            # Clear session
            del request.session['otp_verified_email']
            
            # Log the action
            ActivityLog.objects.create(
                user=user,
                action='other',
                description='Password reset via OTP',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, 'Password has been reset successfully. You can now login.')
            return redirect('login')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found.')


# Language Switching View
from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.i18n import set_language as django_set_language


def set_language_view(request):
    """
    Custom view to set language preference.
    Stores language in both session and cookie.
    """
    if request.method == 'POST':
        language = request.POST.get('language', 'en')
        next_url = request.POST.get('next', '/')
        
        # Validate language choice
        valid_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in valid_languages:
            language = 'en'
        
        # Set language in session
        if hasattr(request, 'session'):
            request.session['django_language'] = language
            request.session.modified = True
        
        # Create response and set language cookie
        response = django_set_language(request)
        if not isinstance(response, HttpResponseRedirect):
            response = HttpResponseRedirect(next_url)
        
        # Set language cookie explicitly
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path='/',
        )
        
        return response
    
    # GET request - redirect to home
    return redirect('/')


def reset_password_view(request, token):
    """Deprecated: Use OTP-based system instead. Kept for backwards compatibility."""
    try:
        user = CustomUser.objects.get(email_verification_token=token)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('login')
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not password or not confirm_password:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'auth/reset_password.html', {'token': token})
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/reset_password.html', {'token': token})
        
        try:
            # Validate password strength
            if len(password) < 16:
                messages.error(request, 'Password must be at least 16 characters long (CERT-IN requirement).')
                return render(request, 'auth/reset_password.html', {'token': token})
            
            # Set new password
            user.set_password(password)
            user.email_verification_token = ''  # Clear token after use
            user.password_needs_reset = False
            user.save()
            
            messages.success(request, 'Password has been reset successfully. You can now login.')
            return redirect('login')
        
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return render(request, 'auth/reset_password.html', {'token': token})
    
    return render(request, 'auth/reset_password.html', {'token': token})
