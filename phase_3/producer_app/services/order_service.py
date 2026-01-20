import random
from api.users_api import fetch_users

ORDER_STATUS = ["created", "shipped", "paid"]

def create_order_data():
    users = fetch_users()
    user = random.choice(users)

    return {
        "order_id": random.randint(1000, 9999),
        "user_id": user["id"],
        "customer_id": random.randint(100, 999),
        "amount": round(random.uniform(10.0, 500.0), 2),
        "user_name": user["name"],
        "user_email": user["email"],
        "currency": "INR",
        "status": random.choice(ORDER_STATUS)
    }
