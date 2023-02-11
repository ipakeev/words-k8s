from dataclasses import dataclass


@dataclass
class MessageToSend:
    chat_id: int
    text: str
