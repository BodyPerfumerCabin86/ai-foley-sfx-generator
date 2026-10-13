"""ModelCache — least-recently-used cache for plugin model weights."""

from __future__ import annotations

from collections import OrderedDict
from typing import Any


class ModelCache:
    def __init__(self, max_entries: int = 4) -> None:
        self._max = max_entries
        self._store: OrderedDict[str, Any] = OrderedDict()

    def get(self, key: str) -> Any | None:
        if key not in self._store:
            return None
        self._store.move_to_end(key)
        return self._store[key]

    def put(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._store.move_to_end(key)
        while len(self._store) > self._max:
            self._store.popitem(last=False)

    def clear(self) -> None:
        self._store.clear()