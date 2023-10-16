from collections import defaultdict
from typing import Any, Callable
class EventHandler:
    listeners = defaultdict(list)

    @staticmethod
    def listen(kind: str, callback_function: Callable):
        EventHandler.listeners[kind].append(callback_function)

    @staticmethod
    def generate(kind: str, instance: Any, payload: Any):
        for callback_func in EventHandler.listeners[kind]:
            callback_func(instance, payload)