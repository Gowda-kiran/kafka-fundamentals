from confluent_kafka import Producer
import os
from dotenv import load_dotenv
from phase_3.products import order_data

load_dotenv()

def generate_order_data():
    import random
    import json
    from datetime import datetime

    order_data = {
        "order_id": random.randint(1000, 9999),
        "customer_id": random.randint(100, 999),
        "amount": round(random.uniform(10.0, 500.0), 2),
        "currency": "USD",
        "timestamp": datetime.utcnow().isoformat()
    }

    with open("orders_data.json", "a") as f:
        f.write(json.dumps(order_data) + "\n")

def produce_message


if __name__ == "__main__":
    
    for i in range(1000):
        
