from typing import Union, Optional

from entities.entity import Entity


class User(Entity):
    def __init__(self, created_by: Optional[str], email: str, password_hash: str, hash_salt: str):
        super().__init__(created_by)
        self.email = email
        self.password_hash = password_hash
        self.hash_salt = hash_salt