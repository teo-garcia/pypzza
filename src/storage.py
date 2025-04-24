"""
Storage module for PyPzza - Handles data persistence for pizza orders.

What is this file?
-----------------
This module manages our order data storage. It:
1. Saves orders to a JSON file
2. Loads orders when needed
3. Handles CRUD operations (Create, Read, Update, Delete)

Why JSON?
--------
JSON (JavaScript Object Notation) is:
- Human-readable text format
- Works in many programming languages
- Built into Python (like in JavaScript)
"""

# Standard library imports
# ----------------------
import json         # JSON handling (like JSON.parse/stringify)
import os          # File operations (like fs in Node.js)
from typing import List, Dict, Any  # Type hints (like TypeScript)

# File path constant
# ----------------
# os.path.join is smart about creating paths:
# - Windows: Uses backslashes (data\orders.json)
# - Mac/Linux: Uses forward slashes (data/orders.json)
# This way our code works on any computer!
ORDERS_FILE = os.path.join("data", "orders.json")

def ensure_storage_exists() -> None:
    """
    Creates storage folder and file if missing.
    
    Similar to:
    - mkdir -p data
    - touch data/orders.json
    """
    # os.makedirs is like 'mkdir -p' in terminal
    # exist_ok=True means:
    # - If folder exists: do nothing
    # - If folder missing: create it
    os.makedirs("data", exist_ok=True)
    
    # os.path.exists checks if a file/folder exists
    # Like fs.existsSync() in Node.js
    if not os.path.exists(ORDERS_FILE):
        # 'with' statement is a special Python feature that:
        # 1. Opens the file
        # 2. Lets us work with it
        # 3. Automatically closes it when we're done
        # This prevents memory leaks and other problems!
        with open(ORDERS_FILE, "w") as file:  # "w" means "write mode"
            # json.dump converts Python data to JSON and writes it
            # It's like JSON.stringify() + writeFileSync()
            json.dump([], file)  # Start with empty array

def load_orders() -> List[Dict[str, Any]]:
    """
    Reads all orders from storage.
    
    Returns:
        List of order dictionaries
    
    Note: Returns empty list if file is corrupted
    Similar to: JSON.parse(readFileSync())
    """
    ensure_storage_exists()
    
    try:
        # "r" means "read mode"
        with open(ORDERS_FILE, "r") as file:
            # json.load reads JSON and converts to Python data
            # It's like JSON.parse(fileContents)
            return json.load(file)
    except json.JSONDecodeError:
        # This error happens if the JSON is invalid
        # Instead of crashing, we:
        # 1. Show a warning
        # 2. Return an empty list
        print("Warning: Invalid JSON file. Creating new empty orders list.")
        return []

def save_orders(orders: List[Dict[str, Any]]) -> None:
    """
    Writes orders to storage file.
    
    Args:
        orders: List of order dictionaries
    
    Note: Creates pretty JSON with indent=2
    Similar to: writeFileSync(JSON.stringify(orders, null, 2))
    """
    ensure_storage_exists()
    
    with open(ORDERS_FILE, "w") as file:
        # indent=2 makes the JSON file pretty and readable:
        # {
        #   "key": "value",
        #   "array": [
        #     1,
        #     2
        #   ]
        # }
        json.dump(orders, file, indent=2)

def add_order(order: Dict[str, Any]) -> None:
    """
    Adds new order to storage.
    
    Args:
        order: Order dictionary to add
    
    Note: Like Array.push() in JavaScript
    """
    orders = load_orders()
    # append() adds item to end of list
    # Like array.push() in JavaScript
    orders.append(order)
    save_orders(orders)

def update_order(order_id: str, updated_order: Dict[str, Any]) -> bool:
    """
    Updates existing order.
    
    Args:
        order_id: ID of order to update
        updated_order: New order data
    
    Returns:
        True if found and updated
        False if not found
    
    Note: Like Array.findIndex() in JavaScript
    """
    orders = load_orders()
    
    # enumerate gives us both position and value:
    # for i, x in enumerate(['a', 'b']):
    #   i will be 0, 1
    #   x will be 'a', 'b'
    for position, order in enumerate(orders):
        # Check if this is the order we want
        if order["id"] == order_id:
            # Replace the old order with the new one
            orders[position] = updated_order
            save_orders(orders)
            return True
    
    # If we get here, we didn't find the order
    return False

def get_order(order_id: str) -> Dict[str, Any] | None:
    """
    Finds order by ID.
    
    Args:
        order_id: ID to search for
    
    Returns:
        Order dictionary if found
        None if not found
    
    Note: Like Array.find() in JavaScript
    """
    orders = load_orders()
    
    # Simple loop to find matching order
    # Like array.find() in JavaScript
    for order in orders:
        if order["id"] == order_id:
            return order
    
    # None is like null in JavaScript
    return None

def delete_order(order_id: str) -> bool:
    """
    Removes order by ID.
    
    Args:
        order_id: ID to delete
    
    Returns:
        True if found and deleted
        False if not found
    
    Note: Uses list comprehension (like Array.filter)
    """
    orders = load_orders()
    # Remember initial count to check if we deleted anything
    initial_count = len(orders)
    
    # This is a list comprehension - a shorter way to filter
    # It creates a new list with only orders that DON'T match the ID
    # Long way:
    #   new_orders = []
    #   for order in orders:
    #       if order["id"] != order_id:
    #           new_orders.append(order)
    orders = [order for order in orders if order["id"] != order_id]
    
    # If we have fewer orders now, we found and deleted one
    if len(orders) < initial_count:
        save_orders(orders)
        return True
    
    return False 