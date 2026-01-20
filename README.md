# Kafka Learning Environment 🚀

Complete Docker setup for learning Apache Kafka with KRaft mode (no ZooKeeper!), Schema Registry, and Kafka UI.

## 📦 What's Included

| Component | Port | Purpose |
|-----------|------|---------|
| **Kafka Broker (KRaft)** | 9092 | Main Kafka broker |
| **Schema Registry** | 8081 | Avro/JSON/Protobuf schema management (FREE) |
| **Kafka UI** | 8080 | Web interface to observe topics, messages, consumers |
| **REST Proxy** | 8082 | HTTP API for Kafka operations |

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose installed
- At least 4GB RAM allocated to Docker

### Start the Environment

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f kafka
docker-compose logs -f schema-registry
docker-compose logs -f kafka-ui

# Stop everything
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### Access the Services

1. **Kafka UI**: http://localhost:8080
   - View topics, partitions, messages
   - Monitor consumer groups
   - Browse schemas

2. **Schema Registry**: http://localhost:8081
   - API endpoint for schema operations

3. **Kafka Broker**: localhost:9092
   - For producer/consumer applications

## 📚 Learning Exercises

### Exercise 1: Create Your First Topic

```bash
# Enter the Kafka container
docker exec -it kafka bash

# Create a topic with 3 partitions
kafka-topics --create \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# List all topics
kafka-topics --list \
  --bootstrap-server localhost:9092

# Describe the topic
kafka-topics --describe \
  --topic user-events \
  --bootstrap-server localhost:9092

# Expected output:
# Topic: user-events    PartitionCount: 3    ReplicationFactor: 1
# Topic: user-events    Partition: 0    Leader: 1    Replicas: 1    Isr: 1
# Topic: user-events    Partition: 1    Leader: 1    Replicas: 1    Isr: 1
# Topic: user-events    Partition: 2    Leader: 1    Replicas: 1    Isr: 1
```

### Exercise 2: Produce Messages (Console Producer)

```bash
# Simple producer (no key)
kafka-console-producer \
  --topic user-events \
  --bootstrap-server localhost:9092

# Type messages and press Enter:
# {"userId": "123", "action": "login"}
# {"userId": "456", "action": "purchase"}
# Press Ctrl+C to exit

# Producer with keys (for partition control)
kafka-console-producer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --property "parse.key=true" \
  --property "key.separator=:"

# Type messages as key:value
# user-123:{"action": "login"}
# user-456:{"action": "purchase"}
# user-123:{"action": "logout"}
# All user-123 messages will go to the same partition!
```

### Exercise 3: Consume Messages (Console Consumer)

```bash
# Consume from beginning
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --from-beginning

# Consume with keys
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --property print.key=true \
  --property key.separator=" : "

# Consume with offset, partition, and timestamp
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --property print.offset=true \
  --property print.partition=true \
  --property print.timestamp=true

# Example output:
# CreateTime:1704153600000    Partition:0    Offset:0    user-123 : {"action": "login"}
# CreateTime:1704153601000    Partition:2    Offset:0    user-456 : {"action": "purchase"}
```

### Exercise 4: Understanding Partitions

```bash
# Create topic with different partition counts
kafka-topics --create \
  --topic orders-1-partition \
  --bootstrap-server localhost:9092 \
  --partitions 1

kafka-topics --create \
  --topic orders-5-partitions \
  --bootstrap-server localhost:9092 \
  --partitions 5

# Compare in Kafka UI at http://localhost:8080
# Observe how messages are distributed across partitions
```

### Exercise 5: Consumer Groups and Offsets

```bash
# Consumer 1 (in terminal 1)
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --from-beginning

# Consumer 2 (in terminal 2 - same group)
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --from-beginning

# Observe: Each consumer in the group gets different partitions

# Check consumer group details
kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --describe

# Expected output shows LAG (uncommitted messages)
# GROUP              TOPIC         PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG
# my-consumer-group  user-events   0          10              10              0
# my-consumer-group  user-events   1          8               8               0
# my-consumer-group  user-events   2          12              12              0

# Reset offsets to beginning
kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --topic user-events \
  --reset-offsets \
  --to-earliest \
  --execute

# Reset to specific offset
kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --group my-consumer-group \
  --topic user-events \
  --reset-offsets \
  --to-offset 5 \
  --execute
```

### Exercise 6: Schema Registry (Avro)

```bash
# Register a schema
curl -X POST http://localhost:8081/subjects/user-events-value/versions \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schema": "{\"type\":\"record\",\"name\":\"User\",\"fields\":[{\"name\":\"userId\",\"type\":\"string\"},{\"name\":\"action\",\"type\":\"string\"},{\"name\":\"timestamp\",\"type\":\"long\"}]}"
  }'

# List all subjects
curl http://localhost:8081/subjects

# Get all versions of a subject
curl http://localhost:8081/subjects/user-events-value/versions

# Get specific version
curl http://localhost:8081/subjects/user-events-value/versions/1

# Check compatibility
curl -X POST http://localhost:8081/compatibility/subjects/user-events-value/versions/latest \
  -H "Content-Type: application/vnd.schemaregistry.v1+json" \
  -d '{
    "schema": "{\"type\":\"record\",\"name\":\"User\",\"fields\":[{\"name\":\"userId\",\"type\":\"string\"},{\"name\":\"action\",\"type\":\"string\"},{\"name\":\"timestamp\",\"type\":\"long\"},{\"name\":\"email\",\"type\":[\"null\",\"string\"],\"default\":null}]}"
  }'

# View schemas in Kafka UI: http://localhost:8080
```

### Exercise 7: Topic Configuration

```bash
# Create topic with custom configuration
kafka-topics --create \
  --topic logs-compressed \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --config compression.type=gzip \
  --config retention.ms=3600000 \
  --config segment.ms=600000

# View topic configuration
kafka-configs --describe \
  --topic logs-compressed \
  --bootstrap-server localhost:9092

# Modify topic configuration
kafka-configs --alter \
  --topic logs-compressed \
  --bootstrap-server localhost:9092 \
  --add-config retention.ms=7200000

# Increase partitions (cannot decrease!)
kafka-topics --alter \
  --topic logs-compressed \
  --bootstrap-server localhost:9092 \
  --partitions 5
```

### Exercise 8: Message Keys and Partitioning

```bash
# Produce messages with different keys to observe partitioning
kafka-console-producer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --property "parse.key=true" \
  --property "key.separator=|"

# Send these messages:
# alice|{"event":"login","time":"10:00"}
# bob|{"event":"login","time":"10:01"}
# alice|{"event":"view_product","time":"10:02"}
# charlie|{"event":"login","time":"10:03"}
# alice|{"event":"purchase","time":"10:05"}
# bob|{"event":"purchase","time":"10:06"}

# In another terminal, consume showing partitions:
kafka-console-consumer \
  --topic user-events \
  --bootstrap-server localhost:9092 \
  --from-beginning \
  --property print.key=true \
  --property print.partition=true \
  --property key.separator=" -> "

# Observe: All "alice" messages go to same partition!
```

## 🧪 Practice Scenarios

### Scenario 1: E-commerce Order Pipeline

```bash
# Create topics for order lifecycle
kafka-topics --create --topic orders.created --bootstrap-server localhost:9092 --partitions 5
kafka-topics --create --topic orders.paid --bootstrap-server localhost:9092 --partitions 5
kafka-topics --create --topic orders.shipped --bootstrap-server localhost:9092 --partitions 5
kafka-topics --create --topic orders.delivered --bootstrap-server localhost:9092 --partitions 5

# Use order ID as key to maintain ordering per order
# Produce to orders.created with key=order-id
```

### Scenario 2: Real-time Analytics

```bash
# Create topics
kafka-topics --create --topic pageviews --bootstrap-server localhost:9092 --partitions 10
kafka-topics --create --topic user-sessions --bootstrap-server localhost:9092 --partitions 10
kafka-topics --create --topic analytics-results --bootstrap-server localhost:9092 --partitions 3 \
  --config cleanup.policy=compact

# Use user ID as key for sessionization
```

### Scenario 3: Log Aggregation

```bash
# Create topic with short retention
kafka-topics --create --topic application-logs --bootstrap-server localhost:9092 \
  --partitions 20 \
  --config retention.ms=3600000 \
  --config compression.type=lz4 \
  --config segment.ms=300000

# Test with high-volume log production
```

## 🔍 Monitoring with Kafka UI

Navigate to http://localhost:8080 and explore:

1. **Brokers**: View cluster health, configuration
2. **Topics**: 
   - See partition distribution
   - View messages in real-time
   - Inspect message headers, keys, values
3. **Consumers**:
   - Monitor consumer lag
   - See partition assignments
   - Track offset commits
4. **Schema Registry**:
   - Browse registered schemas
   - View schema evolution history
   - Check compatibility modes

## 🐛 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs kafka

# Common issue: Port already in use
# Solution: Change ports in docker-compose.yml or kill process using port

# On Mac/Linux:
lsof -i :9092
kill -9 <PID>

# On Windows:
netstat -ano | findstr :9092
taskkill /PID <PID> /F
```

### Kafka UI shows "Connection refused"
```bash
# Wait for Kafka to be fully ready (health checks)
docker-compose ps

# All services should show "healthy"
# If not, wait 30-60 seconds after docker-compose up
```

### Out of memory
```bash
# Increase Docker memory in Docker Desktop settings
# Recommended: 4GB minimum, 8GB optimal

# Or reduce Kafka memory in docker-compose.yml:
# Add to kafka environment:
# KAFKA_HEAP_OPTS: "-Xmx512M -Xms512M"
```

## 📖 Useful Commands Cheat Sheet

```bash
# List topics
kafka-topics --list --bootstrap-server localhost:9092

# Delete topic
kafka-topics --delete --topic <topic-name> --bootstrap-server localhost:9092

# Get topic offset range
kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic user-events

# List consumer groups
kafka-consumer-groups --list --bootstrap-server localhost:9092

# Delete consumer group
kafka-consumer-groups --delete --group <group-name> --bootstrap-server localhost:9092

# Performance test producer
kafka-producer-perf-test \
  --topic perf-test \
  --num-records 100000 \
  --record-size 1024 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092

# Performance test consumer
kafka-consumer-perf-test \
  --topic perf-test \
  --bootstrap-server localhost:9092 \
  --messages 100000
```

## 🎯 Next Steps

1. **Day 1**: Complete Exercises 1-4 (Topics, Partitions, Basic Produce/Consume)
2. **Day 2**: Complete Exercises 5-6 (Consumer Groups, Schema Registry)
3. **Day 3**: Complete Exercises 7-8 (Configurations, Partitioning Strategies)
4. **Day 4**: Build a simple producer/consumer app in your language of choice
5. **Day 5**: Practice with real-world scenarios

## 📚 Additional Resources

- **Kafka Documentation**: https://kafka.apache.org/documentation/
- **Confluent Schema Registry Docs**: https://docs.confluent.io/platform/current/schema-registry/
- **Kafka UI GitHub**: https://github.com/provectus/kafka-ui

## 🧹 Cleanup

```bash
# Stop all services
docker-compose down

# Remove all data (fresh start)
docker-compose down -v

# Remove images (if needed)
docker-compose down --rmi all
```

## ⚠️ Important Notes

- **KRaft Mode**: This setup uses Kafka's new KRaft consensus protocol (no ZooKeeper!)
- **Schema Registry**: FREE under Confluent Community License
- **Single Broker**: This is a single-broker setup for learning
- **Replication Factor**: Set to 1 (would be 3+ in production)
- **Auto-create Topics**: Enabled for convenience (disable in production)

Happy Learning! 🎓