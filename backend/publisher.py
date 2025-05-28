import json
import asyncio
from aio_pika import connect_robust, Message, ExchangeType

RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"

async def publish_notification(notification: dict):
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "notification-exchange",  
        ExchangeType.FANOUT,
        durable=True
    )

    await exchange.publish(
        Message(body=json.dumps(notification).encode()),
        routing_key=""  
    )

    await connection.close()
