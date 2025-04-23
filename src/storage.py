"""
Storage module for PyPzza - Handles data persistence for pizza orders.

This module provides functions to:
- Load orders from a JSON file
- Save orders to a JSON file
- Add, update, get, and delete orders
- Ensure storage directory exists

File Structure:
data/orders.json - Stores orders as a JSON array
"""
# json for working with JSON data (like JSON object in JS)
import json
# os for file/directory operations (like fs/path in Node.js)
import os
# Type hints (like TypeScript types)
from typing import List, Dict, Any

# Constants (like const in JS)
# os.path.join is like path.join in Node.js
# It creates correct path for any OS: 'data/orders.json' or 'data\orders.json'
ORDERS_FILE = os.path.join("data", "orders.json")

def ensure_storage_exists() -> None:
    """
    Ensure the data directory and orders file exist.
    Similar to Node.js:
    ```js
    if (!fs.existsSync('data')) {
        fs.mkdirSync('data', { recursive: true });
    }
    if (!fs.existsSync('data/orders.json')) {
        fs.writeFileSync('data/orders.json', '[]');
    }
    ```
    """
    # Create directory if it doesn't exist (exist_ok=True prevents errors)
    os.makedirs("data", exist_ok=True)
    
    # Create file with empty array if it doesn't exist
    if not os.path.exists(ORDERS_FILE):
        # 'with' is like try-with-resources in Java
        # Automatically closes file when done
        with open(ORDERS_FILE, "w") as f:
            json.dump([], f)  # Write empty array

def load_orders() -> List[Dict[str, Any]]:
    """
    Load all orders from storage.
    JS equivalent:
    ```js
    try {
        return JSON.parse(fs.readFileSync('data/orders.json'));
    } catch (e) {
        console.warn('Invalid JSON file');
        return [];
    }
    ```
    """
    ensure_storage_exists()
    try:
        with open(ORDERS_FILE, "r") as f:  # 'r' mode = read
            return json.load(f)  # Like JSON.parse()
    except json.JSONDecodeError:  # Specific error for invalid JSON
        print("Warning: Invalid JSON file. Creating new empty orders list.")
        return []

def save_orders(orders: List[Dict[str, Any]]) -> None:
    """
    Save orders to storage.
    JS equivalent:
    ```js
    fs.writeFileSync(
        'data/orders.json',
        JSON.stringify(orders, null, 2)
    );
    ```
    """
    ensure_storage_exists()
    with open(ORDERS_FILE, "w") as f:  # 'w' mode = write (overwrites file)
        # indent=2 makes the JSON file pretty (like JSON.stringify(x, null, 2))
        json.dump(orders, f, indent=2)

def add_order(order: Dict[str, Any]) -> None:
    """
    Add a new order to storage.
    JS equivalent:
    ```js
    const orders = loadOrders();
    orders.push(order);
    saveOrders(orders);
    ```
    """
    orders = load_orders()
    orders.append(order)  # append is like Array.push()
    save_orders(orders)

def update_order(order_id: str, updated_order: Dict[str, Any]) -> bool:
    """
    Update an existing order.
    JS equivalent:
    ```js
    const orders = loadOrders();
    const index = orders.findIndex(o => o.id === orderId);
    if (index !== -1) {
        orders[index] = updatedOrder;
        saveOrders(orders);
        return true;
    }
    return false;
    ```
    """
    orders = load_orders()
    # enumerate gives index and value (like Array.entries())
    for i, order in enumerate(orders):
        if order["id"] == order_id:
            orders[i] = updated_order
            save_orders(orders)
            return True
    return False

def get_order(order_id: str) -> Dict[str, Any] | None:
    """
    Get an order by ID.
    JS equivalent:
    ```js
    const orders = loadOrders();
    return orders.find(o => o.id === orderId) || null;
    ```
    """
    orders = load_orders()
    # Simple for loop instead of find() method
    for order in orders:
        if order["id"] == order_id:
            return order
    return None  # None is like null in JS

def delete_order(order_id: str) -> bool:
    """
    Delete an order by ID.
    JS equivalent:
    ```js
    const orders = loadOrders();
    const initialLength = orders.length;
    const newOrders = orders.filter(o => o.id !== orderId);
    if (newOrders.length < initialLength) {
        saveOrders(newOrders);
        return true;
    }
    return false;
    ```
    """
    orders = load_orders()
    initial_length = len(orders)
    # List comprehension: shorter way to filter list
    # [order for order in orders if condition]
    # is like orders.filter(order => condition)
    orders = [order for order in orders if order["id"] != order_id]
    if len(orders) < initial_length:  # Check if we removed an order
        save_orders(orders)
        return True
    return False 