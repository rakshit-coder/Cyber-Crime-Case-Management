"""
Views for the Complaints application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from utils.security import EncryptionManager, IntegrityManager
from utils.email_manager import EmailManager
from utils.pdf_generator import ComplaintPDFGenerator
from .models import Complaint, Evidence, Remark, ComplaintAttachment
from cases.models import CaseWorkflow
from users.models import ActivityLog
from users.views import get_client_ip
from datetime import datetime
import os


@login_required(login_url='login')
def complaints_list_view(request):
    """Display complaints based on user role."""
    if request.user.role == 'admin':
        complaints = Complaint.objects.all()
    elif request.user.role == 'officer':
        # Officers see all complaints (assigned or pending)
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(complainant=request.user)
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        complaints = complaints.filter(
            case_number__icontains=search) | complaints.filter(
            title__icontains=search
        )
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(complaints, 10)
    page_number = request.GET.get('page')
    complaints_page = paginator.get_page(page_number)
    
    context = {
        'complaints': complaints_page,
        'total': paginator.count,
    }
    return render(request, 'complaints/list.html', context)


@login_required(login_url='login')
def complaint_detail_view(request, case_number):
    """Display complaint detail."""
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    # Permission check
    if request.user.role == 'user' and complaint.complainant != request.user:
        messages.error(request, 'You do not have permission to view this complaint.')
        return redirect('complaints_list')
    elif request.user.role == 'officer' and complaint.assigned_officer != request.user:
        if request.user.role != 'admin':
            messages.error(request, 'You do not have permission to view this complaint.')
            return redirect('complaints_list')
    
    # Log activity
    ActivityLog.objects.create(
        user=request.user,
        action='view_complaint',
        description=f'Viewed complaint {case_number}',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    
    evidence_files = complaint.evidence_files.all()
    remarks = complaint.remarks.all()
    attachments = complaint.attachments.all()
    
    context = {
        'complaint': complaint,
        'evidence_files': evidence_files,
        'remarks': remarks,
        'attachments': attachments,
    }
    return render(request, 'complaints/detail.html', context)


@login_required(login_url='login')
def new_complaint_view(request):
    """Create a new complaint."""
    if request.user.role != 'user':
        messages.error(request, 'Only regular users can file complaints.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            category = request.POST.get('category')
            priority = 'medium'  # Default priority - users cannot set this
            incident_date = request.POST.get('incident_date')
            incident_location = request.POST.get('incident_location', '')
            affected_system = request.POST.get('affected_system', '')
            
            # Validation
            if not all([title, description, category, incident_date]):
                messages.error(request, 'All required fields must be filled.')
                return render(request, 'complaints/new.html')
            
            # Validate incident date is not in the future
            try:
                incident_datetime = datetime.fromisoformat(incident_date)
                if incident_datetime > datetime.now():
                    messages.error(request, 'Incident date cannot be in the future. Please select a past date and time.')
                    return render(request, 'complaints/new.html')
            except ValueError:
                messages.error(request, 'Invalid date and time format.')
                return render(request, 'complaints/new.html')
            
            # Create complaint
            complaint = Complaint.objects.create(
                complainant=request.user,
                title=title,
                description=description,
                category=category,
                priority=priority,
                incident_date=incident_date,
                incident_location=incident_location,
                affected_system=affected_system
            )
            
            # Handle file uploads
            if 'evidence_files' in request.FILES:
                import hashlib
                for file in request.FILES.getlist('evidence_files'):
                    # Calculate file hash
                    file_hash = hashlib.sha256()
                    for chunk in file.chunks():
                        file_hash.update(chunk)
                    file_hash_hex = file_hash.hexdigest()
                    file.seek(0)  # Reset file pointer
                    
                    Evidence.objects.create(
                        complaint=complaint,
                        file_type=request.POST.get('evidence_type', 'other'),
                        file=file,
                        original_filename=file.name,
                        file_size=file.size,
                        file_hash=file_hash_hex,
                        uploaded_by=request.user
                    )
            
            # Handle attachments (phone, email, URLs, etc.)
            phone_numbers = request.POST.get('phone_numbers', '')
            if phone_numbers:
                for phone in phone_numbers.split(','):
                    if phone.strip():
                        ComplaintAttachment.objects.create(
                            complaint=complaint,
                            attachment_type='phone',
                            value=phone.strip()
                        )
            
            email_addresses = request.POST.get('email_addresses', '')
            if email_addresses:
                for email in email_addresses.split(','):
                    if email.strip():
                        ComplaintAttachment.objects.create(
                            complaint=complaint,
                            attachment_type='email',
                            value=email.strip()
                        )
            
            urls = request.POST.get('urls', '')
            if urls:
                for url in urls.split('\n'):
                    if url.strip():
                        ComplaintAttachment.objects.create(
                            complaint=complaint,
                            attachment_type='url',
                            value=url.strip()
                        )
            
            # Create workflow entry
            CaseWorkflow.objects.create(
                complaint=complaint,
                action='created',
                performed_by=request.user,
                notes='Complaint created by user'
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action='create_complaint',
                description=f'Created complaint {complaint.case_number}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send confirmation email to complainant
            try:
                EmailManager.send_complaint_confirmation(
                    request.user.email,
                    request.user.first_name,
                    complaint.case_number,
                    complaint.title
                )
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
                messages.warning(request, 'Complaint filed successfully, but email notification could not be sent.')
            
            messages.success(request, f'Complaint filed successfully! Case Number: {complaint.case_number}')
            # Redirect to legal info page instead of complaint detail
            return redirect('complaint_legal_info', case_number=complaint.case_number)
        
        except Exception as e:
            messages.error(request, f'Failed to create complaint: {str(e)}')
            return render(request, 'complaints/new.html')
    
    context = {'categories': Complaint.CATEGORY_CHOICES}
    return render(request, 'complaints/new.html', context)


@login_required(login_url='login')
def add_remark_view(request, case_number):
    """Add a remark to a complaint."""
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    # Permission check
    if request.user.role == 'user':
        messages.error(request, 'Only officers and admins can add remarks.')
        return redirect('complaint_detail', case_number=case_number)
    
    if request.method == 'POST':
        try:
            content = request.POST.get('content')
            is_internal = request.POST.get('is_internal') == 'on'
            
            if not content:
                messages.error(request, 'Remark cannot be empty.')
                return redirect('complaint_detail', case_number=case_number)
            
            remark = Remark.objects.create(
                complaint=complaint,
                author=request.user,
                content=content,
                is_internal=is_internal
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action='add_remark',
                description=f'Added remark to case {case_number}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send email notification to complainant if remark is not internal
            if not is_internal:
                try:
                    EmailManager.send_complaint_update(
                        complaint.complainant.email,
                        complaint.complainant.first_name,
                        complaint.case_number,
                        f'A new update has been added to your case by {request.user.get_full_name()}: {content[:200]}...' if len(content) > 200 else f'A new update has been added to your case by {request.user.get_full_name()}: {content}'
                    )
                except Exception as e:
                    print(f"Email sending failed: {str(e)}")
            
            messages.success(request, 'Remark added successfully!')
        
        except Exception as e:
            messages.error(request, f'Failed to add remark: {str(e)}')
    
    return redirect('complaint_detail', case_number=case_number)


@login_required(login_url='login')
def upload_evidence_view(request, case_number):
    """Upload evidence to a complaint."""
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            file_type = request.POST.get('file_type', 'other')
            description = request.POST.get('description', '')
            
            # Calculate file hash for integrity
            import hashlib
            file_hash = hashlib.sha256()
            for chunk in file.chunks():
                file_hash.update(chunk)
            file_hash_hex = file_hash.hexdigest()
            
            # Reset file pointer after reading
            file.seek(0)
            
            evidence = Evidence.objects.create(
                complaint=complaint,
                file_type=file_type,
                file=file,
                original_filename=file.name,
                file_size=file.size,
                file_hash=file_hash_hex,
                uploaded_by=request.user,
                description=description
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action='upload_evidence',
                description=f'Uploaded evidence to case {case_number}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, 'Evidence uploaded successfully!')
        
        except Exception as e:
            messages.error(request, f'Failed to upload evidence: {str(e)}')
    
    return redirect('complaint_detail', case_number=case_number)


@login_required(login_url='login')
def assign_case_view(request, case_number):
    """Assign a case to an officer (admin only)."""
    if request.user.role != 'admin':
        messages.error(request, 'Only admins can assign cases.')
        return redirect('complaint_detail', case_number=case_number)
    
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    if request.method == 'POST':
        try:
            officer_id = request.POST.get('officer_id')
            officer = get_object_or_404(CustomUser, id=officer_id, role='officer')
            
            complaint.assigned_officer = officer
            complaint.status = 'in_progress'
            complaint.save()
            
            # Create workflow entry
            CaseWorkflow.objects.create(
                complaint=complaint,
                action='assigned',
                performed_by=request.user,
                notes=f'Case assigned to {officer.get_full_name()}'
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                action='assign_case',
                description=f'Assigned case {case_number} to {officer.username}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Send notification email to officer
            try:
                EmailManager.send_assignment_notification(
                    officer.email,
                    officer.first_name,
                    complaint.case_number,
                    complaint.title
                )
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
            
            messages.success(request, f'Case assigned to {officer.get_full_name()}!')
        
        except Exception as e:
            messages.error(request, f'Failed to assign case: {str(e)}')
    
    return redirect('complaint_detail', case_number=case_number)


# Import CustomUser for assign_case_view
from users.models import CustomUser
from utils.law_references import get_law_reference


@login_required(login_url='login')
def complaint_legal_info_view(request, case_number):
    """Display legal information related to the complaint."""
    complaint = get_object_or_404(Complaint, case_number=case_number)
    
    # Permission check
    if request.user.role == 'user' and complaint.complainant != request.user:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('complaints_list')
    
    # Get legal information for the complaint category
    legal_info = get_law_reference(complaint.category)
    
    context = {
        'complaint': complaint,
        'legal_info': legal_info,
    }
    
    return render(request, 'complaints/legal_info.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def approve_complaint_view(request, case_number):
    """Approve a complaint (admin only)."""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
    
    try:
        complaint = get_object_or_404(Complaint, case_number=case_number)
        
        complaint.approval_status = 'approved'
        complaint.status = 'approved'
        complaint.approved_by = request.user
        complaint.approval_date = datetime.now()
        complaint.admin_notes = request.POST.get('notes', '')
        complaint.save()
        
        # Create notification
        from .models import AdminNotification
        try:
            AdminNotification.objects.create(
                notification_type='complaint_approved',
                complaint=complaint,
                admin=request.user,
                title=f'Complaint {case_number} Approved',
                message=f'You have approved complaint {case_number}: {complaint.title}'
            )
        except Exception as notification_error:
            print(f"❌ AdminNotification creation failed: {str(notification_error)}")
            import traceback
            traceback.print_exc()
        
        # Send email to complainant
        try:
            EmailManager.send_complaint_update(
                complaint.complainant.email,
                complaint.complainant.first_name,
                case_number,
                f'Your complaint has been approved and is now being processed.'
            )
        except Exception as email_error:
            print(f"❌ Email notification failed: {str(email_error)}")
            import traceback
            traceback.print_exc()
        
        # Log activity
        try:
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Approved complaint {case_number}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        except Exception as log_error:
            print(f"❌ ActivityLog creation failed: {str(log_error)}")
            import traceback
            traceback.print_exc()
        
        return JsonResponse({'success': True, 'message': f'Complaint {case_number} approved successfully'})
    
    except Exception as e:
        print(f"❌ Approve complaint error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='login')
@require_http_methods(["POST"])
def reject_complaint_view(request, case_number):
    """Reject a complaint with reason (admin only)."""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
    
    try:
        complaint = get_object_or_404(Complaint, case_number=case_number)
        reason = request.POST.get('reason', 'Complaint rejected by admin')
        
        complaint.approval_status = 'rejected'
        complaint.status = 'rejected'
        complaint.approved_by = request.user
        complaint.approval_date = datetime.now()
        complaint.admin_notes = reason
        complaint.save()
        
        # Create notification
        from .models import AdminNotification
        try:
            AdminNotification.objects.create(
                notification_type='complaint_rejected',
                complaint=complaint,
                admin=request.user,
                title=f'Complaint {case_number} Rejected',
                message=f'You have rejected complaint {case_number}: {complaint.title}'
            )
        except Exception as notification_error:
            print(f"❌ AdminNotification creation failed: {str(notification_error)}")
            import traceback
            traceback.print_exc()
        
        # Send email to complainant with reason
        try:
            EmailManager.send_complaint_update(
                complaint.complainant.email,
                complaint.complainant.first_name,
                case_number,
                f'Your complaint has been rejected. Reason: {reason}'
            )
        except Exception as email_error:
            print(f"❌ Email notification failed: {str(email_error)}")
            import traceback
            traceback.print_exc()
        
        # Log activity
        try:
            ActivityLog.objects.create(
                user=request.user,
                action='other',
                description=f'Rejected complaint {case_number}: {reason}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        except Exception as log_error:
            print(f"❌ ActivityLog creation failed: {str(log_error)}")
            import traceback
            traceback.print_exc()
        
        return JsonResponse({'success': True, 'message': f'Complaint {case_number} rejected'})
    
    except Exception as e:
        print(f"❌ Reject complaint error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='login')
def get_pending_complaints_api(request):
    """API endpoint to get pending complaints for admin (JSON)."""
    if request.user.role != 'admin':
        return JsonResponse({'success': False, 'message': 'Access denied'}, status=403)
    
    pending_complaints = Complaint.objects.filter(approval_status='pending_approval').order_by('-created_at')[:5]
    
    data = {
        'pending_count': pending_complaints.count(),
        'complaints': [
            {
                'case_number': c.case_number,
                'title': c.title,
                'complainant': c.complainant.get_full_name(),
                'category': c.get_category_display(),
                'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'description': c.description[:100] + '...' if len(c.description) > 100 else c.description,
            }
            for c in pending_complaints
        ]
    }
    
    return JsonResponse(data)


@login_required(login_url='login')
def download_complaint_pdf(request, case_number):
    """Download complaint details as PDF."""
    try:
        complaint = get_object_or_404(Complaint, case_number=case_number)
        
        # Permission check
        if request.user.role == 'user' and complaint.complainant != request.user:
            messages.error(request, 'You do not have permission to download this file.')
            return redirect('complaints_list')
        
        # Generate PDF
        pdf_buffer = ComplaintPDFGenerator.generate_complaint_pdf(complaint, include_evidence=True)
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='export_report',
            description=f'Downloaded PDF for complaint {case_number}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        # Return PDF as attachment
        response = FileResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="complaint_{case_number}.pdf"'
        return response
    
    except Exception as e:
        messages.error(request, f'Error generating PDF: {str(e)}')
        return redirect('complaint_detail', case_number=case_number)
