"""
URL configuration for secure_case_connect project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('i18n/setlang/', set_language, name='set_language'),  # Explicit language setter
    path('api/users/', include('users.urls')),
    path('api/complaints/', include('complaints.urls')),
    path('api/cases/', include('cases.urls')),
]

# Wrap main URL patterns with i18n for language prefixes
urlpatterns += i18n_patterns(
    path('', include('users.urls')),
    path('complaints/', include('complaints.urls')),
    path('cases/', include('cases.urls')),
    path('laws/', include('laws.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
