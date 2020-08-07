from enum import Enum
from typing import Tuple


class Content(Enum):
    characters = "characters"
    pages = "pages"

    @classmethod
    def all(cls) -> Tuple[str]:
        return tuple(map(lambda c: c.value, cls))

    @staticmethod
    def from_str(v: str) -> "Content":
        for content in Content:
            if content.value == v:
                return content
        raise ValueError(f"invalid value: {v}")


class Annotation(Enum):
    body = "body"
    face = "face"
    frame = "frame"
    text = "text"

    @classmethod
    def all(cls) -> Tuple[str]:
        return tuple(map(lambda c: c.value, cls))

    @staticmethod
    def from_str(v: str) -> "Annotation":
        for content in Annotation:
            if content.value == v:
                return content
        raise ValueError(f"invalid value: {v}")
