import datetime
import uuid
from abc import ABC
from typing import Optional, Dict, Any
from uuid import UUID


class Entity(ABC):
    id: UUID
    date_created: datetime
    date_updated: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]

    def __init__(self, created_by: Optional[str]):
        self.id = uuid.uuid4()
        self.date_created = datetime.datetime.now(datetime.UTC)
        self.created_by = created_by
        self.updated_by = None
        self.date_updated = None