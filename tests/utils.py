from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


def sublist(lst: list[T], size: int) -> list[list[T]]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def find_project_root():
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / ".git").exists():
            return parent
    return current_path
