"""
Order management module for PyPzza - Handles order creation and validation.

This module provides:
- Order data validation
- Price calculation
- Order status management
- Business rules enforcement

Key Components:
- PIZZA_SIZES: Available sizes and their base prices
- AVAILABLE_TOPPINGS: List of allowed toppings
- ORDER_STATES: Valid order status progression
"""
# datetime for working with dates (like Date in JS)
from datetime import datetime
# uuid for generating unique IDs (like crypto.randomUUID() in JS)
import uuid
# Type hints (like TypeScript types)
from typing import List, Dict, Any

# Dictionary (like object literal in JS)
# const PIZZA_SIZES = {
#   small: 10.99,
#   medium: 14.99,
#   large: 18.99
# };
PIZZA_SIZES = {
    "small": 10.99,
    "medium": 14.99,
    "large": 18.99
}

# List (like array in JS)
# const AVAILABLE_TOPPINGS = [
#   'cheese', 'pepperoni', ...
# ];
AVAILABLE_TOPPINGS = [
    "cheese", "pepperoni", "mushrooms", "onions",
    "sausage", "bacon", "green_peppers", "olives"
]

# Constant (like const in JS)
TOPPING_PRICE = 1.50

# List of valid states in order (like enum in TypeScript)
# Must progress through these states in sequence
ORDER_STATES = ["PENDING", "PREPARING", "READY", "DELIVERED"]

def validate_order_data(customer_name: str, size: str, toppings: List[str]) -> None:
    """
    Validate order data against business rules.
    """ 
    # strip() removes whitespace (like trim() in JS)
    if not customer_name.strip():
        raise ValueError("Customer name cannot be empty")
    
    # in checks key existence (like hasOwnProperty or 'in' operator in JS)
    if size not in PIZZA_SIZES:
        raise ValueError(f"Invalid size. Choose from: {list(PIZZA_SIZES.keys())}")
    
    # List comprehension to find invalid toppings
    # Similar to Array.filter() in JS
    invalid_toppings = [t for t in toppings if t not in AVAILABLE_TOPPINGS]
    if invalid_toppings:
        raise ValueError(f"Invalid toppings: {invalid_toppings}. Choose from: {AVAILABLE_TOPPINGS}")

def calculate_price(size: str, toppings: List[str]) -> float:
    """
    Calculate total price based on size and toppings.
    """
    base_price = PIZZA_SIZES[size]
    # len() gets length (like array.length in JS)
    toppings_price = len(toppings) * TOPPING_PRICE
    # round(x, 2) is like Number(x.toFixed(2)) in JS
    return round(base_price + toppings_price, 2)

def create_order(customer_name: str, size: str, toppings: List[str]) -> Dict[str, Any]:
    """
    Create a new order with validated data.
    """
    validate_order_data(customer_name, size, toppings)
    
    # Dictionary (like object in JS)
    return {
        "id": str(uuid.uuid4()),  # Generate UUID (like crypto.randomUUID())
        "customer_name": customer_name.strip(),
        "pizza_size": size,
        "toppings": toppings,
        "status": "PENDING",
        "price": calculate_price(size, toppings),
        # isoformat() is like toISOString() in JS
        "created_at": datetime.now().isoformat()
    }

def validate_status_transition(current_status: str, new_status: str) -> None:
    """
    Validate if the status transition is allowed.
    """
    # index() is like indexOf() in JS
    current_idx = ORDER_STATES.index(current_status)
    new_idx = ORDER_STATES.index(new_status)
    
    # Check if moving one step forward
    if new_idx != current_idx + 1:
        # f-strings are like template literals in JS
        raise ValueError(
            f"Invalid status transition from {current_status} to {new_status}. "
            f"Valid next status: {ORDER_STATES[current_idx + 1]}"
        )

def update_order_status(order: Dict[str, Any], new_status: str) -> Dict[str, Any]:
    """
    Update order status if transition is valid.
    """
    # Check if status is valid
    if new_status not in ORDER_STATES:
        raise ValueError(f"Invalid status. Choose from: {ORDER_STATES}")
    
    # Only validate if status is actually changing
    if order["status"] != new_status:
        validate_status_transition(order["status"], new_status)
        # Update dictionary (like object property in JS)
        order["status"] = new_status
    
    return order 