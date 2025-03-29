from game.errors import *
from enum import Enum


class LogicEvents(Enum):
    EMPTY_DECK: int = 0
    PEEK_EFFECT: int = 1
    SPY_EFFECT: int = 2
    SWAP_EFFECT: int = 3
    CABO: int = 4


class LogicEvent:
    def __init__(self, eid: int, kind: LogicEvents, data=None):
        assertion.assert_types(eid, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_type(kind, LogicEvents, ArgumentCodes, code=ArgumentCodes.NOT_LOGIC_EVENTS)
        assertion.assert_is_positiv(eid, ArgumentError, code=ArgumentCodes.NOT_POSITIV)
        self._kind: LogicEvents = kind
        self._eid: int = eid
        self._data = data

    def get_eid(self) -> int:
        return self._eid

    def get_kind(self) -> LogicEvents:
        return self._kind

    def get_data(self):
        return self._data


class LogicEventHandler:
    def __init__(self):
        self._events: list = list()
        self._ids: int = 0

    def add_event(self, event: LogicEvents, data=None) -> None:
        assertion.assert_type(event, LogicEvents, ArgumentCodes, code=ArgumentCodes.NOT_LOGIC_EVENTS)
        self._events.append(LogicEvent(self._ids, event, data))
        self._ids += 1

    def get_events(self) -> list:
        return [*self._events]

    def remove_event(self, event_id: int) -> None:
        assertion.assert_types(event_id, Types.INT.value, ArgumentError, code=ArgumentCodes.NOT_INT)
        assertion.assert_below(event_id, self._ids, ArgumentError, code=ArgumentCodes.TOO_BIG)
        c = list()
        for event in self._events:
            if event.get_eid() == event_id:
                continue
            c.append(event)
        self._events = [*c]

    def get_event_by_kind(self, kind: LogicEvents) -> LogicEvent | None:
        assertion.assert_type(kind, LogicEvents, ArgumentError, code=ArgumentCodes.NOT_LOGIC_EVENTS)
        if not self.has_event(kind): return None
        for event in self._events:
            if event.get_kind() == kind:
                return event

    def remove_event_by_kind(self, kind: LogicEvents) -> None:
        assertion.assert_type(kind, LogicEvents, ArgumentError, code=ArgumentCodes.NOT_LOGIC_EVENTS)
        event: LogicEvent | None = self.get_event_by_kind(kind)
        if event is None: return
        self.remove_event(event.get_eid())

    def clear_events(self) -> None:
        self._events = list()

    def has_event(self, kind: LogicEvents) -> bool:
        assertion.assert_type(kind, LogicEvents, ArgumentError, code=ArgumentCodes.NOT_LOGIC_EVENTS)
        return any([event.get_kind() == kind for event in self._events])

    def __iter__(self):
        return self._events

    def __next__(self):
        if len(self._events) > 0:
            return self._events.pop(0)
        raise StopIteration
