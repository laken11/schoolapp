import abc
from datetime import datetime
from typing import Optional, Generator, Dict, Any
from uuid import UUID

from mysql.connector import MySQLConnection
from mysql.connector import Error

class Context(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_many(self, query: str, param: dict[str, object]) -> Generator[Dict[str, object], None, None]:
        pass

    @abc.abstractmethod
    def get(self, query: str, param: dict[str, object]) -> Dict[str, object]:
        pass

    @abc.abstractmethod
    def execute(self, query: str, param: object) -> int:
        pass


class MySqlDbContext(Context):
    _connection = None

    def __init__(self, host: str, database: str, user: str, password: str, port: int = 3306):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self._connection = MySQLConnection(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            if self._connection.is_connected():
                return self._connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    def get_many(self, query: str, param: dict[str, object]) -> Generator[Dict[str, object], None, None]:
        self.connect()
        with self._connection as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, param)
                for item in cursor.fetchall():
                    yield item

    def get(self, query: str, param: dict[str, object]) -> Optional[Dict[str, object]]:
        self.connect()
        with self._connection as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, param)
                result = cursor.fetchone()
                return result

    def execute(self, query: str, param: object) -> int:
        try:
            self.connect()
            with self._connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, self._to_dict(param))
                    row_count = cursor.rowcount
                    connection.commit()
                    return row_count
        except Exception as e:
            self._connection.rollback()
            raise e

    @staticmethod
    def _to_dict(params: object) -> Dict[str, Any]:
        """Convert dictionary values to MySQL-compatible types"""
        if isinstance(params, dict):
            return params
        params = params.__dict__
        converted = {}
        for key, value in params.items():
            if isinstance(value, UUID):
                converted[key] = str(value)
            elif isinstance(value, datetime):
                converted[key] = value.strftime('%Y-%m-%d %H:%M:%S')
            elif value is None:
                converted[key] = None
            else:
                converted[key] = value
        return converted