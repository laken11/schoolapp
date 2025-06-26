from typing import Optional, Dict, List, Generator
from uuid import UUID

from repositories.context import Context
from repositories.dto.user_dto import UserDto


class UserRepository:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    def create(self, user: UserDto) -> Optional[UUID]:
        try:
            query = f"""INSERT INTO users 
            (id, date_created, created_by, date_updated, updated_by, email, password_hash, hash_salt) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            user_id = self._context.execute(query, user)
            return UUID(str(user_id))
        except Exception as e:
            print(e)
            return None

    def change_password(self, user: UserDto) -> Optional[UUID]:
        try:
            query = f"""UPDATE users SET date_updated = (%(date_updated)s), updated_by = %(updated_by)s),
                                password_hash = %(password_hash)s, hash_salt = %(hash_salt)s WHERE id = %(id)s"""
            params = {
                'id': user.id,
                'date_updated': user.date_updated,
                'updated_by': user.updated_by,
                'password_hash': user.password_hash,
                'hash_salt': user.hash_salt
            }
            user_id = self._context.execute(query, params)
            return UUID(str(user_id))
        except Exception as e:
            print(e)
            return None

    def get(self, email: Optional[str], id: Optional[UUID]) -> Optional[UserDto]:
        query = ""
        params = {}
        try:
            if email:
                query = f"""SELECT * FROM users WHERE email = %(email)s"""
                params = {
                    'email': email
                }
            if id:
                query = f"""SELECT * FROM users WHERE id = %(id)s"""
                params = {
                    'id': id
                }
            if query is "" or params is {}: return None
            data: Dict = self._context.get(query, params)
            user = UserDto(
                id=data.get('id'),
                date_created=data.get('date_created'),
                created_by=data.get('created_by', None),
                date_updated=data.get('date_updated', None),
                updated_by=data.get('updated_by', None),
                email=data.get('email'),
                password_hash=data.get('password_hash'),
                hash_salt=data.get('hash_salt')
            )
            return user
        except Exception as e:
            print(e)

    def list(self) -> List[UserDto]:
        users: List[UserDto] = []
        try:
            query = "SELECT id, email, date_created, created_by, updated_by, date_updated FROM users"
            params = {}
            data: Generator[Dict, None, None] = self._context.get_many(query, params)
            for item in data:
                users.append(UserDto(
                    id=item.get('id'),
                    email=item.get('email'),
                    date_created=item.get('date_created'),
                    created_by=item.get('created_by', None),
                    updated_by=item.get('updated_by', None),
                    date_updated=item.get('date_updated', None)
                ))
            return users
        except Exception as e:
            print(e)
            return users
