from abc import ABCMeta
from typing import Dict, Any, Optional


class ContainerService:
    container: Dict[str, Any] = {}

    @staticmethod
    def get(key: str) -> Optional[Any]:
        if key not in ContainerService.container:
            return None
        return ContainerService.container[key]

    @staticmethod
    def set(key: str, value: Any) -> None:
        ContainerService.container[key] = value

    @staticmethod
    def delete(key: str) -> None:
        del ContainerService.container[key]
