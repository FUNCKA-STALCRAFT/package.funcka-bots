from funcka_bots.events import BaseEvent, event_builder


vkevent: BaseEvent = event_builder.build_vkevent(
    event_type="message",
    event_id=1245124124,
    peer={"bpid": 0, "cid": 0, "name": "Some Converastion"},
    user={
        "uudi": 0,
        "name": "Some User",
        "firstname": "Some",
        "lastname": "User",
        "nick": "someuser",
    },
    message={"cmid": 0, "text": "Hi!", "attachemnts": []},
    message_reply={"uuid": 0, "cmid": 0, "text": "He!"},
)

# OR if message contains forwarded messages\group of replied messages

vkevent: BaseEvent = event_builder.build_vkevent(
    event_type="message",
    event_id=1245124124,
    peer={"bpid": 0, "cid": 0, "name": "Some Converastion"},
    user={
        "uudi": 0,
        "name": "Some User",
        "firstname": "Some",
        "lastname": "User",
        "nick": "someuser",
    },
    message={"cmid": 0, "text": "Hi!", "attachemnts": []},
    message_forward=[
        {"uuid": 0, "cmid": 0, "text": "Hu!"},
        {"uuid": 0, "cmid": 0, "text": "Ho!"},
    ],
)

# Event type for a custom VK event
# is set when building an event.
# Optional fields are also set only as needed.
# # Thus, you can create as many event options as you want,
# # declare their own types to them, and their own attributes.
# These don't have to be classic events like Reaction or Button...
# Using this logic, you can handle cmdlets or combined events.

combined_vkevent: BaseEvent = event_builder.build_vkevent(
    event_type="combined_event",
    event_id=1245124124,
    peer={"bpid": 0, "cid": 0, "name": "Some Converastion"},
    user={
        "uudi": 0,
        "name": "Some User",
        "firstname": "Some",
        "lastname": "User",
        "nick": "someuser",
    },
    button={"cmid": 0, "beid": 0, "payload": {"key": "value"}},
    reaction={"cmid": 0, "rid": 0},
)

# In a normal situation, when some service fletcher receives
# message from LPS VK, we can clearly identify only one message.
# However, we can create our own logic:
# For example, let's say that after pressing any button on the keyboard
# in the chat, we expect pressing any reaction.
# That's when we might need an example with a combined event.


# All the same applies to punishment events.
# Unlike VK events, punishment events are
# exclusively an internal concept, an internal structure
# through which data is transmitted to the punishment service.
# Usually, they contain data about the goal, and accompanying
# data for punishment. (Kick mode, number of warn points)

punishment: BaseEvent = event_builder.build_punishment(
    punishment_type="Kick",
    punishment_comment="Cross yourself!",
    peer={"bpid": 0, "cid": 0, "name": "Some Converastion"},
    user={
        "uudi": 0,
        "name": "Some User",
        "firstname": "Some",
        "lastname": "User",
        "nick": "someuser",
    },
    kick={"mode": "global"},
)
