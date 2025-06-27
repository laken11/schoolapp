import dataclasses
from typing import Optional

@dataclasses.dataclass
class BaseResponse:
    status: bool
    message: Optional[str]