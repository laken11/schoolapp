from entities.user import User
from repositories.dto.user_dto import UserDto


class UserConverter:

    @staticmethod
    def convert_dto_entity(dto: UserDto) -> User:
        user =  User(
            created_by=dto.created_by,
            email=dto.email,
            password_hash=dto.password_hash,
            hash_salt=dto.hash_salt,
        )
        user.id = dto.id
        user.updated_by = dto.updated_by
        user.date_updated = dto.date_updated
        user.date_created = dto.date_created
        return user


    @staticmethod
    def convert_entity_to_dto(entity: User) -> UserDto:
        user_dto = UserDto(
            created_by=entity.created_by,
            email=entity.email,
            password_hash=entity.password_hash,
            hash_salt=entity.hash_salt,
            id=entity.id,
            updated_by=entity.updated_by,
            date_updated=entity.date_updated,
            date_created=entity.date_created,
        )
        return user_dto