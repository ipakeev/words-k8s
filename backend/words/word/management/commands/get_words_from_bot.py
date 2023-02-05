import json
from typing import Any

import pika
from django.core.management.base import BaseCommand
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from words.application.settings import CONFIG
from words.word.models import Word


class Command(BaseCommand):
    help = "Store new words to the database."

    def handle(self, *args: Any, **kwargs: Any) -> None:
        parameters = pika.URLParameters(CONFIG.rabbit.url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(CONFIG.rabbit.exchange)
        result = channel.queue_declare("")
        queue_name = result.method.queue
        channel.queue_bind(
            queue_name,
            CONFIG.rabbit.exchange,
            routing_key=CONFIG.rabbit.routing_key,
        )
        consumer_tag = channel.basic_consume(
            queue=queue_name,
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

    @staticmethod
    def on_message_callback(
        channel: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        data: dict = json.loads(body)
        print(f"consumed msg: {data}")
        Word.objects.create(original=data["original"])
        channel.basic_ack(delivery_tag=method.delivery_tag)
