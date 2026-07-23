"""
Views for law and article information pages.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.law_references import CYBER_LAW_REFERENCES


def law_index_view(request):
    """Display all cyber crime laws and categories."""
    context = {
        'laws': CYBER_LAW_REFERENCES,
        'categories': list(CYBER_LAW_REFERENCES.keys()),
    }
    return render(request, 'laws/index.html', context)


def law_detail_view(request, category):
    """Display detailed legal information for a specific crime category."""
    if category not in CYBER_LAW_REFERENCES:
        return render(request, 'laws/not_found.html', status=404)
    
    legal_info = CYBER_LAW_REFERENCES[category]
    all_categories = list(CYBER_LAW_REFERENCES.keys())
    
    context = {
        'category': category,
        'legal_info': legal_info,
        'all_categories': all_categories,
    }
    return render(request, 'laws/detail.html', context)
