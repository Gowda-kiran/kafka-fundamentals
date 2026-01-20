from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    user_id: int
    customer_id: int
    amount: float
    user_name: str
    user_email: str
    currency: str
    status: str