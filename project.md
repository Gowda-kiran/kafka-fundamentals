# 🛍️ E-commerce Event Streaming Project
**Real-Time Analytics Pipeline with Kafka + Schema Evolution**

---

## 📋 Project Overview

**Goal**: Build a production-grade real-time e-commerce analytics pipeline demonstrating Kafka, Schema Registry, Spark Streaming, and modern data engineering patterns.

**Tech Stack**:
- **Streaming**: Kafka + Schema Registry (Avro)
- **Processing**: Spark Streaming
- **Storage**: Parquet/Iceberg on MinIO/S3
- **Orchestration**: Airflow (optional)
- **Visualization**: Metabase/Grafana
- **Language**: Python

**Timeline**: 3-4 weeks (1-2 hours/weekday, 3 hours/weekend)

**Portfolio Impact**: ⭐⭐⭐⭐⭐
- Aligns with your e-commerce background
- Demonstrates real-time data engineering
- Shows schema evolution mastery
- Production-ready patterns

---

## 🎯 Learning Objectives

By completing this project, you will master:

- [ ] Kafka topic design and partitioning strategies
- [ ] Schema Registry with Avro serialization
- [ ] Backward/forward/full compatibility modes
- [ ] Spark Structured Streaming
- [ ] Exactly-once semantics
- [ ] Event-driven architecture
- [ ] Real-time aggregations and windowing
- [ ] Production monitoring and error handling

---

## 📚 Prerequisites

### Required Knowledge
- [ ] Basic Kafka concepts (topics, partitions, producers, consumers)
- [ ] Python programming
- [ ] SQL fundamentals
- [ ] Basic understanding of Docker

### Setup Requirements
- [ ] Docker Desktop installed
- [ ] Python 3.8+ installed
- [ ] 8GB+ RAM available
- [ ] VS Code or preferred IDE
- [ ] Git for version control

---

## 🗓️ Phase-by-Phase Plan

---

## **PHASE 1: Foundation Setup** ⏱️ Week 1 (Days 1-7)

### Day 1: Environment Setup (2 hours)

**Objectives**:
- [ ] Set up Docker environment
- [ ] Verify all components running
- [ ] Understand the architecture

**Tasks**:

**1. Create project directory**
```bash
mkdir ecommerce-streaming-pipeline
cd ecommerce-streaming-pipeline
```

**2. Create docker-compose.yml**
```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  schema-registry:
    image: confluentinc/cp-schema-registry:7.5.0
    depends_on:
      - kafka
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka:9092
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    depends_on:
      - kafka
      - schema-registry
    ports:
      - "8080:8080"
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
      KAFKA_CLUSTERS_0_SCHEMAREGISTRY: http://schema-registry:8081
```

**3. Start services**
```bash
docker-compose up -d
```

**4. Verify setup**
```bash
# Check all containers running
docker-compose ps

# Access Kafka UI
# Open browser: http://localhost:8080
```

**Checkpoint**:
- [ ] All containers running (green status)
- [ ] Kafka UI accessible
- [ ] No error logs

---

### Day 2: Event Schema Design (2 hours)

**Objectives**:
- [ ] Design realistic e-commerce event schemas
- [ ] Understand Avro schema structure
- [ ] Create schema evolution strategy

**Tasks**:

**1. Create schemas directory**
```bash
mkdir -p schemas/v1 schemas/v2
```

**2. Design Version 1 Schema**

Create `schemas/v1/user_event.avsc`:
```json
{
  "type": "record",
  "name": "UserEvent",
  "namespace": "com.ecommerce.events",
  "doc": "User activity event in e-commerce platform",
  "fields": [
    {
      "name": "event_id",
      "type": "string",
      "doc": "Unique event identifier (UUID)"
    },
    {
      "name": "user_id",
      "type": "string",
      "doc": "User identifier"
    },
    {
      "name": "event_type",
      "type": {
        "type": "enum",
        "name": "EventType",
        "symbols": [
          "PAGE_VIEW",
          "ADD_TO_CART",
          "REMOVE_FROM_CART",
          "PURCHASE",
          "SEARCH"
        ]
      },
      "doc": "Type of user action"
    },
    {
      "name": "timestamp",
      "type": "long",
      "doc": "Event timestamp (epoch milliseconds)"
    },
    {
      "name": "session_id",
      "type": "string",
      "doc": "User session identifier"
    }
  ]
}
```

**3. Design Version 2 Schema (Evolved)**

Create `schemas/v2/user_event.avsc`:
```json
{
  "type": "record",
  "name": "UserEvent",
  "namespace": "com.ecommerce.events",
  "doc": "User activity event - v2 with enriched fields",
  "fields": [
    {
      "name": "event_id",
      "type": "string"
    },
    {
      "name": "user_id",
      "type": "string"
    },
    {
      "name": "event_type",
      "type": {
        "type": "enum",
        "name": "EventType",
        "symbols": [
          "PAGE_VIEW",
          "ADD_TO_CART",
          "REMOVE_FROM_CART",
          "PURCHASE",
          "SEARCH"
        ]
      }
    },
    {
      "name": "timestamp",
      "type": "long"
    },
    {
      "name": "session_id",
      "type": "string"
    },
    {
      "name": "product_id",
      "type": ["null", "string"],
      "default": null,
      "doc": "Product ID (if applicable)"
    },
    {
      "name": "product_name",
      "type": ["null", "string"],
      "default": null,
      "doc": "Product name"
    },
    {
      "name": "price",
      "type": ["null", "double"],
      "default": null,
      "doc": "Product price"
    },
    {
      "name": "category",
      "type": ["null", "string"],
      "default": null,
      "doc": "Product category"
    },
    {
      "name": "device_type",
      "type": ["null", {
        "type": "enum",
        "name": "DeviceType",
        "symbols": ["MOBILE", "DESKTOP", "TABLET"]
      }],
      "default": null,
      "doc": "Device used"
    },
    {
      "name": "country",
      "type": ["null", "string"],
      "default": null,
      "doc": "User country code"
    }
  ]
}
```

**Checkpoint**:
- [ ] Both schema versions created
- [ ] Understand difference between v1 and v2
- [ ] Verified backward compatibility (v2 has defaults for new fields)

**📝 Notes**:
- V2 adds optional fields with `null` union type and `default: null`
- This ensures backward compatibility
- Old consumers can read new messages (ignore new fields)
- New consumers can read old messages (use default values)

---

### Day 3: Event Generator - Basic Version (2 hours)

**Objectives**:
- [ ] Create realistic event generator
- [ ] Understand event patterns
- [ ] Generate diverse event types

**Tasks**:

**1. Create generator directory**
```bash
mkdir -p src
```

**2. Install dependencies**
```bash
pip install confluent-kafka faker avro-python3
```

**3. Create event generator**

Create `src/event_generator.py`:
```python
"""
E-commerce Event Generator
Generates realistic user events for streaming pipeline
"""

import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List
from faker import Faker

fake = Faker()

# Product catalog
PRODUCTS = [
    {"id": "prod_001", "name": "iPhone 15 Pro", "price": 79999, "category": "Electronics"},
    {"id": "prod_002", "name": "Nike Air Max", "price": 4999, "category": "Fashion"},
    {"id": "prod_003", "name": "Coffee Maker", "price": 2499, "category": "Home"},
    {"id": "prod_004", "name": "Yoga Mat", "price": 899, "category": "Sports"},
    {"id": "prod_005", "name": "Laptop Backpack", "price": 1999, "category": "Accessories"},
    {"id": "prod_006", "name": "Wireless Earbuds", "price": 3499, "category": "Electronics"},
    {"id": "prod_007", "name": "Running Shoes", "price": 5999, "category": "Sports"},
    {"id": "prod_008", "name": "Smart Watch", "price": 12999, "category": "Electronics"},
    {"id": "prod_009", "name": "Jeans", "price": 2999, "category": "Fashion"},
    {"id": "prod_010", "name": "Water Bottle", "price": 499, "category": "Sports"},
]

EVENT_TYPES = ["PAGE_VIEW", "ADD_TO_CART", "REMOVE_FROM_CART", "PURCHASE", "SEARCH"]
DEVICES = ["MOBILE", "DESKTOP", "TABLET"]
COUNTRIES = ["IN", "US", "UK", "DE", "CA", "AU"]

class SessionManager:
    """Manages realistic user sessions"""
    
    def __init__(self):
        self.active_sessions: Dict[str, Dict] = {}
        self.session_duration_minutes = (5, 30)  # min, max
    
    def get_or_create_session(self, user_id: str) -> str:
        """Get existing session or create new one"""
        now = datetime.utcnow()
        
        # Clean up old sessions
        expired = [
            sid for sid, data in self.active_sessions.items()
            if (now - data['start_time']).seconds > data['duration']
        ]
        for sid in expired:
            del self.active_sessions[sid]
        
        # Check if user has active session
        user_sessions = [
            sid for sid, data in self.active_sessions.items()
            if data['user_id'] == user_id
        ]
        
        if user_sessions:
            return user_sessions[0]
        
        # Create new session
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        duration = random.randint(*self.session_duration_minutes) * 60
        
        self.active_sessions[session_id] = {
            'user_id': user_id,
            'start_time': now,
            'duration': duration,
            'cart': [],
            'viewed_products': []
        }
        
        return session_id
    
    def get_session_data(self, session_id: str) -> Dict:
        """Get session data"""
        return self.active_sessions.get(session_id, {})

class EventGenerator:
    """Generates realistic e-commerce events"""
    
    def __init__(self, num_users: int = 100):
        self.users = [f"user_{i:04d}" for i in range(num_users)]
        self.session_manager = SessionManager()
    
    def generate_event(self, schema_version: int = 1) -> Dict:
        """Generate a single event"""
        
        user_id = random.choice(self.users)
        session_id = self.session_manager.get_or_create_session(user_id)
        session_data = self.session_manager.get_session_data(session_id)
        
        # Choose event type based on session state
        event_type = self._choose_event_type(session_data)
        
        # Base event (v1 schema)
        event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event_type": event_type,
            "timestamp": int(datetime.utcnow().timestamp() * 1000),
            "session_id": session_id
        }
        
        # Add v2 fields if requested
        if schema_version == 2:
            product = random.choice(PRODUCTS)
            
            event.update({
                "product_id": product["id"] if event_type != "SEARCH" else None,
                "product_name": product["name"] if event_type != "SEARCH" else None,
                "price": product["price"] if event_type != "SEARCH" else None,
                "category": product["category"] if event_type != "SEARCH" else None,
                "device_type": random.choice(DEVICES),
                "country": random.choice(COUNTRIES)
            })
            
            # Update session state
            if event_type == "ADD_TO_CART":
                session_data.get('cart', []).append(product["id"])
            elif event_type == "REMOVE_FROM_CART" and session_data.get('cart'):
                session_data['cart'].pop()
        
        return event
    
    def _choose_event_type(self, session_data: Dict) -> str:
        """Choose event type based on realistic user behavior"""
        
        # 60% page views, 20% add to cart, 10% purchase, 5% remove, 5% search
        weights = {
            "PAGE_VIEW": 60,
            "ADD_TO_CART": 20,
            "PURCHASE": 10,
            "REMOVE_FROM_CART": 5,
            "SEARCH": 5
        }
        
        # Can't remove if cart is empty
        if not session_data.get('cart'):
            weights["REMOVE_FROM_CART"] = 0
            weights["PURCHASE"] = 0
        
        choices = list(weights.keys())
        w = list(weights.values())
        
        return random.choices(choices, weights=w)[0]
    
    def generate_batch(self, count: int, schema_version: int = 1) -> List[Dict]:
        """Generate multiple events"""
        return [self.generate_event(schema_version) for _ in range(count)]

# Test the generator
if __name__ == "__main__":
    generator = EventGenerator(num_users=50)
    
    print("Generating 10 events (v1 schema):")
    for event in generator.generate_batch(10, schema_version=1):
        print(json.dumps(event, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    print("Generating 10 events (v2 schema):")
    for event in generator.generate_batch(10, schema_version=2):
        print(json.dumps(event, indent=2))
```

**4. Test the generator**
```bash
python src/event_generator.py
```

**Checkpoint**:
- [ ] Generator creates realistic events
- [ ] Events follow user behavior patterns (sessions, cart)
- [ ] Both v1 and v2 schemas working
- [ ] Understand event distribution

---

### Day 4-5: Kafka Producer with Schema Registry (3-4 hours)

**Objectives**:
- [ ] Integrate Schema Registry
- [ ] Implement Avro serialization
- [ ] Create Kafka producer
- [ ] Handle errors properly

**Tasks**:

**1. Install dependencies**
```bash
pip install confluent-kafka[avro] requests
```

**2. Create Kafka producer**

Create `src/kafka_producer.py`:
```python
"""
Kafka Producer with Schema Registry
Produces e-commerce events to Kafka with Avro serialization
"""

import json
import time
from typing import Dict
from confluent_kafka import Producer
from confluent_kafka.avro import AvroProducer
from confluent_kafka.admin import AdminClient, NewTopic
from event_generator import EventGenerator

# Configuration
KAFKA_BROKER = 'localhost:9092'
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
TOPIC_NAME = 'ecommerce-events'

# Load Avro schemas
def load_schema(schema_path: str) -> str:
    """Load Avro schema from file"""
    with open(schema_path, 'r') as f:
        return f.read()

def create_topic_if_not_exists(topic: str, num_partitions: int = 3):
    """Create Kafka topic if it doesn't exist"""
    admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
    
    # Check if topic exists
    metadata = admin_client.list_topics(timeout=10)
    if topic not in metadata.topics:
        print(f"Creating topic: {topic}")
        new_topic = NewTopic(
            topic,
            num_partitions=num_partitions,
            replication_factor=1
        )
        admin_client.create_topics([new_topic])
        print(f"Topic {topic} created successfully")
    else:
        print(f"Topic {topic} already exists")

def delivery_callback(err, msg):
    """Callback for message delivery reports"""
    if err:
        print(f'❌ Message delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')

class EcommerceEventProducer:
    """Producer for e-commerce events with Avro serialization"""
    
    def __init__(self, schema_version: int = 1):
        self.schema_version = schema_version
        
        # Load appropriate schema
        schema_path = f'schemas/v{schema_version}/user_event.avsc'
        self.value_schema = load_schema(schema_path)
        
        # Create AvroProducer
        self.producer = AvroProducer({
            'bootstrap.servers': KAFKA_BROKER,
            'schema.registry.url': SCHEMA_REGISTRY_URL,
            'compression.type': 'snappy',  # Compress messages
            'linger.ms': 100,  # Batch messages for 100ms
            'acks': 'all'  # Wait for all replicas
        }, default_value_schema=self.value_schema)
        
        self.event_generator = EventGenerator(num_users=100)
        
        print(f"Producer initialized with schema version {schema_version}")
    
    def produce_event(self, event: Dict):
        """Produce a single event to Kafka"""
        try:
            self.producer.produce(
                topic=TOPIC_NAME,
                value=event,
                key=event['user_id'],  # Partition by user_id
                callback=delivery_callback
            )
            self.producer.poll(0)  # Trigger callbacks
        except Exception as e:
            print(f"Error producing event: {e}")
    
    def produce_continuous(self, events_per_second: int = 10, duration_seconds: int = 60):
        """Produce events continuously"""
        print(f"Producing {events_per_second} events/sec for {duration_seconds} seconds...")
        
        interval = 1.0 / events_per_second
        end_time = time.time() + duration_seconds
        
        count = 0
        while time.time() < end_time:
            event = self.event_generator.generate_event(self.schema_version)
            self.produce_event(event)
            count += 1
            time.sleep(interval)
        
        # Flush remaining messages
        self.producer.flush()
        print(f"\nProduced {count} events total")
    
    def produce_batch(self, num_events: int):
        """Produce a batch of events"""
        print(f"Producing {num_events} events...")
        
        for i in range(num_events):
            event = self.event_generator.generate_event(self.schema_version)
            self.produce_event(event)
            
            if (i + 1) % 100 == 0:
                print(f"Produced {i + 1} events...")
        
        self.producer.flush()
        print(f"✅ All {num_events} events produced")

if __name__ == "__main__":
    # Create topic
    create_topic_if_not_exists(TOPIC_NAME, num_partitions=3)
    
    # Create producer with v1 schema
    producer = EcommerceEventProducer(schema_version=1)
    
    # Produce 100 events
    producer.produce_batch(100)
    
    # Or produce continuously
    # producer.produce_continuous(events_per_second=10, duration_seconds=30)
```

**3. Test the producer**
```bash
python src/kafka_producer.py
```

**4. Verify in Kafka UI**
- Open http://localhost:8080
- Navigate to Topics → ecommerce-events
- Check messages are arriving
- Verify schema in Schema Registry

**Checkpoint**:
- [ ] Producer sends events to Kafka
- [ ] Schema registered in Schema Registry
- [ ] Messages visible in Kafka UI
- [ ] No errors in producer logs

---

### Day 6-7: Basic Kafka Consumer (3-4 hours)

**Objectives**:
- [ ] Create Avro consumer
- [ ] Implement proper offset management
- [ ] Handle consumer groups
- [ ] Process events correctly

**Tasks**:

**1. Create Kafka consumer**

Create `src/kafka_consumer.py`:
```python
"""
Kafka Consumer with Avro Deserialization
Consumes e-commerce events from Kafka
"""

import json
from typing import Dict
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro import AvroConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
SCHEMA_REGISTRY_URL = 'http://localhost:8081'
TOPIC_NAME = 'ecommerce-events'
CONSUMER_GROUP = 'ecommerce-analytics'

class EcommerceEventConsumer:
    """Consumer for e-commerce events with Avro deserialization"""
    
    def __init__(self, consumer_group: str = CONSUMER_GROUP):
        self.consumer = AvroConsumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': consumer_group,
            'schema.registry.url': SCHEMA_REGISTRY_URL,
            'auto.offset.reset': 'earliest',  # Start from beginning
            'enable.auto.commit': False  # Manual commit for exactly-once
        })
        
        self.consumer.subscribe([TOPIC_NAME])
        print(f"Consumer subscribed to {TOPIC_NAME} with group {consumer_group}")
    
    def process_event(self, event: Dict):
        """Process a single event - override this for custom processing"""
        print(f"Event: {event['event_type']:15s} | "
              f"User: {event['user_id']:10s} | "
              f"Product: {event.get('product_name', 'N/A'):20s}")
    
    def consume_batch(self, num_messages: int = 10):
        """Consume a specific number of messages"""
        print(f"Consuming {num_messages} messages...\n")
        
        consumed = 0
        try:
            while consumed < num_messages:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('Reached end of partition')
                    else:
                        print(f'Error: {msg.error()}')
                    continue
                
                # Deserialize message
                event = msg.value()
                
                # Process event
                self.process_event(event)
                
                consumed += 1
            
            # Commit offsets
            self.consumer.commit()
            print(f"\n✅ Consumed and committed {consumed} messages")
            
        except KeyboardInterrupt:
            print("\nConsumer interrupted")
        finally:
            self.consumer.close()
    
    def consume_continuous(self):
        """Consume messages continuously"""
        print("Consuming messages continuously (Ctrl+C to stop)...\n")
        
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f'Error: {msg.error()}')
                        continue
                
                # Deserialize message
                event = msg.value()
                
                # Process event
                self.process_event(event)
                
                # Commit every 100 messages
                if msg.offset() % 100 == 0:
                    self.consumer.commit()
                    print(f"Committed offset: {msg.offset()}")
        
        except KeyboardInterrupt:
            print("\nConsumer interrupted")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    consumer = EcommerceEventConsumer()
    
    # Consume 50 messages
    consumer.consume_batch(50)
    
    # Or consume continuously
    # consumer.consume_continuous()
```

**2. Test consumer**

Terminal 1 - Producer:
```bash
python src/kafka_producer.py
```

Terminal 2 - Consumer:
```bash
python src/kafka_consumer.py
```

**Checkpoint**:
- [ ] Consumer receives messages
- [ ] Avro deserialization works
- [ ] Consumer group management working
- [ ] Offsets committed properly

---

## 📊 Week 1 Checkpoint

**What you should have by end of Week 1**:
- [x] Docker environment running (Kafka, Schema Registry, Kafka UI)
- [x] Avro schemas designed (v1 and v2)
- [x] Event generator creating realistic data
- [x] Kafka producer with Schema Registry integration
- [x] Kafka consumer with Avro deserialization
- [x] Basic end-to-end flow working

**Interview talking point**:
"I set up a Kafka environment with Schema Registry and built an event generator that creates realistic e-commerce user events. The producer uses Avro serialization for efficient, schema-validated messages."

---

## **PHASE 2: Schema Evolution** ⏱️ Week 2 (Days 8-14)

### Day 8: Schema Evolution - Theory & Planning (2 hours)

**Objectives**:
- [ ] Understand compatibility modes deeply
- [ ] Plan migration strategy
- [ ] Test compatibility locally

**Tasks**:

**1. Study compatibility modes**

Read and understand:
- Backward compatibility (new schema reads old data)
- Forward compatibility (old schema reads new data)
- Full compatibility (both)

**2. Test schema compatibility**

Create `src/test_compatibility.py`:
```python
"""
Test schema compatibility between versions
"""

import requests
import json

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
SUBJECT = 'ecommerce-events-value'

def load_schema(path):
    with open(path, 'r') as f:
        return json.load(f)

def register_schema(schema):
    """Register schema with Schema Registry"""
    response = requests.post(
        f"{SCHEMA_REGISTRY_URL}/subjects/{SUBJECT}/versions",
        headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
        json={'schema': json.dumps(schema)}
    )
    return response.json()

def check_compatibility(schema):
    """Check if schema is compatible with latest version"""
    response = requests.post(
        f"{SCHEMA_REGISTRY_URL}/compatibility/subjects/{SUBJECT}/versions/latest",
        headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
        json={'schema': json.dumps(schema)}
    )
    return response.json()

if __name__ == "__main__":
    # Load schemas
    v1_schema = load_schema('schemas/v1/user_event.avsc')
    v2_schema = load_schema('schemas/v2/user_event.avsc')
    
    print("Testing v1 → v2 compatibility...")
    
    # Check if v2 is compatible with v1
    result = check_compatibility(v2_schema)
    
    if result.get('is_compatible'):
        print("✅ V2 schema is BACKWARD COMPATIBLE with V1")
    else:
        print("❌ V2 schema is NOT compatible")
        print(f"Error: {result}")
```

**Checkpoint**:
- [ ] Understand why v2 is backward compatible
- [ ] Know what changes would break compatibility
- [ ] Can test compatibility before deploying

---

### Day 9-10: Implement Schema Evolution (3-4 hours)

**Objectives**:
- [ ] Deploy v2 schema
- [ ] Run dual producers (v1 and v2)
- [ ] Verify consumers handle both versions

**Tasks**:

**1. Create migration script**

Create `src/migrate_schema.py`:
```python
"""
Schema Migration Script
Safely migrate from v1 to v2 schema
"""

import requests
import json
import time
from kafka_producer import EcommerceEventProducer

SCHEMA_REGISTRY_URL = 'http://localhost:8081'
SUBJECT = 'ecommerce-events-value'

def get_current_version():
    """Get current schema version"""
    response = requests.get(f"{SCHEMA_REGISTRY_URL}/subjects/{SUBJECT}/versions/latest")
    if response.status_code == 200:
        return response.json()['version']
    return 0

def register_new_schema():
    """Register v2 schema"""
    with open('schemas/v2/user_event.avsc', 'r') as f:
        schema = json.load(f)
    
    response = requests.post(
        f"{SCHEMA_REGISTRY_URL}/subjects/{SUBJECT}/versions",
        headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
        json={'schema': json.dumps(schema)}
    )
    
    if response.status_code == 200:
        print(f"✅ V2 schema registered: version {response.json()['id']}")
        return True
    else:
        print(f"❌ Failed to register schema: {response.text}")
        return False

def run_dual_write(duration_seconds: int = 60):
    """Run dual-write: both v1 and v2 producers"""
    print(f"Running dual-write for {duration_seconds} seconds...")
    
    v1_producer = EcommerceEventProducer(schema_version=1)
    v2_producer = EcommerceEventProducer(schema_version=2)
    
    end_time = time.time() + duration_seconds
    count = 0
    
    while time.time() < end_time:
        # Send v1 event
        v1_event = v1_producer.event_generator.generate_event(1)
        v1_producer.produce_event(v1_event)
        
        # Send v2 event
        v2_event = v2_producer.event_generator.generate_event(2)
        v2_producer.produce_event(v2_event)
        
        count += 2
        time.sleep(0.1)
    
    v1_producer.producer.flush()
    v2_producer.producer.flush()
    
    print(f"✅ Dual-write complete: {count} events sent")

if __name__ == "__main__":
    print("Schema Migration Process")
    print("=" * 50)
    
    # Step 1: Check current version
    current = get_current_version()
    print(f"Current schema version: {current}")
    
    # Step 2: Register v2
    if register_new_schema():
        # Step 3: Run dual-write
        run_dual_write(duration_seconds=30)
    else:
        print("Migration aborted")
```

**2. Test migration**
```bash
python src/migrate_schema.py
```

**3. Verify in Kafka UI**
- Check that both v1 and v2 messages exist
- Verify Schema Registry shows both versions
- Consumer should read both versions successfully

**Checkpoint**:
- [ ] V2 schema registered successfully
- [ ] Dual-write working (both schemas coexist)
- [ ] Consumer reads both v1 and v2 messages
- [ ] No compatibility errors

---

### Day 11-12: Advanced Consumer - Handle Multiple Versions (3 hours)

**Objectives**:
- [ ] Build version-aware consumer
- [ ] Extract analytics from enriched v2 data
- [ ] Handle schema differences gracefully

**Tasks**:

**1. Create analytics consumer**

Create `src/analytics_consumer.py`:
```python
"""
Analytics Consumer
Processes events from both schema versions and generates insights
"""

from collections import defaultdict
from typing import Dict
from kafka_consumer import EcommerceEventConsumer

class AnalyticsConsumer(EcommerceEventConsumer):
    """Consumer that extracts analytics from events"""
    
    def __init__(self):
        super().__init__(consumer_group='analytics-group')
        
        # Analytics state
        self.event_counts = defaultdict(int)
        self.events_by_device = defaultdict(int)
        self.events_by_country = defaultdict(int)
        self.revenue = 0.0
        self.cart_additions = 0
        self.purchases = 0
        
    def process_event(self, event: Dict):
        """Process event and update analytics"""
        
        event_type = event['event_type']
        self.event_counts[event_type] += 1
        
        # V2-specific fields (may not exist in v1 messages)
        device = event.get('device_type')
        country = event.get('country')
        price = event.get('price')
        
        if device:
            self.events_by_device[device] += 1
        
        if country:
            self.events_by_country[country] += 1
        
        # Track conversions
        if event_type == 'ADD_TO_CART':
            self.cart_additions += 1
        
        if event_type == 'PURCHASE' and price:
            self.purchases += 1
            self.revenue += price
        
        # Print summary every 100 events
        total_events = sum(self.event_counts.values())
        if total_events % 100 == 0:
            self.print_summary()
    
    def print_summary(self):
        """Print analytics summary"""
        total = sum(self.event_counts.values())
        
        print("\n" + "="*60)
        print(f"Analytics Summary (Total Events: {total})")
        print("="*60)
        
        print("\nEvent Types:")
        for event_type, count in sorted(self.event_counts.items()):
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {event_type:20s}: {count:5d} ({pct:5.1f}%)")
        
        if self.events_by_device:
            print("\nBy Device:")
            for device, count in sorted(self.events_by_device.items()):
                pct = (count / sum(self.events_by_device.values()) * 100)
                print(f"  {device:10s}: {count:5d} ({pct:5.1f}%)")
        
        if self.events_by_country:
            print("\nBy Country:")
            for country, count in sorted(self.events_by_country.items()):
                pct = (count / sum(self.events_by_country.values()) * 100)
                print(f"  {country:10s}: {count:5d} ({pct:5.1f}%)")
        
        if self.cart_additions > 0:
            conversion_rate = (self.purchases / self.cart_additions * 100)
            print(f"\nConversion: {self.cart_additions} carts → {self.purchases} purchases ({conversion_rate:.1f}%)")
            print(f"Revenue: ₹{self.revenue:,.2f}")
        
        print("="*60 + "\n")

if __name__ == "__main__":
    consumer = AnalyticsConsumer()
    consumer.consume_continuous()
```

**2. Test analytics**

Terminal 1 - Producer (v2):
```bash
python -c "from kafka_producer import *; p = EcommerceEventProducer(2); p.produce_continuous(10, 120)"
```

Terminal 2 - Analytics Consumer:
```bash
python src/analytics_consumer.py
```

**Checkpoint**:
- [ ] Consumer handles both v1 and v2 messages
- [ ] Analytics extracted from v2 enriched data
- [ ] Graceful handling of missing fields
- [ ] Real-time metrics displayed

---

### Day 13-14: Document Schema Evolution (2-3 hours)

**Objectives**:
- [ ] Document the migration process
- [ ] Create runbook for future migrations
- [ ] Prepare for interviews

**Tasks**:

**1. Create SCHEMA_EVOLUTION.md**
```markdown
# Schema Evolution Guide

## Overview
This document describes how we evolved our e-commerce event schema from v1 to v2.

## Changes in V2
- Added `product_id`, `product_name`, `price`, `category` (optional)
- Added `device_type` enum (optional)
- Added `country` field (optional)

## Why These Changes Are Backward Compatible
1. All new fields are optional (union with null)
2. All new fields have default values (null)
3. No fields were removed
4. No field types were changed
5. Enum values were only added, not removed

## Migration Process
1. Tested compatibility with Schema Registry
2. Registered v2 schema
3. Ran dual-write (both v1 and v2) for transition period
4. Verified old consumers work with new data
5. Verified new consumers work with old data
6. Gradually migrated all producers to v2

## Rollback Plan
If issues arise:
1. Stop all v2 producers
2. Continue with v1 producers
3. Old consumers are unaffected
4. New consumers handle v1 via default values
```

**2. Update README.md**
Add schema evolution section

**Checkpoint**:
- [ ] Documentation complete
- [ ] Can explain migration to interviewer
- [ ] Understand backward compatibility deeply

---

## 📊 Week 2 Checkpoint

**What you should have**:
- [x] V2 schema deployed successfully
- [x] Both v1 and v2 messages in Kafka
- [x] Consumer handles both versions
- [x] Analytics extracted from enriched data
- [x] Complete documentation

**Interview talking point**:
"I implemented backward-compatible schema evolution using Avro and Schema Registry. When we needed to add device type and geolocation fields, I added them as optional fields with defaults, ensuring old consumers continued working while new consumers got enriched data. I validated compatibility before deploying and ran dual-write during the transition."

---

## **PHASE 3: Spark Streaming** ⏱️ Week 3 (Days 15-21)

### Day 15-16: Spark Streaming Setup (3-4 hours)

**Objectives**:
- [ ] Set up Spark Streaming environment
- [ ] Read from Kafka with Spark
- [ ] Process streaming data

**Tasks**:

**1. Add Spark to docker-compose**

Update `docker-compose.yml`:
```yaml
  spark-master:
    image: bitnami/spark:3.5.0
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
    ports:
      - "8081:8080"  # Spark UI (changed from 8080 to avoid conflict)
      - "7077:7077"  # Spark Master

  spark-worker:
    image: bitnami/spark:3.5.0
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2G
      - SPARK_WORKER_CORES=2
    depends_on:
      - spark-master
```

**2. Restart services**
```bash
docker-compose up -d
```

**3. Install PySpark locally**
```bash
pip install pyspark==3.5.0
```

**4. Create Spark Streaming job**

Create `src/spark_streaming.py`:
```python
"""
Spark Structured Streaming
Real-time processing of e-commerce events
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'ecommerce-events'
CHECKPOINT_DIR = '/tmp/spark-checkpoints/ecommerce'

def create_spark_session():
    """Create Spark session with Kafka support"""
    return SparkSession.builder \
        .appName("EcommerceStreaming") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .config("spark.sql.streaming.schemaInference", "true") \
        .getOrCreate()

def process_stream():
    """Main streaming processing logic"""
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "earliest") \
        .load()
    
    # Kafka returns: key, value, topic, partition, offset, timestamp
    # Our events are in the 'value' column as JSON
    
    # Define schema (matches v2)
    schema = StructType([
        StructField("event_id", StringType(), False),
        StructField("user_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("timestamp", LongType(), False),
        StructField("session_id", StringType(), False),
        StructField("product_id", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("category", StringType(), True),
        StructField("device_type", StringType(), True),
        StructField("country", StringType(), True),
    ])
    
    # Parse JSON value
    events = df.select(
        col("timestamp").alias("kafka_timestamp"),
        from_json(col("value").cast("string"), schema).alias("event")
    ).select("kafka_timestamp", "event.*")
    
    # Convert timestamp to datetime
    events = events.withColumn(
        "event_time",
        to_timestamp(col("timestamp") / 1000)
    )
    
    # Write to console (for testing)
    query = events.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .option("numRows", 10) \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    process_stream()
```

**5. Test Spark Streaming**

Terminal 1 - Producer:
```bash
python -c "from kafka_producer import *; p = EcommerceEventProducer(2); p.produce_continuous(5, 60)"
```

Terminal 2 - Spark:
```bash
python src/spark_streaming.py
```

**Checkpoint**:
- [ ] Spark reads from Kafka
- [ ] JSON parsed correctly
- [ ] Events displayed in console
- [ ] No errors in Spark logs

---

### Day 17-18: Real-time Aggregations (3-4 hours)

**Objectives**:
- [ ] Implement windowed aggregations
- [ ] Calculate real-time metrics
- [ ] Write results to storage

**Tasks**:

**1. Create aggregation job**

Create `src/spark_aggregations.py`:
```python
"""
Real-time Aggregations
Calculate e-commerce metrics in real-time
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'ecommerce-events'
OUTPUT_PATH = '/tmp/ecommerce-analytics'

def create_spark_session():
    return SparkSession.builder \
        .appName("EcommerceAggregations") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()

def calculate_metrics():
    """Calculate real-time metrics"""
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .load()
    
    # Schema
    schema = StructType([
        StructField("event_id", StringType()),
        StructField("user_id", StringType()),
        StructField("event_type", StringType()),
        StructField("timestamp", LongType()),
        StructField("session_id", StringType()),
        StructField("product_id", StringType()),
        StructField("product_name", StringType()),
        StructField("price", DoubleType()),
        StructField("category", StringType()),
        StructField("device_type", StringType()),
        StructField("country", StringType()),
    ])
    
    # Parse events
    events = df.select(
        from_json(col("value").cast("string"), schema).alias("event"),
        col("timestamp").alias("kafka_timestamp")
    ).select("event.*", "kafka_timestamp")
    
    # Add event time
    events = events.withColumn(
        "event_time",
        to_timestamp(col("timestamp") / 1000)
    )
    
    # 1. Events per minute by type
    events_per_minute = events \
        .withWatermark("event_time", "1 minute") \
        .groupBy(
            window(col("event_time"), "1 minute"),
            col("event_type")
        ) \
        .agg(
            count("*").alias("event_count")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("event_type"),
            col("event_count")
        )
    
    # 2. Revenue by category (5-minute windows)
    revenue_by_category = events \
        .filter(col("event_type") == "PURCHASE") \
        .filter(col("price").isNotNull()) \
        .withWatermark("event_time", "5 minutes") \
        .groupBy(
            window(col("event_time"), "5 minutes"),
            col("category")
        ) \
        .agg(
            sum("price").alias("total_revenue"),
            count("*").alias("purchase_count"),
            avg("price").alias("avg_price")
        ) \
        .select(
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            col("category"),
            col("total_revenue"),
            col("purchase_count"),
            col("avg_price")
        )
    
    # 3. Device distribution (10-minute windows)
    device_distribution = events \
        .filter(col("device_type").isNotNull()) \
        .withWatermark("event_time", "10 minutes") \
        .groupBy(
            window(col("event_time"), "10 minutes"),
            col("device_type")
        ) \
        .agg(
            count("*").alias("event_count")
        )
    
    # Write streams
    
    # Query 1: Events per minute to console
    query1 = events_per_minute.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .trigger(processingTime="10 seconds") \
        .start()
    
    # Query 2: Revenue to Parquet
    query2 = revenue_by_category.writeStream \
        .outputMode("update") \
        .format("parquet") \
        .option("path", f"{OUTPUT_PATH}/revenue") \
        .option("checkpointLocation", f"{OUTPUT_PATH}/checkpoints/revenue") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    # Query 3: Device distribution to console
    query3 = device_distribution.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", "false") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    # Wait for queries
    query1.awaitTermination()

if __name__ == "__main__":
    calculate_metrics()
```

**2. Test aggregations**

Terminal 1 - Producer (higher volume):
```bash
python -c "from kafka_producer import *; p = EcommerceEventProducer(2); p.produce_continuous(50, 300)"
```

Terminal 2 - Spark:
```bash
python src/spark_aggregations.py
```

**3. Check output**
```bash
ls -lh /tmp/ecommerce-analytics/revenue/
```

**Checkpoint**:
- [ ] Windowed aggregations working
- [ ] Metrics calculated in real-time
- [ ] Parquet files written
- [ ] Can see revenue by category

---

### Day 19-21: Storage & Optimization (4-5 hours)

**Objectives**:
- [ ] Implement proper storage strategy
- [ ] Optimize Spark performance
- [ ] Add monitoring

**Tasks**:

**1. Add MinIO for storage**

Update `docker-compose.yml`:
```yaml
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"
    volumes:
      - minio-data:/data

volumes:
  minio-data:
```

**2. Restart**
```bash
docker-compose up -d
```

**3. Create optimized streaming job**

Create `src/spark_streaming_optimized.py`:
```python
"""
Optimized Spark Streaming
Production-ready streaming with proper storage and monitoring
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'ecommerce-events'
MINIO_ENDPOINT = 'localhost:9000'
OUTPUT_BUCKET = 's3a://ecommerce-data'

def create_spark_session():
    return SparkSession.builder \
        .appName("EcommerceStreamingOptimized") \
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.4") \
        .config("spark.hadoop.fs.s3a.endpoint", f"http://{MINIO_ENDPOINT}") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def process_and_store():
    """Process events and store in data lake"""
    
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    
    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .option("maxOffsetsPerTrigger", "1000") \
        .load()
    
    schema = StructType([
        StructField("event_id", StringType()),
        StructField("user_id", StringType()),
        StructField("event_type", StringType()),
        StructField("timestamp", LongType()),
        StructField("session_id", StringType()),
        StructField("product_id", StringType()),
        StructField("product_name", StringType()),
        StructField("price", DoubleType()),
        StructField("category", StringType()),
        StructField("device_type", StringType()),
        StructField("country", StringType()),
    ])
    
    events = df.select(
        from_json(col("value").cast("string"), schema).alias("event")
    ).select("event.*")
    
    # Add derived columns
    events = events \
        .withColumn("event_time", to_timestamp(col("timestamp") / 1000)) \
        .withColumn("event_date", to_date(col("event_time"))) \
        .withColumn("event_hour", hour(col("event_time")))
    
    # Write to data lake (partitioned by date and hour)
    query = events.writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", f"{OUTPUT_BUCKET}/events/raw") \
        .option("checkpointLocation", f"{OUTPUT_BUCKET}/checkpoints/raw-events") \
        .partitionBy("event_date", "event_hour") \
        .trigger(processingTime="30 seconds") \
        .start()
    
    query.awaitTermination()

if __name__ == "__main__":
    process_and_store()
```

**4. Create bucket in MinIO**
- Open http://localhost:9001
- Login: minioadmin / minioadmin
- Create bucket: `ecommerce-data`

**5. Run optimized job**
```bash
python src/spark_streaming_optimized.py
```

**Checkpoint**:
- [ ] Data written to MinIO
- [ ] Partitioned by date and hour
- [ ] Parquet format used
- [ ] Adaptive query execution enabled

---

## 📊 Week 3 Checkpoint

**What you should have**:
- [x] Spark Streaming reading from Kafka
- [x] Real-time aggregations (windowed)
- [x] Data stored in Parquet format
- [x] MinIO as data lake
- [x] Optimized Spark configuration

**Interview talking point**:
"I built a Spark Structured Streaming pipeline that processes e-commerce events in real-time. It calculates windowed aggregations like revenue per category and events per minute, then stores the results in Parquet format on a data lake with proper partitioning by date and hour for efficient querying."

---

## **PHASE 4: Visualization & Deployment** ⏱️ Week 4 (Days 22-28)

### Day 22-23: Dashboard with Metabase (3 hours)

**Objectives**:
- [ ] Set up Metabase
- [ ] Connect to data lake
- [ ] Build dashboards

**Tasks**:

**1. Add Metabase to docker-compose**
```yaml
  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: h2
      MB_DB_FILE: /metabase-data/metabase.db
    volumes:
      - metabase-data:/metabase-data

volumes:
  metabase-data:
```

**2. Setup Metabase**
- Open http://localhost:3000
- Create admin account
- Skip data source for now

**3. Query data with DuckDB**

Create `src/query_data.py`:
```python
"""
Query analytics data using DuckDB
"""

import duckdb

# Connect to DuckDB
conn = duckdb.connect()

# Query Parquet files
query = """
SELECT 
    event_date,
    event_type,
    COUNT(*) as event_count
FROM read_parquet('/tmp/ecommerce-analytics/revenue/*.parquet')
GROUP BY event_date, event_type
ORDER BY event_date DESC, event_count DESC
"""

result = conn.execute(query).fetchdf()
print(result)
```

**Checkpoint**:
- [ ] Metabase running
- [ ] Can query Parquet files
- [ ] Basic dashboard created

---

### Day 24-25: End-to-End Testing (3 hours)

**Objectives**:
- [ ] Test entire pipeline
- [ ] Verify data quality
- [ ] Measure performance

**Tasks**:

**1. Create integration test**

Create `src/test_pipeline.py`:
```python
"""
Integration test for the entire pipeline
"""

import time
import subprocess
from kafka_producer import EcommerceEventProducer

def test_pipeline():
    """Test end-to-end pipeline"""
    
    print("Starting pipeline test...")
    
    # 1. Produce events
    print("\n1. Producing 1000 events...")
    producer = EcommerceEventProducer(schema_version=2)
    producer.produce_batch(1000)
    print("✅ Events produced")
    
    # Wait for processing
    print("\n2. Waiting for processing...")
    time.sleep(30)
    
    # 3. Verify data
    print("\n3. Verifying data in storage...")
    # Add verification logic
    
    print("\n✅ Pipeline test complete!")

if __name__ == "__main__":
    test_pipeline()
```

**2. Load test**

Create `src/load_test.py`:
```python
"""
Load test the pipeline
"""

from kafka_producer import EcommerceEventProducer
import time

def run_load_test(events_per_second: int, duration_seconds: int):
    """Run load test"""
    
    print(f"Load test: {events_per_second} events/sec for {duration_seconds} seconds")
    
    producer = EcommerceEventProducer(schema_version=2)
    producer.produce_continuous(events_per_second, duration_seconds)
    
    print("Load test complete")

if __name__ == "__main__":
    # Test with different loads
    run_load_test(10, 60)    # Light load
    # run_load_test(100, 60)  # Medium load
    # run_load_test(1000, 60) # Heavy load
```

**Checkpoint**:
- [ ] Pipeline handles 100 events/sec
- [ ] No data loss
- [ ] Latency acceptable (<5 seconds)

---

### Day 26-27: Documentation & GitHub (3 hours)

**Objectives**:
- [ ] Complete README
- [ ] Add architecture diagram
- [ ] Prepare for demo

**Tasks**:

**1. Create comprehensive README.md**
```markdown
# E-commerce Real-Time Analytics Pipeline

Production-grade streaming pipeline for e-commerce event analytics.

## Architecture

[Add diagram]

## Features
- Real-time event processing with Kafka
- Schema evolution with Avro & Schema Registry
- Stream processing with Spark Structured Streaming
- Data lake storage with MinIO
- Real-time dashboards with Metabase

## Tech Stack
- Apache Kafka 7.5.0
- Schema Registry
- Apache Spark 3.5.0
- MinIO
- Metabase
- Python 3.11

## Quick Start
[Add instructions]

## Schema Evolution
[Explain how schema evolved]

## Performance
- Throughput: 1000 events/second
- Latency: <5 seconds end-to-end
- Storage: Partitioned Parquet

## Interview Highlights
- Backward-compatible schema evolution
- Exactly-once semantics
- Windowed aggregations
- Production monitoring
```

**2. Add architecture diagram**
- Use draw.io or similar
- Show data flow
- Include all components

**3. Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit: E-commerce streaming pipeline"
git remote add origin <your-repo>
git push -u origin main
```

**Checkpoint**:
- [ ] README complete and professional
- [ ] Architecture diagram clear
- [ ] Code well-commented
- [ ] Pushed to GitHub

---

### Day 28: Interview Preparation (2 hours)

**Objectives**:
- [ ] Prepare demo script
- [ ] Practice explaining architecture
- [ ] Prepare for questions

**Interview Prep Checklist**:

**Demo Script** (5 minutes):
1. Show architecture diagram (30 sec)
2. Start producer (30 sec)
3. Show Kafka UI - messages flowing (1 min)
4. Show Spark UI - jobs running (1 min)
5. Show MinIO - data stored (1 min)
6. Show dashboard - real-time metrics (1 min)
7. Explain schema evolution (1 min)

**Key Talking Points**:
- [ ] "Built real-time pipeline processing e-commerce events"
- [ ] "Implemented backward-compatible schema evolution"
- [ ] "Used Kafka for ingestion, Spark for processing"
- [ ] "Achieved 1000 events/sec throughput"
- [ ] "Exactly-once semantics with idempotent producers"
- [ ] "Windowed aggregations for real-time metrics"
- [ ] "Partitioned Parquet for efficient querying"

**Common Interview Questions**:
1. **Why Kafka?** → High throughput, durability, decoupling
2. **Why Schema Registry?** → Schema evolution, compatibility
3. **Why Spark Streaming?** → Mature, SQL support, integrations
4. **How did you ensure data quality?** → Schema validation, monitoring
5. **What if Kafka goes down?** → Replication, monitoring, alerts
6. **How did you test?** → Unit tests, integration tests, load tests
7. **Biggest challenge?** → Schema evolution strategy
8. **What would you improve?** → Add alerting, better monitoring, CI/CD

---

## 📊 Project Completion Checklist

**Technical Components**:
- [ ] Kafka cluster running
- [ ] Schema Registry with v1 and v2 schemas
- [ ] Event generator producing realistic data
- [ ] Kafka producer with Avro serialization
- [ ] Kafka consumer with analytics
- [ ] Spark Streaming job
- [ ] Real-time aggregations
- [ ] MinIO data lake
- [ ] Parquet storage with partitioning
- [ ] Metabase dashboard

**Documentation**:
- [ ] README.md complete
- [ ] Architecture diagram
- [ ] Schema evolution guide
- [ ] Code comments
- [ ] API documentation

**Quality**:
- [ ] No critical bugs
- [ ] Proper error handling
- [ ] Logging implemented
- [ ] Performance tested
- [ ] Load tested (100+ events/sec)

**Portfolio Readiness**:
- [ ] GitHub repo public
- [ ] Professional README
- [ ] Demo ready (5 min)
- [ ] Can explain every component
- [ ] Screenshots/video of running system

---

## 🎯 Success Metrics

By completing this project, you will:

**Skills Demonstrated**:
✅ Kafka expertise (producers, consumers, topics)
✅ Schema Registry & Avro
✅ Backward-compatible schema evolution
✅ Spark Structured Streaming
✅ Windowed aggregations
✅ Data lake architecture
✅ Real-time analytics
✅ Production patterns (exactly-once, monitoring)

**Interview Readiness**:
✅ 15-minute deep technical discussion ready
✅ Can whiteboard the architecture
✅ Can explain tradeoffs
✅ Can discuss alternatives
✅ Real production experience to reference

**Portfolio Impact**:
✅ Aligns with e-commerce background
✅ Shows modern data engineering stack
✅ Demonstrates end-to-end thinking
✅ Production-quality code
✅ Proper documentation

---

## 💡 Tips for Success

**Daily Habits**:
- [ ] Commit code daily
- [ ] Document as you build
- [ ] Test each component before moving on
- [ ] Take screenshots of working features
- [ ] Write down challenges and solutions

**Time Management**:
- Weekdays: 1.5-2 hours focused work
- Weekends: 3 hours with breaks
- If stuck >30 min, move on and come back

**Learning Approach**:
- Understand WHY before coding
- Read official docs
- Don't copy-paste blindly
- Experiment with parameters
- Break things intentionally to learn

**Interview Prep**:
- Practice explaining to non-technical person
- Record yourself doing demo
- Prepare for "why not X instead of Y" questions
- Have a failure story ready (what went wrong, how you fixed it)

---

## 🚀 Next Steps After Completion

**Enhancements** (if time permits):
1. Add Airflow for orchestration
2. Implement alerting with Prometheus/Grafana
3. Add data quality checks (Great Expectations)
4. Implement exactly-once with transactions
5. Add CDC from PostgreSQL
6. Deploy to cloud (AWS/GCP)
7. Add CI/CD pipeline
8. Implement data lineage tracking

**Related Projects**:
1. Build batch version using Airflow + Spark
2. Add ML model for recommendation
3. Implement A/B testing framework
4. Build customer segmentation pipeline

---

## 📚 Resources

**Kafka**:
- Confluent Documentation
- Kafka: The Definitive Guide (book)

**Spark**:
- Spark Structured Streaming Guide
- Learning Spark (book)

**Schema Evolution**:
- Confluent Schema Registry docs
- Avro specification

**Community**:
- r/dataengineering
- Confluent Community Slack
- Stack Overflow

---

## ✅ Final Checklist Before Interview

**1 Day Before**:
- [ ] Test entire pipeline end-to-end
- [ ] Ensure all services start cleanly
- [ ] Practice demo (5 minutes exactly)
- [ ] Review architecture diagram
- [ ] Read your own code comments

**During Interview**:
- [ ] Stay calm, it's just code
- [ ] Explain business value first, then tech
- [ ] Be honest about what you don't know
- [ ] Show enthusiasm for data engineering
- [ ] Ask questions about their stack

---

**Good luck with your project! 🚀**

Remember: This project shows you can build production-quality data pipelines. That's exactly what 5 YoE roles need.