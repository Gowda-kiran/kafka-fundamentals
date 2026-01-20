from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from pathlib import Path
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Load schema from .avsc file (production approach)
SCHEMA_FILE = Path(__file__).parent.parent.parent.parent / "schemas" / "orders" / "order-v1.avsc"
with open(SCHEMA_FILE, 'r') as f:
    order_avro_schema = json.dumps(json.load(f))

# Schema Registry setup
schema_registry_conf = {'url': os.getenv('SCHEMA_REGISTRY_URL')}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Avro serializer
avro_serializer = AvroSerializer(
    schema_registry_client,
    order_avro_schema,
    conf={
        'auto.register.schemas': False,
        'subject.name.strategy': 'record_name_strategy'
    }
)

# Producer config
producer_conf = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'acks': 'all',
    'linger.ms': 10,
    'retries': 5,
    'batch.size': 32 * 1024,
    'enable.idempotence': True
}

# Create producer once (reuse it)
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for Order {msg.key()}: {err}")
    else:
        print(f"Order {msg.key()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def send_to_kafka(order_data):
    if order_data['status'] == 'created':
        topic_name = "order.created"
    elif order_data['status'] == 'paid':
        topic_name = "order.paid"
    elif order_data['status'] == 'shipped':
        topic_name = "order.shipped"
    else:
        topic_name = "order.unknown"

    # Serialize value with Avro
    serialized_value = avro_serializer(
        order_data,
        SerializationContext(topic_name, MessageField.VALUE)
    )

    # Actually produce the message
    producer.produce(
        topic=topic_name,
        key=str(order_data['order_id']).encode('utf-8'),
        value=serialized_value,
        callback=delivery_report
    )

    producer.poll(0)
    producer.flush()