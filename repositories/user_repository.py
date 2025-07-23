from typing import Optional, Dict, List, Generator
from uuid import UUID

from sqlalchemy.orm import Session
from persistence.decorator import with_session
from persistence.models import User
from sqlalchemy import select
from helpers.converters.user_converter import UserConverter
from repositories.context import Context
from repositories.dto.user_dto import UserDto, ChangePasswordDto

class ORMUserRepository:
    @with_session
    def create(self, user: User, session: Session = None) -> Optional[UUID]:
        try:
            session.add(user)
            return user.id if user else None
        except Exception as e:
            print(e)
            return None
    
    @with_session
    def change_password(self, change_password_dto: ChangePasswordDto, session: Session = None) -> Optional[UUID]:
        try:
            statement = (
                select(User)
                .where(User.id==change_password_dto.id)
            )
            user_to_change = session.scalars(statement).one_or_none()
            if not user_to_change:
                return None
            
            user_to_change.password_hash = change_password_dto.password_hash
            user_to_change.date_updated = change_password_dto.date_updated
            user_to_change.updated_by = change_password_dto.updated_by
            user_to_change.hash_salt = change_password_dto.hash_salt
            return user_to_change.id
        except Exception as e:
            session.rollback()
            print(e)
    
    @with_session
    def get(self, email: Optional[str] = None, id: Optional[UUID] = None, session: Session = None) -> Optional[UserDto]:
        try:
            statement = (
                select(User)
            )
            if email:
                statement = statement.where(User.email==email)
            elif id:
                statement = statement.where(User.id==id)
            else:
                return None               
            user = session.scalars(statement).one_or_none()
            if user:
                return UserConverter.convert_entity_to_dto(user)
            return None
        except Exception as e:
            print(e)
          
    @with_session
    def list(self, session: Session = None) -> List[UserDto]:
        result: List[UserDto] = []
        try:
            statement =(
                select(User)
            )
            users = session.scalars(statement).all()
            for user in users:
                result.append(UserConverter.convert_entity_to_dto(user))
        except Exception as e:
            print(e) 
            
                       
class UserRepository:
    _context: Context

    def __init__(self, context: Context):
        self._context = context

    def create(self, user: User) -> Optional[UUID]:
        try:
            user_dto = UserConverter.convert_entity_to_dto(user)
            query = """INSERT INTO users
                       (id, date_created, created_by, date_updated, updated_by, email, role, password_hash, hash_salt)
                       VALUES (%(id)s, %(date_created)s, %(created_by)s, %(date_updated)s, %(updated_by)s,
                               %(email)s, %(role)s, %(password_hash)s, %(hash_salt)s)"""
            row_count = self._context.execute(query, user_dto)
            return user.id if row_count > 0 else None
        except Exception as e:
            print(e)
            return None

    def change_password(self, user_id: UUID, change_password_dto: ChangePasswordDto) -> Optional[UUID]:
        try:
            query = f"""UPDATE users SET date_updated = (%(date_updated)s), updated_by = %(updated_by)s,
                                password_hash = %(password_hash)s, hash_salt = %(hash_salt)s WHERE id = %(id)s"""
            params = {
                'id': user_id,
                'date_updated': change_password_dto.date_updated,
                'updated_by': change_password_dto.updated_by,
                'password_hash': change_password_dto.password_hash,
                'hash_salt': change_password_dto.hash_salt
            }
            row_count = self._context.execute(query, params)
            return params["id"] if row_count > 0 else None
        except Exception as e:
            print(e)
            return None

    def get(self, email: Optional[str] = None, id: Optional[UUID] = None) -> Optional[User]:
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
            # check if any parameter was provided
            if query == "" or params == {}:
                return None
            data: Dict = self._context.get(query, params)
            if data is None:
                return None
            user = UserDto(
                id=data.get('id'),
                date_created=data.get('date_created'),
                created_by=data.get('created_by', None),
                date_updated=data.get('date_updated', None),
                updated_by=data.get('updated_by', None),
                email=data.get('email'),
                password_hash=data.get('password_hash'),
                hash_salt=data.get('hash_salt'),
                role=data.get('role')
            )
            return UserConverter.convert_dto_entity(user)
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
                    date_updated=item.get('date_updated', None),
                    role=item.get('role'),
                ))
            return users
        except Exception as e:
            print(e)
            return users
