"""
AI Hospital Receptionist System - Patient Model
High-performance, production-ready SQLAlchemy model
"""

import re
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    DateTime,
    Boolean,
    Enum,
    JSON,
    Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from backend.database.db import Base

# ----------------------------
# Constants
# ----------------------------
GENDER_TYPES = ("male", "female", "other")

# ----------------------------
# Patient Model
# ----------------------------
class Patient(Base):
    __tablename__ = "patients"

    # ----------------------------
    # Primary Identity
    # ----------------------------
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # ----------------------------
    # Basic Info
    # ----------------------------
    first_name = Column(String(100), nullable=False, index=True)
    last_name = Column(String(100), nullable=True, index=True)
    gender = Column(Enum(*GENDER_TYPES, name="gender_enum"), nullable=True)

    date_of_birth = Column(Date, nullable=True)

    # ----------------------------
    # Contact Info
    # ----------------------------
    email = Column(String(255), unique=True, nullable=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)

    address = Column(String(255), nullable=True)

    # ----------------------------
    # Medical Data
    # ----------------------------
    blood_group = Column(String(5), nullable=True, index=True)
    allergies = Column(String(255), nullable=True)
    chronic_conditions = Column(String(255), nullable=True)

    # Flexible JSON storage (AI / medical notes / history)
    medical_history = Column(JSON, nullable=True)

    # ----------------------------
    # System Fields
    # ----------------------------
    is_active = Column(Boolean, default=True, index=True)
    is_deleted = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ----------------------------
    # Indexing for performance
    # ----------------------------
    __table_args__ = (
        Index("idx_patient_fullname", "first_name", "last_name"),
        Index("idx_patient_contact", "email", "phone"),
    )

    # ----------------------------
    # Validators
    # ----------------------------
    @validates("email")
    def validate_email(self, key, value):
        if value is None:
            return value
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value.lower()

    @validates("phone")
    def validate_phone(self, key, value):
        if value is None:
            return value
        pattern = r"^[0-9]{10,15}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid phone number")
        return value

    @validates("gender")
    def validate_gender(self, key, value):
        if value is None:
            return value
        if value not in GENDER_TYPES:
            raise ValueError(f"Gender must be one of {GENDER_TYPES}")
        return value

    # ----------------------------
    # Utility Methods
    # ----------------------------
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    def age(self):
        if not self.date_of_birth:
            return None
        today = datetime.utcnow().date()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False

    def to_dict(self):
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name(),
            "gender": self.gender,
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "age": self.age(),
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "blood_group": self.blood_group,
            "allergies": self.allergies,
            "chronic_conditions": self.chronic_conditions,
            "medical_history": self.medical_history,
            "is_active": self.is_active,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

    # ----------------------------
    # Representation
    # ----------------------------
    def __repr__(self):
        return f"<Patient {self.full_name()} | {self.id}>"