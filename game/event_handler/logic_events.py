from game.errors import *
from enum import Enum


class LogicEvents(Enum):
    EMPTY_DECK: int = 0


class LogicEvent:
    def __init__(self, eid: int, kind: LogicEvents):
        self._kind: int = kind
        self._eid: int = eid

    def get_eid(self) -> int:
        return self._eid

    def get_kind(self) -> int:
        return self._kind


class LogicEventHandler:
    def __init__(self):
        self._events: list = list()
        self._ids: int = 0

    def add_event(self, event: LogicEvents) -> None:
        self._events.append(LogicEvent(self._ids, event))
        self._ids += 1

    def get_events(self) -> list:
        return [*self._events]

    def remove_event(self, event_id: int) -> None:
        c = list()
        for event in self._events:
            if event.get_eid() == event_id:
                continue
            c.append(event)
        self._events = [*c]

    def get_event_by_kind(self, kind: LogicEvents) -> LogicEvent | None:
        if not self.has_event(kind): return
        for event in self._events:
            if event.get_kind() == kind:
                return event

    def remove_event_by_kind(self, kind: LogicEvents) -> None:
        event: LogicEvent | None = self.get_event_by_kind(kind)
        if event is None: return
        self.remove_event(event.get_eid())

    def clear_events(self) -> None:
        self._events = list()

    def has_event(self, kind: LogicEvents) -> bool:
        return any([event.get_kind() == kind for event in self._events])