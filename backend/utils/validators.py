"""
Custom validators for input validation and password enforcement.
"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re


class CERTINPasswordValidator:
    """
    Validate password according to CERT-IN government portal guidelines.
    Password must be 16-21 characters long.
    Must contain uppercase, lowercase, digits, and special characters.
    """
    
    def validate(self, password, user=None):
        """Validate password according to CERT-IN standards."""
        # Check length (16-21 characters as per CERT-IN guidelines)
        if len(password) < 16:
            raise ValidationError(
                _('Password must be at least 16 characters long (CERT-IN requirement).'),
                code='password_too_short',
            )
        
        if len(password) > 21:
            raise ValidationError(
                _('Password must not exceed 21 characters.'),
                code='password_too_long',
            )
        
        # Check for uppercase letters
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _('Password must contain at least one uppercase letter.'),
                code='password_no_upper',
            )
        
        # Check for lowercase letters
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _('Password must contain at least one lowercase letter.'),
                code='password_no_lower',
            )
        
        # Check for digits
        if not re.search(r'\d', password):
            raise ValidationError(
                _('Password must contain at least one digit.'),
                code='password_no_digit',
            )
        
        # Check for special characters (limited set to prevent injection)
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
            raise ValidationError(
                _('Password must contain at least one special character: !@#$%^&*()_+-=[]{};\':\"",.<>?/\\|`~'),
                code='password_no_special',
            )
        
        # Prevent common patterns
        if re.search(r'(.)\1{2,}', password):  # No 3+ repeated characters
            raise ValidationError(
                _('Password cannot contain 3 or more repeated characters.'),
                code='password_repeated_chars',
            )
    
    def get_help_text(self):
        """Return help text for password requirements."""
        return _(
            'Your password must be 16-21 characters and contain uppercase letters, '
            'lowercase letters, digits, and special characters (!@#$%^&*()_+-=[]{};\':\"",.<>?/\\|`~).'
        )


class InputSanitizer:
    """
    Sanitize user input to prevent injection attacks.
    """
    
    # Blocked characters that could be used in injection attacks
    BLOCKED_CHARS = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '&': '&amp;',
    }
    
    BLOCKED_PATTERNS = [
        r'<script',
        r'javascript:',
        r'onerror=',
        r'onload=',
        r'onclick=',
        r'eval\(',
        r'expression\(',
        r'alert\(',
        r'document\.',
        r'window\.',
    ]
    
    @staticmethod
    def sanitize(text: str, allow_html=False) -> str:
        """
        Sanitize input to prevent XSS and injection attacks.
        
        Args:
            text: Input text to sanitize
            allow_html: If True, preserve HTML (use with caution)
        
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Check for dangerous patterns
        text_lower = text.lower()
        for pattern in InputSanitizer.BLOCKED_PATTERNS:
            if re.search(pattern, text_lower):
                raise ValidationError(
                    _('Input contains potentially dangerous content. Please remove special characters like <>\"\'&'),
                    code='dangerous_input',
                )
        
        # Escape HTML entities if not allowing HTML
        if not allow_html:
            for char, escape in InputSanitizer.BLOCKED_CHARS.items():
                text = text.replace(char, escape)
        
        return text
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format (Indian format)."""
        # Allow 10-13 digits, with optional +, hyphens, spaces
        pattern = r'^\+?[0-9]{10,13}$|^\+?[0-9\s\-()]{10,}$'
        return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None
    
    @staticmethod
    def validate_complaint_text(text: str) -> bool:
        """Validate complaint/description text."""
        if len(text) < 10:
            raise ValidationError(
                _('Description must be at least 10 characters long.'),
                code='text_too_short',
            )
        if len(text) > 5000:
            raise ValidationError(
                _('Description must not exceed 5000 characters.'),
                code='text_too_long',
            )
        return True


class AccessControlValidator:
    """
    Validate and enforce access control policies.
    """
    
    @staticmethod
    def check_user_access(user, resource_owner):
        """Check if user has access to resource."""
        if user.role == 'admin':
            return True  # Admin has access to all
        if user.role == 'officer':
            return True  # Officer can access assigned cases
        # Regular user can only access their own resources
        return user.id == resource_owner.id or user == resource_owner
