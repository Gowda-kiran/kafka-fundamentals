from services.order_service import create_order_data
from producer.kafka_producer import send_to_kafka
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
if __name__ == "__main__":
    for i in range(5):
        order = create_order_data()
        logger
        send_to_kafka(order)
