"""
Views for the Cases application.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import CaseWorkflow, CaseReport, CaseStatistics
from complaints.models import Complaint
from users.models import CustomUser, ActivityLog
from users.views import get_client_ip
from django.views.decorators.http import require_http_methods
import json


@login_required(login_url='login')
def cases_list_view(request):
    """List all cases (officers and admins only)."""
    if request.user.role not in ['officer', 'admin']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.user.role == 'officer':
        cases = Complaint.objects.filter(assigned_officer=request.user)
    else:
        cases = Complaint.objects.all()
    
    # Filter
    status = request.GET.get('status')
    if status:
        cases = cases.filter(status=status)
    
    from django.core.paginator import Paginator
    paginator = Paginator(cases, 15)
    page_number = request.GET.get('page')
    cases_page = paginator.get_page(page_number)
    
    context = {
        'cases': cases_page,
        'total': paginator.count,
    }
    return render(request, 'cases/list.html', context)


@login_required(login_url='login')
def case_report_view(request, case_number):
    """Generate or view case report."""
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    # Permission check
    if request.user.role not in ['officer', 'admin']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    if request.user.role == 'officer' and complaint.assigned_officer != request.user:
        messages.error(request, 'You do not have permission to access this report.')
        return redirect('cases_list')
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action='other',
        description=f'Viewed report for case {case_number}',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    try:
        report = CaseReport.objects.get(complaint=complaint)
    except CaseReport.DoesNotExist:
        report = None
    
    context = {
        'complaint': complaint,
        'report': report,
    }
    return render(request, 'cases/report.html', context)


@login_required(login_url='login')
def dashboard_view(request):
    """Admin dashboard with statistics."""
    if request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    try:
        stats = CaseStatistics.objects.first()
    except CaseStatistics.DoesNotExist:
        stats = None
    
    context = {
        'stats': stats,
    }
    return render(request, 'cases/admin_dashboard.html', context)


def get_or_create_stats():
    """Get or create statistics."""
    from complaints.models import Complaint
    from users.models import CustomUser
    
    stats, created = CaseStatistics.objects.get_or_create(pk=1)
    
    stats.total_complaints = Complaint.objects.count()
    stats.pending_complaints = Complaint.objects.filter(status='pending').count()
    stats.in_progress_complaints = Complaint.objects.filter(status='in_progress').count()
    stats.resolved_complaints = Complaint.objects.filter(status='resolved').count()
    stats.closed_complaints = Complaint.objects.filter(status='closed').count()
    stats.total_users = CustomUser.objects.filter(role='user').count()
    stats.total_officers = CustomUser.objects.filter(role='officer').count()
    
    stats.save()
    return stats


@login_required(login_url='login')
@require_http_methods(["POST"])
def assign_case_to_officer(request):
    """Assign a case to an officer (Admin only)."""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        case_number = data.get('case_number')
        officer_id = data.get('officer_id')
        
        complaint = get_object_or_404(Complaint, case_number=case_number)
        officer = get_object_or_404(CustomUser, id=officer_id, role='officer')
        
        # Assign case
        complaint.assigned_officer = officer
        complaint.status = 'assigned'
        complaint.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='case_assigned',
            description=f'Assigned case {case_number} to officer {officer.get_full_name()}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Log activity for officer
        ActivityLog.objects.create(
            user=officer,
            action='case_received',
            description=f'Received case assignment for {case_number}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Send assignment notification to officer
        try:
            from utils.email_manager import EmailManager
            EmailManager.send_assignment_notification(
                officer.email,
                officer.get_full_name(),
                complaint.case_number,
                complaint.title
            )
        except Exception as e:
            print(f"Error sending assignment notification to officer {officer.email}: {str(e)}")
        
        # Send assignment notification to complainant
        try:
            from utils.email_manager import EmailManager
            EmailManager.send_case_assigned_notification(
                complaint.complainant.email,
                complaint.complainant.get_full_name(),
                complaint.case_number,
                complaint.title,
                officer.get_full_name()
            )
        except Exception as e:
            print(f"Error sending assignment notification to complainant {complaint.complainant.email}: {str(e)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Case {case_number} assigned to {officer.get_full_name()}',
            'officer_name': officer.get_full_name(),
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def update_case_status(request):
    """Update case status (Officer and Admin)."""
    if request.user.role not in ['officer', 'admin']:
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        case_number = data.get('case_number')
        new_status = data.get('status')
        
        complaint = get_object_or_404(Complaint, case_number=case_number)
        
        # Permission check
        if request.user.role == 'officer' and complaint.assigned_officer != request.user:
            return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
        
        old_status = complaint.status
        complaint.status = new_status
        
        if new_status in ['closed', 'resolved']:
            from django.utils import timezone
            complaint.resolved_at = timezone.now()
        
        complaint.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='status_updated',
            description=f'Updated case {case_number} status from {old_status} to {new_status}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Send email notification to complainant about status change
        try:
            from utils.email_manager import EmailManager
            status_messages = {
                'pending': 'Your complaint is pending review.',
                'in_progress': 'Your complaint is now being investigated by our team.',
                'under_review': 'Your complaint is currently under review.',
                'resolved': 'Your complaint has been resolved. Thank you for reporting.',
                'closed': 'Your complaint has been closed.',
                'rejected': 'Your complaint has been reviewed and could not be processed further.',
            }
            update_message = status_messages.get(new_status, f'Your case status has been updated to {new_status}.')
            EmailManager.send_complaint_update(
                complaint.complainant.email,
                complaint.complainant.first_name,
                complaint.case_number,
                update_message
            )
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
        
        return JsonResponse({
            'success': True,
            'message': f'Case {case_number} status updated to {new_status}',
            'new_status': new_status,
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='login')
def unassigned_cases_view(request):
    """Admin view of unassigned cases."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    from django.core.paginator import Paginator
    
    # Get unassigned cases (pending status or no assigned officer)
    unassigned = Complaint.objects.filter(
        assigned_officer__isnull=True
    ).order_by('-created_at')
    
    # Get all officers for assignment dropdown
    officers = CustomUser.objects.filter(role='officer', is_active=True).order_by('first_name')
    
    paginator = Paginator(unassigned, 10)
    page_num = request.GET.get('page', 1)
    complaints_page = paginator.get_page(page_num)
    
    context = {
        'complaints': complaints_page,
        'officers': officers,
        'total': paginator.count,
    }
    return render(request, 'admin/unassigned_cases.html', context)
