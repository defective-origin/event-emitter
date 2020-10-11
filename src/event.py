from __future__ import annotations
from typing import Callable, List
from .base_event import BaseEvent
from .action import Action, ActionState

class Event(BaseEvent):
    __actions = {}
    __is_enabled = True

    @property
    def is_enabled(self) -> bool:
        """Return True if the event is enabled otherwise False."""
        return self.__is_enabled

    @property
    def is_disabled(self) -> bool:
        """Return True if the event is disabled otherwise False."""
        return not self.__is_enabled

    def on(self, callback: Callable) -> Event:
        """Add unlimited action."""
        return self.once(callback, ActionState.UNLIMITED)

    def once(self, callback: Callable, times: int = ActionState.ONCE) -> Event:
        """Add limited action."""
        self.__actions[callback] = Action(callback, times)
        return self

    def off(self, callback: Callable) -> Event:
        """Remove actions by callback name."""
        if callback in self.__actions:
            del self.__actions[callback]
        return self

    def enable(self) -> Event:
        """Enable the event. After that it can be emitted."""
        self.__is_enabled = True
        return self

    def disable(self) -> Event:
        """Disable the event. After that it can't be emitted."""
        self.__is_enabled = False
        return self

    @staticmethod
    def combine(*events: List[Event]) -> Event:
        """Combine several events to one"""
        new_event = Event()
        for event in events:
            new_event.__actions = {**new_event.__actions, **event.__actions}
        return new_event

    async def emit(self, *args, **kwargs) -> None:
        """
            Execute all actions in the event if the event is not disabled
            and remove all unusable actions.
        """
        if self.is_disabled: return

        left_actions = {}
        for key, action in self.__actions.items():
            await action.exec(*args, **kwargs)
            if action.is_usable:
                left_actions[key] = action
        self.__actions = left_actions
