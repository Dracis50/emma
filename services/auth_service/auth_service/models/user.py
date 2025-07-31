from dataclasses import dataclass, field
import datetime as dt
from typing import Optional

@dataclass
class User:
    """Simple data class to represent a user profile."""
    id: Optional[int] = None
    email: str = ""
    hashed_password: str = ""
    is_active: bool = True
    is_admin: bool = False
    is_premium: bool = False
    created_at: dt.datetime = field(default_factory=dt.datetime.utcnow)
