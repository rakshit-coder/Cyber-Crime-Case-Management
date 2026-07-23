"""
PDF generation utilities for case files and reports.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime


class ComplaintPDFGenerator:
    """Generate PDF reports for complaints/cases."""
    
    @staticmethod
    def generate_complaint_pdf(complaint, include_evidence=True):
        """
        Generate a PDF document for a complaint.
        
        Args:
            complaint: Complaint model instance
            include_evidence: Include evidence files list
        
        Returns:
            BytesIO object containing the PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0052cc'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#0052cc'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderColor=colors.HexColor('#0052cc'),
            borderWidth=1,
            borderPadding=10,
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
        )
        
        # Title
        title = Paragraph(
            f"Cyber Crime Complaint Report<br/>{complaint.case_number}",
            title_style
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Case Information Section
        elements.append(Paragraph(f"Case Information", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        case_info = [
            ['Case Number:', complaint.case_number],
            ['Title:', complaint.title],
            ['Category:', complaint.get_category_display()],
            ['Status:', complaint.get_status_display()],
            ['Priority:', complaint.get_priority_display()],
            ['Created Date:', complaint.created_at.strftime('%B %d, %Y')],
            ['Last Updated:', complaint.updated_at.strftime('%B %d, %Y')],
        ]
        
        case_table = Table(case_info, colWidths=[2*inch, 4*inch])
        case_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(case_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Complainant Information
        elements.append(Paragraph("Complainant Information", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        complainant_info = [
            ['Name:', complaint.complainant.get_full_name()],
            ['Email:', complaint.complainant.email],
            ['Phone:', complaint.complainant.phone or 'N/A'],
            ['Username:', complaint.complainant.username],
        ]
        
        complainant_table = Table(complainant_info, colWidths=[2*inch, 4*inch])
        complainant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(complainant_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Complaint Description
        elements.append(Paragraph("Complaint Description", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        description = Paragraph(complaint.description, normal_style)
        elements.append(description)
        elements.append(Spacer(1, 0.3*inch))
        
        # Incident Details
        if complaint.incident_date or complaint.incident_location or complaint.affected_system:
            elements.append(Paragraph("Incident Details", heading_style))
            elements.append(Spacer(1, 0.1*inch))
            
            incident_info = []
            if complaint.incident_date:
                incident_info.append(['Incident Date:', complaint.incident_date.strftime('%B %d, %Y')])
            if complaint.incident_location:
                incident_info.append(['Location:', complaint.incident_location])
            if complaint.affected_system:
                incident_info.append(['Affected System:', complaint.affected_system])
            
            if incident_info:
                incident_table = Table(incident_info, colWidths=[2*inch, 4*inch])
                incident_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f4ff')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                elements.append(incident_table)
                elements.append(Spacer(1, 0.3*inch))
        
        # Officer Assignment (if assigned)
        if complaint.assigned_officer:
            elements.append(Paragraph("Assigned Officer", heading_style))
            elements.append(Spacer(1, 0.1*inch))
            
            officer_info = [
                ['Officer Name:', complaint.assigned_officer.get_full_name()],
                ['Badge Number:', complaint.assigned_officer.badge_number or 'N/A'],
                ['Department:', complaint.assigned_officer.department or 'N/A'],
                ['Email:', complaint.assigned_officer.email],
            ]
            
            officer_table = Table(officer_info, colWidths=[2*inch, 4*inch])
            officer_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            elements.append(officer_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Evidence Files (if include_evidence)
        if include_evidence and complaint.evidence_files.exists():
            elements.append(Paragraph("Evidence Files", heading_style))
            elements.append(Spacer(1, 0.1*inch))
            
            evidence_data = [['Type', 'File Name', 'Size (KB)', 'Uploaded']]
            
            for evidence in complaint.evidence_files.all():
                evidence_data.append([
                    evidence.get_file_type_display(),
                    evidence.original_filename[:30],
                    str(round(evidence.file_size / 1024, 2)) + ' KB',
                    evidence.uploaded_at.strftime('%m/%d/%Y')
                ])
            
            evidence_table = Table(evidence_data, colWidths=[1.2*inch, 2.2*inch, 1.2*inch, 1.4*inch])
            evidence_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0052cc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
            ]))
            elements.append(evidence_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Footer with generation date
        elements.append(Spacer(1, 0.2*inch))
        footer_text = f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Indian Cyber Crime Portal"
        footer = Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=TA_CENTER))
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
