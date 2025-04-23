# PyPzza - Pizza Order Management CLI

A simple command-line application to manage pizza orders, built with Python.

## Project Overview

PyPzza is a beginner-friendly CLI application that helps manage pizza orders. It's designed to practice Python fundamentals while creating something useful.

### Core Features (MVP)

- Create, read, update, and delete pizza orders
- Store orders in a JSON file (simple data persistence)
- Basic order status management (pending, preparing, ready)
- Simple price calculation

## Technical Design

### Data Models

```python
# Example structure of our data
Order = {
    "id": str,              # Unique order ID
    "customer_name": str,   # Name of customer
    "pizza_size": str,      # Small, Medium, Large
    "toppings": list,       # List of toppings
    "status": str,          # Order status
    "price": float,         # Total price
    "created_at": str       # Order creation timestamp
}
```

### File Structure

```
pypzza/
├── data/
│   └── orders.json        # Store orders
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── order.py          # Order management
│   └── storage.py        # Data persistence
├── README.md
├── requirements.txt
└── .gitignore
```

### Core Components

1. **Main Menu (main.py)**

   - Display options to user
   - Handle user input
   - Route to appropriate functions

2. **Order Management (order.py)**

   - Create new orders
   - Update order status
   - Calculate prices
   - Validate order data

3. **Storage (storage.py)**
   - Save orders to JSON
   - Load orders from JSON
   - Basic data persistence

### Basic Workflows

1. **Creating an Order**

   ```
   1. Get customer name
   2. Select pizza size
   3. Choose toppings
   4. Calculate price
   5. Save order
   ```

2. **Viewing Orders**

   ```
   1. Load orders from storage
   2. Display formatted list
   3. Option to view details
   ```

3. **Updating Order Status**
   ```
   1. Select order by ID
   2. Choose new status
   3. Save updated order
   ```

## Implementation Plan

### Phase 1: Basic Structure

- [x] Set up project structure
- [x] Create main menu interface
- [x] Implement basic order creation
- [x] Set up JSON storage

### Phase 2: Core Features

- [x] Add order management (CRUD operations)
- [x] Implement price calculation
- [x] Add order status management
- [x] Basic error handling

### Phase 3: Enhancements (Optional)

- [x] Add order validation
- [ ] Implement search/filter
- [ ] Add simple reporting
- [ ] Improve user interface
  - [ ] Add color themes
  - [ ] Add progress bars for operations
  - [ ] Add order history visualization

## Getting Started

1. Create virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python src/main.py
   ```

## Dependencies

- `rich`: For better CLI formatting
- `uuid`: For generating unique order IDs
- `json`: For data storage (built-in)
- `datetime`: For timestamp handling (built-in)

## Learning Goals

This project will help practice:

- Python basics (functions, loops, conditionals)
- Working with dictionaries and lists
- File I/O operations
- Basic error handling
- Simple data validation
- JSON data handling
