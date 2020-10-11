from typing import Callable

class ActionState:
    UNLIMITED = -1
    NEUTRAL = 0
    ONCE = 1

class Action:

    @property
    def is_limited(self) -> bool:
        """Return True if the action can be called only several times otherwise False."""
        return self.__times > ActionState.UNLIMITED

    @property
    def is_unlimited(self) -> bool:
        """Return True if the action can be called an unlimited number of times otherwise False."""
        return not self.is_limited

    @property
    def is_usable(self) -> bool:
        """Return True if Action can be run otherwise False."""
        return self.is_unlimited or self.__times > ActionState.NEUTRAL

    def __init__(self, callback: Callable, times: int = ActionState.UNLIMITED) -> None:
        self.__callback = callback
        self.__times = times

    def __eq__(self, other) -> bool:
        if callable(other):
            return self.__callback.__name__ == other.__name__
        return NotImplemented

    async def exec(self, *args, **kwargs) -> None:
        """Call callback was given if the action is usable."""
        if self.is_usable:
            if self.is_limited:
                self.__times -= 1
            self.__callback(*args, **kwargs)

