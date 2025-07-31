# auth_service/database.py

# In-memory storage for users and sessions. This file replaces the SQLAlchemy-
# based implementation to remove the dependency on PostgreSQL and ORM.

from typing import Dict, Any, Iterable

# Global in-memory storage for user objects, keyed by user id.
_USERS: Dict[int, Any] = {}
_NEXT_ID: int = 1

class MemorySession:
    """
    Simple in-memory session to mimic the minimal interface of SQLAlchemy's Session.
    """
    def query(self, model: Any) -> Iterable:
        # Return all stored objects for the given model.
        # As we only store User objects, ignore the model parameter.
        return list(_USERS.values())

    def add(self, obj: Any) -> None:
        global _NEXT_ID
        # Assign a new id if necessary and store the object.
        if getattr(obj, "id", None) is None:
            obj.id = _NEXT_ID
            _NEXT_ID += 1
        _USERS[obj.id] = obj

    def commit(self) -> None:
        # Nothing to do for in-memory storage.
        pass

    def refresh(self, obj: Any) -> None:
        # Refresh is a no-op in this simple implementation.
        pass

    def delete(self, obj: Any) -> None:
        # Remove the object from storage.
        if getattr(obj, "id", None) is not None:
            _USERS.pop(obj.id, None)

    def close(self) -> None:
        # No resources to release.
        pass

# SessionLocal points to our in-memory session class.
SessionLocal = MemorySession

# Base is kept for compatibility but unused here.
Base = object

def init_db(retries: int = 1, delay: float = 0.0) -> None:
    """
    No-op database initializer. Included for compatibility with the original signature.
    """
    return None
