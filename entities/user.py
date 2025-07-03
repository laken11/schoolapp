from typing import Union, Optional

from entities.entity import Entity


class User(Entity):
    def __init__(self, email: str,  role: str, password_hash: Optional[str] = None, hash_salt: Optional[str] = None ,created_by: Optional[str] = None):
        super().__init__(created_by)
        self.email = email
        self.password_hash = password_hash
        self.hash_salt = hash_salt
        self.role = role