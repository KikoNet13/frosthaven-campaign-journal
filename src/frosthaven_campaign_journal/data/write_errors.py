from __future__ import annotations


class FirestoreWriteError(Exception):
    """Base error for Firestore write operations."""


class FirestoreConflictError(FirestoreWriteError):
    """Concurrent/base-obsoleta conflict; caller should refresh and retry."""


class FirestoreValidationError(FirestoreWriteError):
    """Domain validation error; caller should fix the action locally."""


class FirestoreTransitionInvalidError(FirestoreWriteError):
    """Invalid state transition; caller should show local error."""

