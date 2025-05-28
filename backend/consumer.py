import asyncio
import json
from aio_pika import connect_robust, ExchangeType
from firebase_admin_setup import send_push

TOKENS_FILE = "tokens.json"
RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


async def consume():
    connection = None
    while connection is None:
        try:
            print("Trying to connect to RabbitMQ...")
            connection = await connect_robust(RABBITMQ_URL)
        except Exception:
            print("RabbitMQ not ready, retrying in 3 seconds...")
            await asyncio.sleep(3)

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange("notification-exchange", ExchangeType.FANOUT, durable=True)
    queue = await channel.declare_queue("notifications-queue", durable=True)
    await queue.bind(exchange)

    print("Connected to RabbitMQ. Waiting for messages...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    print(f"📩 Received: {message.body.decode()}")
                    payload = json.loads(message.body)

                    with open(TOKENS_FILE, "r") as f:
                        tokens = json.load(f)

                    for token in tokens:
                        try:
                            send_push(token, payload)
                            print(f"✅ Sent to {token}")
                        except Exception as e:
                            print(f"❌ Failed for {token}: {e}")

                except Exception as e:
                    print(f"Error handling message: {e}")

if __name__ == "__main__":
    asyncio.run(consume())
