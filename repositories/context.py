import abc
from datetime import date, datetime, timedelta, time
from decimal import Decimal
from typing import Optional, Any, Generator, Dict

from mysql.connector import MySQLConnection


class Context(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_many(self, query: str, param: dict[str, object]) -> Generator[Dict[str, object], None, None]:
        pass

    @abc.abstractmethod
    def get(self, query: str, param: dict[str, object]) -> Dict[str, object]:
        pass

    @abc.abstractmethod
    def execute(self, query: str, param: object) -> object:
        pass


class MySqlDbContext(Context):
    db_connection: Optional[MySQLConnection] = None

    def __init__(self, host: str, database: str, user: str, password: str, port: int = 3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    def create(self, host: str, database: str, user: str, password: str, port: int = 3306):
        self.db_connection = MySQLConnection(host=host, database=database, user=user,
                                             password=password, port=port)

    def get_many(self, query: str, param: dict[str, object]) -> Generator[Dict[str, object], None, None]:
        with self.db_connection.connect() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, param)
                for item in cursor.fetchall():
                    yield item

    def get(self, query: str, param: dict[str, object]) -> Dict[str, object]:
        with self.db_connection.connect() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, param)
                result = cursor.fetchone()
                return result

    def execute(self, query: str, param: object) -> object:
        try:
            with self.db_connection.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, param)
                    last_row_id = cursor.lastrowid
                    connection.commit()
                    return last_row_id
        except Exception as e:
            self.db_connection.rollback()
            raise e