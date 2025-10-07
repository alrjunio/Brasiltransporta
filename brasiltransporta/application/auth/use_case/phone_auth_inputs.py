from dataclasses import dataclass
from typing import Optional

@dataclass
class SendPhoneVerificationCodeCommand:
    phone: str

@dataclass  
class VerifyPhoneCodeCommand:
    phone: str
    code: str

@dataclass
class PhoneLoginCommand:
    phone: str
    code: str