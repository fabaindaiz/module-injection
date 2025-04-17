from abc import ABC, abstractmethod
from threading import Thread
from typing import Callable

class EventContext(ABC):
    pass

class EventSubscriber(ABC):
    def __init__(self, callback: Callable[[EventContext], None]) -> None:
        self.callback: Callable[[EventContext], None] = callback

    def update(self, context: EventContext) -> None:
        Thread(target=self.callback, args=(context,), daemon=True).start()

class EventPublisher():
    def __init__(self) -> None:
        self.__targets: dict[type[EventContext], list[EventSubscriber]] = {}

    def subscribe(self, listener: type[EventSubscriber]) -> Callable:
        def wrapper(func: Callable[[EventContext], None]) -> Callable[[EventContext], None]:
            for name, value in func.__annotations__.items():
                if name == "return":
                    raise TypeError(f"Subscribe must wrap a function with an argument subtype EventContext, but '{func.__name__}' has a return type annotation.")
                if not issubclass(value, EventContext):
                    raise TypeError(f"Subscribe must wrap a function with an argument subtype EventContext, but '{func.__name__}' parameter '{name}' is of type '{value.__name__}'.")
                break
            self.__targets.setdefault(value, []).append(listener(func))
            return func
        return wrapper
    
    def update(self, context: EventContext) -> None:
        listeners = self.__targets.get(type(context), [])
        for listener in listeners:
            listener.update(context)


if __name__ == '__main__':
    class EventA(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameterA = parameter

    class EventB(EventContext):
        def __init__(self, parameter: str) -> None:
            self.parameterB = parameter

    class Observer():
        def __init__(self) -> None:
            self.publisher = EventPublisher()

            @self.publisher.subscribe(EventSubscriber)
            def listen_event_a(context1: EventA) -> None:
                print(f"Event A triggered with parameter: {context1.parameterA}")
            
            @self.publisher.subscribe(EventSubscriber)
            def listen_event_b(context2: EventB) -> None:
                print(f"Event B triggered with parameter: {context2.parameterB}")
        
    instance = Observer()
    instance.publisher.update(EventA("Hello World!"))
    instance.publisher.update(EventB("Goodbye World!"))