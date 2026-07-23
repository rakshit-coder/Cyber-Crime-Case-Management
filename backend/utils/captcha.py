"""
CAPTCHA implementation for form security.
Code-based CAPTCHA with image generation.
"""
import random
import string
import io
import base64
from django.utils.translation import gettext as _

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class CodeCaptcha:
    """
    Code-based CAPTCHA for form submissions.
    Generates distorted alphanumeric codes for user verification.
    """
    
    # CAPTCHA configuration
    WIDTH = 200
    HEIGHT = 80
    CODE_LENGTH = 6
    FONT_SIZE = 40
    
    @staticmethod
    def generate_captcha():
        """
        Generate a CAPTCHA code and image.
        
        Returns:
            dict: {
                'code': 'ABC123',
                'image_base64': 'data:image/png;base64,...',
                'code_hash': 'hashed_value_of_code'
            }
        """
        # Generate random alphanumeric code (uppercase + digits, no confusing chars)
        valid_chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'  # Exclude 0,1,I,O,L for clarity
        code = ''.join(random.choice(valid_chars) for _ in range(CodeCaptcha.CODE_LENGTH))
        
        # Create hash of the code for verification
        from hashlib import sha256
        import time
        
        timestamp = int(time.time() / 60)  # 60-second window
        code_data = f'{code}_{timestamp}'
        code_hash = sha256(code_data.encode()).hexdigest()
        
        # Generate image
        image_base64 = CodeCaptcha._generate_image(code)
        
        return {
            'code': code,
            'code_hash': code_hash,
            'image_base64': image_base64,
            'timestamp': timestamp
        }
    
    @staticmethod
    def _generate_image(code):
        """
        Generate CAPTCHA image with distorted text.
        
        Args:
            code (str): The CAPTCHA code to display
            
        Returns:
            str: Base64 encoded PNG image data URI
        """
        if not PILLOW_AVAILABLE:
            # Fallback: return a simple HTML representation
            return CodeCaptcha._get_fallback_image(code)
        
        try:
            # Create image with white background
            img = Image.new('RGB', (CodeCaptcha.WIDTH, CodeCaptcha.HEIGHT), color='white')
            draw = ImageDraw.Draw(img)
            
            # Add background noise (random lines)
            for _ in range(10):
                x1 = random.randint(0, CodeCaptcha.WIDTH)
                y1 = random.randint(0, CodeCaptcha.HEIGHT)
                x2 = random.randint(0, CodeCaptcha.WIDTH)
                y2 = random.randint(0, CodeCaptcha.HEIGHT)
                color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
            
            # Add noise dots
            for _ in range(50):
                x = random.randint(0, CodeCaptcha.WIDTH)
                y = random.randint(0, CodeCaptcha.HEIGHT)
                color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
                draw.point((x, y), fill=color)
            
            # Try to use a default font, fallback to default if not available
            try:
                # Try to find a system font
                font = ImageFont.truetype("arial.ttf", CodeCaptcha.FONT_SIZE)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", CodeCaptcha.FONT_SIZE)
                except:
                    # Use default font
                    font = ImageFont.load_default()
            
            # Draw CAPTCHA text with random rotation and distortion
            text_color = (50, 50, 100)  # Dark blue
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), code, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (CodeCaptcha.WIDTH - text_width) // 2
            y = (CodeCaptcha.HEIGHT - text_height) // 2
            
            draw.text((x, y), code, fill=text_color, font=font)
            
            # Apply filters for distortion
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            
            # Add border
            border_color = (100, 100, 150)
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (CodeCaptcha.WIDTH - 1, CodeCaptcha.HEIGHT - 1)], outline=border_color, width=2)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return f'data:image/png;base64,{img_base64}'
        
        except Exception as e:
            # Fallback if image generation fails
            return CodeCaptcha._get_fallback_image(code)
    
    @staticmethod
    def _get_fallback_image(code):
        """
        Generate a simple SVG fallback CAPTCHA when PIL is not available.
        
        Args:
            code (str): The CAPTCHA code to display
            
        Returns:
            str: Data URI for SVG image
        """
        svg = f'''<svg width="200" height="80" xmlns="http://www.w3.org/2000/svg">
            <rect width="200" height="80" fill="white" stroke="#646496" stroke-width="2"/>
            <text x="100" y="50" font-family="Arial, sans-serif" font-size="40" 
                  font-weight="bold" text-anchor="middle" fill="#323264" 
                  opacity="0.8" letter-spacing="2">{code}</text>
            <line x1="20" y1="30" x2="80" y2="50" stroke="#ddd" stroke-width="1" opacity="0.5"/>
            <line x1="120" y1="20" x2="180" y2="60" stroke="#ddd" stroke-width="1" opacity="0.5"/>
        </svg>'''
        svg_base64 = base64.b64encode(svg.encode()).decode()
        return f'data:image/svg+xml;base64,{svg_base64}'
    
    @staticmethod
    def verify_captcha(user_code, correct_hash, timestamp):
        """
        Verify the CAPTCHA code.
        
        Args:
            user_code (str): The user's entered code
            correct_hash (str): The correct code hash
            timestamp (int): The CAPTCHA generation timestamp
            
        Returns:
            bool: True if correct, False otherwise
        """
        try:
            from hashlib import sha256
            import time
            
            # Check if CAPTCHA is expired (5 minutes)
            current_timestamp = int(time.time() / 60)
            if current_timestamp - timestamp > 5:
                return False
            
            # Verify code (case-insensitive)
            expected_data = f'{user_code.upper().strip()}_{timestamp}'
            expected_hash = sha256(expected_data.encode()).hexdigest()
            
            return expected_hash == correct_hash
        except:
            return False
    
    @staticmethod
    def verify_captcha_simple(user_code, correct_code):
        """
        Simple CAPTCHA verification without timestamp checking.
        Use this for testing or less critical forms.
        
        Args:
            user_code (str): The user's entered code
            correct_code (str): The correct code
            
        Returns:
            bool: True if correct, False otherwise
        """
        try:
            return str(user_code).strip().upper() == str(correct_code).strip().upper()
        except:
            return False


class PasswordStrengthMeter:
    """
    Additional security: Password strength meter for login attempts.
    Tracks failed login attempts and implements rate limiting.
    """
    
    @staticmethod
    def is_account_locked(username, max_attempts=5, lockout_minutes=15):
        """
        Check if account is locked due to too many failed attempts.
        
        Args:
            username (str): Username
            max_attempts (int): Maximum failed attempts allowed
            lockout_minutes (int): Minutes to lock account
            
        Returns:
            bool: True if account is locked, False otherwise
        """
        from django.core.cache import cache
        from datetime import datetime, timedelta
        
        lock_key = f'login_lock_{username}'
        attempts_key = f'login_attempts_{username}'
        
        # Check if account is locked
        if cache.get(lock_key):
            return True
        
        # Get number of failed attempts
        attempts = cache.get(attempts_key, 0)
        return attempts >= max_attempts
    
    @staticmethod
    def record_failed_attempt(username, max_attempts=5, lockout_minutes=15):
        """
        Record a failed login attempt and potentially lock the account.
        
        Args:
            username (str): Username
            max_attempts (int): Maximum failed attempts allowed
            lockout_minutes (int): Minutes to lock account
        """
        from django.core.cache import cache
        from datetime import datetime, timedelta
        
        attempts_key = f'login_attempts_{username}'
        lock_key = f'login_lock_{username}'
        
        # Increment failed attempts
        attempts = cache.get(attempts_key, 0) + 1
        cache.set(attempts_key, attempts, 60 * lockout_minutes)
        
        # Lock account if max attempts exceeded
        if attempts >= max_attempts:
            cache.set(lock_key, True, 60 * lockout_minutes)
    
    @staticmethod
    def reset_failed_attempts(username):
        """
        Reset failed login attempts on successful login.
        
        Args:
            username (str): Username
        """
        from django.core.cache import cache
        
        attempts_key = f'login_attempts_{username}'
        lock_key = f'login_lock_{username}'
        
        cache.delete(attempts_key)
        cache.delete(lock_key)


# Default CAPTCHA settings (can be overridden in Django settings)
CAPTCHA_SETTINGS = {
    'ENABLED': True,  # Enable/disable CAPTCHA
    'TYPE': 'code',  # 'code' based CAPTCHA
    'CODE_LENGTH': 6,  # Length of CAPTCHA code
    'CODE_CAPTCHA_TIMEOUT': 300,  # 5 minutes in seconds
    'FAILED_LOGIN_THRESHOLD': 5,  # Attempts before account lockout
    'LOCKOUT_DURATION': 15,  # Minutes
}
