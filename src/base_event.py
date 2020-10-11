from __future__ import annotations
from typing import Callable
from abc import ABC, abstractmethod
from .action import Action

class BaseEvent:
    @abstractmethod
    def on(self, callback: Callable) -> BaseEvent: pass

    @abstractmethod
    def once(self, times: int, callback: Callable) -> BaseEvent: pass

    @abstractmethod
    def off(self, callback: Callable) -> BaseEvent: pass

    @abstractmethod
    def enable(self) -> BaseEvent: pass

    @abstractmethod
    def disable(self) -> BaseEvent: pass

    @abstractmethod
    def is_enabled(self) -> bool: pass

    @abstractmethod
    def is_disabled(self) -> bool: pass

    @abstractmethod
    async def emit(self, *args, **kwargs) -> None: pass
