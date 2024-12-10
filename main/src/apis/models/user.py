from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional



class User(BaseModel):
    name : str
    username: str
    role: str

class UserCredentials(BaseModel):
    username: str
    password: str


class CreateUser(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    username: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password with at least 8 characters")
    role: str = Field(default='user', description="Role assigned to the user (e.g., user, admin)")

    @field_validator("password")
    def validate_password_strength(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        return value
    
class UpdateUser(BaseModel):
    phone: Optional[str] = None
    department: Optional[str] = None
    shift_information: Optional[str] = None
    employee_type: Optional[str] = None
    job_position: Optional[str] = None
    reporting_manager: Optional[str] = None
    work_location: Optional[str] = None
    work_type: Optional[str] = None
    salary: Optional[str] = None
    company: Optional[str] = None
    bank_name: Optional[str] = None
    branch: Optional[str] = None
    bank_address: Optional[str] = None
    bank_code_1: Optional[str] = None
    bank_code_2: Optional[str] = None
    account_number: Optional[str] = None
    bank_country: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
