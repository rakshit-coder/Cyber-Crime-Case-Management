"""
SMS notification service for user updates.
Supports multiple SMS providers: Twilio, AWS SNS, Indian SMS gateways, etc.
"""
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)


class SMSNotificationService:
    """
    Send SMS notifications to users about complaint status changes.
    Supports:
    - Twilio
    - AWS SNS
    - Textlocal (Indian provider)
    - Custom HTTP SMS gateway
    """
    
    @staticmethod
    def send_sms(phone_number: str, message: str) -> bool:
        """
        Send SMS notification to user.
        
        Args:
            phone_number: Recipient phone number (10 digits, Indian format)
            message: SMS message content (max 160 characters)
        
        Returns:
            bool: True if SMS sent successfully, False otherwise
        """
        
        # Get SMS provider from settings
        sms_provider = getattr(settings, 'SMS_PROVIDER', 'twilio')
        
        try:
            if sms_provider == 'twilio':
                return SMSNotificationService._send_via_twilio(phone_number, message)
            elif sms_provider == 'textlocal':
                return SMSNotificationService._send_via_textlocal(phone_number, message)
            elif sms_provider == 'custom':
                return SMSNotificationService._send_via_custom_gateway(phone_number, message)
            else:
                logger.warning(f"Unknown SMS provider: {sms_provider}")
                return False
        
        except Exception as e:
            logger.error(f"SMS sending failed: {str(e)}")
            return False
    
    @staticmethod
    def _send_via_twilio(phone_number: str, message: str) -> bool:
        """Send SMS via Twilio (requires twilio Python SDK)."""
        try:
            from twilio.rest import Client
            
            account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
            auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
            from_number = getattr(settings, 'TWILIO_FROM_NUMBER', '')
            
            if not all([account_sid, auth_token, from_number]):
                logger.error("Twilio credentials not configured")
                return False
            
            client = Client(account_sid, auth_token)
            message_obj = client.messages.create(
                body=message,
                from_=from_number,
                to=f"+91{phone_number}" if not phone_number.startswith('+') else phone_number
            )
            
            logger.info(f"SMS sent successfully via Twilio: {message_obj.sid}")
            return True
        
        except ImportError:
            logger.error("Twilio SDK not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            logger.error(f"Twilio SMS error: {str(e)}")
            return False
    
    @staticmethod
    def _send_via_textlocal(phone_number: str, message: str) -> bool:
        """Send SMS via Textlocal (Indian SMS gateway)."""
        try:
            api_key = getattr(settings, 'TEXTLOCAL_API_KEY', '')
            sender_id = getattr(settings, 'TEXTLOCAL_SENDER_ID', '')
            
            if not api_key:
                logger.error("Textlocal API key not configured")
                return False
            
            url = "https://api.textlocal.in/send/"
            params = {
                'apikey': api_key,
                'numbers': phone_number,
                'message': message,
                'sender': sender_id or 'INDIG0V'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('status') == 'success':
                logger.info(f"SMS sent successfully via Textlocal: {phone_number}")
                return True
            else:
                logger.error(f"Textlocal SMS failed: {result.get('error', 'Unknown error')}")
                return False
        
        except Exception as e:
            logger.error(f"Textlocal SMS error: {str(e)}")
            return False
    
    @staticmethod
    def _send_via_custom_gateway(phone_number: str, message: str) -> bool:
        """Send SMS via custom HTTP gateway."""
        try:
            gateway_url = getattr(settings, 'SMS_GATEWAY_URL', '')
            gateway_user = getattr(settings, 'SMS_GATEWAY_USER', '')
            gateway_password = getattr(settings, 'SMS_GATEWAY_PASSWORD', '')
            
            if not gateway_url:
                logger.error("SMS gateway URL not configured")
                return False
            
            payload = {
                'user': gateway_user,
                'password': gateway_password,
                'phone': phone_number,
                'message': message
            }
            
            response = requests.post(gateway_url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"SMS sent successfully via custom gateway: {phone_number}")
            return True
        
        except Exception as e:
            logger.error(f"Custom SMS gateway error: {str(e)}")
            return False
    
    @staticmethod
    def send_complaint_status_update(user_phone: str, case_number: str, status: str) -> bool:
        """
        Send complaint status update SMS to user.
        
        Args:
            user_phone: User's phone number
            case_number: Complaint case number
            status: New complaint status
        
        Returns:
            bool: True if SMS sent successfully
        """
        
        status_messages = {
            'pending': f'Your cyber crime complaint {case_number} is under review. We will update you soon.',
            'approved': f'Great! Your complaint {case_number} has been approved and assigned to an officer.',
            'assigned': f'Your complaint {case_number} has been assigned to a cybercrime officer.',
            'in_progress': f'Investigation on your complaint {case_number} is in progress. More info soon.',
            'near_to_close': f'Your case {case_number} is near closure. Final update coming soon.',
            'closed': f'Your complaint {case_number} has been closed. Thank you for reporting.',
            'rejected': f'Your complaint {case_number} was not approved. Contact support for details.'
        }
        
        message = status_messages.get(status, f'Update on complaint {case_number}')
        message = message[:160]  # SMS character limit
        
        return SMSNotificationService.send_sms(user_phone, message)
    
    @staticmethod
    def send_verification_code(phone_number: str, code: str) -> bool:
        """Send verification/OTP code via SMS."""
        message = f"Your cyber crime portal verification code is: {code}. Valid for 10 minutes."
        return SMSNotificationService.send_sms(phone_number, message)
    
    @staticmethod
    def send_urgent_alert(phone_number: str, alert_message: str) -> bool:
        """Send urgent alert SMS to admin or officer."""
        urgent_message = f"URGENT ALERT: {alert_message[:140]}"
        return SMSNotificationService.send_sms(phone_number, urgent_message)


# Settings needed in .env for SMS integration:
"""
# SMS Configuration (.env)
SMS_PROVIDER=textlocal  # Options: twilio, textlocal, custom

# For Twilio:
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890

# For Textlocal:
TEXTLOCAL_API_KEY=your_api_key
TEXTLOCAL_SENDER_ID=INDIG0V

# For Custom Gateway:
SMS_GATEWAY_URL=https://your-sms-provider.com/api/send
SMS_GATEWAY_USER=your_username
SMS_GATEWAY_PASSWORD=your_password
"""
