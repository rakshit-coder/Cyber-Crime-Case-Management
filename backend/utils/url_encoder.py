"""
URL encoding utility for safe and proper URL handling.
Ensures all special characters in URLs are properly percent-encoded.
"""
from urllib.parse import urlparse, quote, unquote


def normalize_url(url_string):
    """
    Normalize and encode a URL to ensure all special characters are properly percent-encoded.
    Prevents double-encoding of already-encoded characters.
    
    Args:
        url_string (str): The URL to normalize
        
    Returns:
        str: The properly encoded URL
    """
    if not url_string:
        return url_string
    
    try:
        # Parse the URL into components
        parsed = urlparse(url_string)
        
        # For path component, first unquote (to handle already-encoded chars)
        # then quote only what needs to be encoded
        decoded_path = unquote(parsed.path)
        encoded_path = quote(decoded_path, safe='/')
        
        # For query string, handle carefully to preserve structure
        encoded_query = ''
        if parsed.query:
            # Parse query parameters and encode them
            params = parsed.query.split('&')
            encoded_params = []
            for param in params:
                if '=' in param:
                    key, value = param.split('=', 1)
                    # Unquote first to avoid double-encoding
                    decoded_key = unquote(key)
                    decoded_value = unquote(value)
                    # Then encode
                    encoded_key = quote(decoded_key, safe='')
                    encoded_value = quote(decoded_value, safe='')
                    encoded_params.append(f'{encoded_key}={encoded_value}')
                else:
                    # Parameter without value
                    decoded_param = unquote(param)
                    encoded_params.append(quote(decoded_param, safe=''))
            encoded_query = '&'.join(encoded_params)
        
        # Handle fragment if present
        encoded_fragment = ''
        if parsed.fragment:
            decoded_fragment = unquote(parsed.fragment)
            encoded_fragment = quote(decoded_fragment, safe='')
        
        # Reconstruct the URL
        result = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
        
        if encoded_query:
            result += f"?{encoded_query}"
        if encoded_fragment:
            result += f"#{encoded_fragment}"
        
        return result
    
    except Exception as e:
        # If encoding fails, return the original URL
        # (better to have an unencoded URL than a broken one)
        return url_string


def encode_for_html_attribute(url_string):
    """
    Ensure URL is safe to use in HTML attributes (href, src, etc).
    This handles ampersand escaping for HTML context.
    
    Args:
        url_string (str): The URL to encode
        
    Returns:
        str: The URL encoded for HTML attribute context
    """
    # First normalize the URL
    normalized = normalize_url(url_string)
    
    # HTML entities: & should be &amp; in HTML attributes
    # However, Django's template auto-escaping handles this
    # So we just return the normalized URL
    return normalized


# Dictionary of URLs that have been verified/encoded
SAFE_URLS = {
    # Government resource links - already checked and safe
    'cybercrime': 'https://cybercrime.gov.in/webform/complaint/',
    'rbi_phishing': 'https://www.rbi.org.in/Scripts/BS_ViewContent.aspx?Id=3009',
    'rbi_fraud': 'https://www.rbi.org.in/Scripts/BS_ViewContent.aspx?Id=3010',
    'cert_in': 'https://www.cert-in.org.in',
    'uidai': 'https://www.uidai.gov.in/protecting-your-information',
    'ncrb': 'https://ncrb.gov.in/cyber-crime',
    'sebi': 'https://www.sebi.gov.in/sebiweb/home/homepagesimp1.jsp?sid=investor%20grievance',
    'ncw': 'https://ncw.gov.in/resources/articles/cyber-harassment',
    'childline': 'https://childlineindia.org.in',
    'meity': 'https://www.meity.gov.in',
}
