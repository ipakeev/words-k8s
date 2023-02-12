import json
from typing import Any

import pika
from django.core.management.base import BaseCommand
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from words.application import settings
from words.word.models import Word


class Command(BaseCommand):
    help = "Store new words to the database."

    @property
    def broker_url(self) -> str:
        if settings.RABBIT_USERNAME:
            credentials = f"{settings.RABBIT_USERNAME}:{settings.RABBIT_PASSWORD}@"
        else:
            credentials = ""
        return f"{settings.RABBIT_SCHEMA}{credentials}{settings.RABBIT_HOST}:{settings.RABBIT_PORT}"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        parameters = pika.URLParameters(self.broker_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(settings.RABBIT_QUEUE)
        channel.queue_bind(
            queue=settings.RABBIT_QUEUE,
            exchange=settings.RABBIT_EXCHANGE,
            routing_key=settings.RABBIT_ROUTING_KEY,
        )
        consumer_tag = channel.basic_consume(
            queue=settings.RABBIT_QUEUE,
            on_message_callback=self.on_message_callback,
        )

        try:
            print("starting")
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Stopping process, please wait...")
            channel.stop_consuming(consumer_tag=consumer_tag)
        finally:
            connection.close()

    def on_message_callback(
        self,
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        data: dict = json.loads(body)
        print(f"consumed msg: {data}")
        Word.objects.create(original=data["original"])
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def notify_word_created(self) -> None:
        pass
