"""
Security utilities for encryption, hashing, and integrity verification.
"""
import hashlib
import bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
from django.conf import settings


class PasswordManager:
    """Handles password hashing and verification using bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its bcrypt hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


class EncryptionManager:
    """Handles AES-256 encryption and decryption for sensitive data."""
    
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """Derive a 256-bit key from password using PBKDF2."""
        return PBKDF2(password, salt, dkLen=32, count=100000)
    
    @staticmethod
    def encrypt_data(plaintext: str, key: str = None) -> str:
        """
        Encrypt plaintext using AES-256 in CBC mode.
        Returns base64 encoded string: salt+iv+ciphertext
        """
        if key is None:
            key = settings.ENCRYPTION_KEY
        
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        derived_key = EncryptionManager._derive_key(key, salt)
        
        cipher = AES.new(derived_key, AES.MODE_CBC, iv)
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Add PKCS7 padding
        padding_length = 16 - (len(plaintext_bytes) % 16)
        padded_plaintext = plaintext_bytes + bytes([padding_length] * padding_length)
        
        ciphertext = cipher.encrypt(padded_plaintext)
        
        # Combine salt, iv, and ciphertext
        encrypted_data = salt + iv + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    @staticmethod
    def decrypt_data(encrypted_text: str, key: str = None) -> str:
        """
        Decrypt base64 encoded encrypted data using AES-256.
        """
        if key is None:
            key = settings.ENCRYPTION_KEY
        
        encrypted_data = base64.b64decode(encrypted_text.encode('utf-8'))
        
        # Extract salt, iv, and ciphertext
        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        
        derived_key = EncryptionManager._derive_key(key, salt)
        cipher = AES.new(derived_key, AES.MODE_CBC, iv)
        
        padded_plaintext = cipher.decrypt(ciphertext)
        
        # Remove PKCS7 padding
        padding_length = padded_plaintext[-1]
        plaintext = padded_plaintext[:-padding_length]
        
        return plaintext.decode('utf-8')


class IntegrityManager:
    """Handles SHA-256 hashing for integrity verification."""
    
    @staticmethod
    def calculate_hash(data: str) -> str:
        """Calculate SHA-256 hash of data."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    @staticmethod
    def verify_hash(data: str, hash_value: str) -> bool:
        """Verify data against its SHA-256 hash."""
        return IntegrityManager.calculate_hash(data) == hash_value
    
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
