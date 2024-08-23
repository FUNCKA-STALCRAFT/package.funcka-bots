from funcka_bots.handler import ABCHandler
from funcka_bots.broker.events import BaseEvent


class SomeHandler(ABCHandler):
    def __call__(self, event: BaseEvent) -> None:
        try:
            self.main_func(event)

        except Exception as e:
            print(e)

        finally:
            self.finally_func(event)

    def main_func(self, event: BaseEvent) -> None:
        print(event.as_dict())

    def finally_func(self, event: BaseEvent) -> None:
        del event


# Usually, the handler looks something like this.
# However, this does not mean that it can be done
# that's the only way. The implementation is limited only by the fact,
# that the handler will only perform the actions
# if it will be called as a callable object. (function)


def main() -> None:
    handle_event = SomeHandler()
    event = BaseEvent()

    handle_event(event)
