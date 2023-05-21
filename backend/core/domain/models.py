"""Domain models for the school management system."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Aluno:
    """Aluno model class for domain layer."""
    id: int | None
    name: str
    born_date: date
    address: str
    tutor_name: str
    tutor_phone: str
    class_shift: str


@dataclass
class Presenca:
    """Presenca model class for domain layer."""
    id: int | None
    aluno_id: int
    status: str
    document: str
    reason_missing_class: str


@dataclass
class Professor:
    """Professor model class for domain layer."""
    id: int | None
    name: str
    email: str # must be unique
    password: str