"""
PyPzza - A simple CLI pizza order management system.

This module provides the command-line interface for the PyPzza application.
It uses the Rich library for enhanced terminal output and user interaction.

Key Features:
- Create new orders with custom toppings
- List and manage existing orders
- Update order status
- View detailed order information
- Delete orders
"""
from typing import List
from rich.console import Console     # Rich's main interface for terminal output
from rich.table import Table        # For creating formatted tables
from rich.prompt import Prompt, Confirm  # For user input with validation
from rich import print as rprint    # Enhanced print function with markup

from order import (
    create_order, update_order_status,
    PIZZA_SIZES, AVAILABLE_TOPPINGS, ORDER_STATES
)
import storage

# Create console instance for Rich formatting
console = Console()

def print_menu() -> None:
    """
    Display the main menu with Rich formatting.
    
    Uses:
    - console.print: Rich's formatted output
    - [bold blue]: Rich's markup for styling
    """
    console.print("\n[bold blue]PyPzza Order Management[/bold blue]")
    console.print("\n1. Create new order")
    console.print("2. List all orders")
    console.print("3. Update order status")
    console.print("4. View order details")
    console.print("5. Delete order")
    console.print("6. Exit")

def get_toppings() -> List[str]:
    """
    Interactive topping selection interface.
    
    Flow:
    1. Display available toppings
    2. Loop for user input
    3. Validate and add selections
    4. Continue until user finishes
    
    Uses:
    - enumerate: Generate numbered list
    - Prompt.ask: Rich's input prompt
    - rprint: Colored status messages
    
    Returns:
        List[str]: Selected toppings
    """
    console.print("\n[bold]Available toppings:[/bold]")
    # enumerate with start=1 for human-friendly numbering
    for i, topping in enumerate(AVAILABLE_TOPPINGS, 1):
        console.print(f"{i}. {topping}")
    
    toppings = []
    while True:
        # Prompt with empty default to allow finishing
        topping_num = Prompt.ask(
            "\nEnter topping number (or press Enter to finish)",
            default=""
        )
        if not topping_num:
            break
        
        try:
            idx = int(topping_num) - 1  # Convert to 0-based index
            if 0 <= idx < len(AVAILABLE_TOPPINGS):
                topping = AVAILABLE_TOPPINGS[idx]
                if topping not in toppings:
                    toppings.append(topping)
                    rprint(f"[green]Added {topping}[/green]")
                else:
                    rprint(f"[yellow]'{topping}' already added[/yellow]")
            else:
                rprint("[red]Invalid topping number[/red]")
        except ValueError:
            rprint("[red]Please enter a valid number[/red]")
    
    return toppings

def create_new_order() -> None:
    """
    Handle new order creation workflow.
    
    Flow:
    1. Get customer name
    2. Display and select size
    3. Select toppings
    4. Create and save order
    
    Uses:
    - Prompt.ask: User input with validation
    - create_order: Business logic
    - storage.add_order: Data persistence
    """
    console.print("\n[bold]Create New Order[/bold]")
    
    customer_name = Prompt.ask("Customer name")
    
    console.print("\n[bold]Available sizes:[/bold]")
    for size, price in PIZZA_SIZES.items():
        console.print(f"- {size}: ${price}")
    
    # Prompt with choices ensures valid input
    size = Prompt.ask("Pizza size", choices=list(PIZZA_SIZES.keys()))
    toppings = get_toppings()
    
    try:
        order = create_order(customer_name, size, toppings)
        storage.add_order(order)
        rprint(f"\n[green]Order created successfully! Order ID: {order['id']}[/green]")
    except ValueError as e:
        rprint(f"\n[red]Error: {e}[/red]")

def display_orders(orders: List[dict]) -> None:
    """
    Display orders in a formatted table.
    
    Uses:
    - Rich.Table: Create formatted tables
    - String slicing: Truncate long IDs
    
    Args:
        orders: List of order dictionaries to display
    """
    if not orders:
        console.print("[yellow]No orders found[/yellow]")
        return
    
    table = Table(title="Pizza Orders")
    # Add columns with styles
    table.add_column("ID", style="cyan")
    table.add_column("Customer", style="magenta")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Price", style="yellow")
    
    for order in orders:
        table.add_row(
            order["id"][:8] + "...",  # Show only first 8 chars of UUID
            order["customer_name"],
            order["pizza_size"],
            order["status"],
            f"${order['price']}"
        )
    
    console.print(table)

def list_orders() -> None:
    """
    Handle listing all orders.
    
    Flow:
    1. Load orders from storage
    2. Display in formatted table
    """
    console.print("\n[bold]All Orders[/bold]")
    orders = storage.load_orders()
    display_orders(orders)

def update_status() -> None:
    """
    Handle order status update workflow.
    
    Flow:
    1. Get order ID
    2. Validate order exists
    3. Check current status
    4. Confirm and update
    
    Uses:
    - Prompt.ask: Get order ID
    - Confirm.ask: Yes/no confirmation
    - update_order_status: Business logic
    - storage.update_order: Persist changes
    """
    order_id = Prompt.ask("Enter order ID")
    order = storage.get_order(order_id)
    
    if not order:
        rprint("[red]Order not found[/red]")
        return
    
    current_status = order["status"]
    current_idx = ORDER_STATES.index(current_status)
    
    if current_idx == len(ORDER_STATES) - 1:
        rprint("[yellow]Order is already in final state (DELIVERED)[/yellow]")
        return
    
    next_status = ORDER_STATES[current_idx + 1]
    if Confirm.ask(f"Update order status to {next_status}?"):
        try:
            updated_order = update_order_status(order, next_status)
            storage.update_order(order_id, updated_order)
            rprint(f"[green]Status updated to {next_status}[/green]")
        except ValueError as e:
            rprint(f"[red]Error: {e}[/red]")

def view_order_details() -> None:
    """
    Handle viewing detailed order information.
    
    Flow:
    1. Get order ID
    2. Fetch order details
    3. Display formatted information
    
    Uses:
    - Prompt.ask: Get order ID
    - storage.get_order: Fetch order
    - console.print: Formatted output
    """
    order_id = Prompt.ask("Enter order ID")
    order = storage.get_order(order_id)
    
    if not order:
        rprint("[red]Order not found[/red]")
        return
    
    console.print("\n[bold]Order Details[/bold]")
    console.print(f"ID: {order['id']}")
    console.print(f"Customer: {order['customer_name']}")
    console.print(f"Size: {order['pizza_size']}")
    console.print(f"Toppings: {', '.join(order['toppings']) or 'No toppings'}")
    console.print(f"Status: {order['status']}")
    console.print(f"Price: ${order['price']}")
    console.print(f"Created: {order['created_at']}")

def delete_order_by_id() -> None:
    """
    Handle order deletion.
    
    Flow:
    1. Get order ID
    2. Attempt deletion
    3. Show result
    
    Uses:
    - Prompt.ask: Get order ID
    - storage.delete_order: Remove order
    """
    order_id = Prompt.ask("Enter order ID")
    
    if storage.delete_order(order_id):
        rprint("[green]Order deleted successfully[/green]")
    else:
        rprint("[red]Order not found[/red]")

def main() -> None:
    """
    Main program loop.
    
    Flow:
    1. Display menu
    2. Get user choice
    3. Execute selected action
    4. Repeat until exit
    
    Uses:
    - Prompt.ask: Menu selection
    - Confirm.ask: Exit confirmation
    """
    while True:
        print_menu()
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            create_new_order()
        elif choice == "2":
            list_orders()
        elif choice == "3":
            update_status()
        elif choice == "4":
            view_order_details()
        elif choice == "5":
            delete_order_by_id()
        else:
            if Confirm.ask("\nAre you sure you want to exit?"):
                console.print("[bold blue]Thank you for using PyPzza![/bold blue]")
                break

if __name__ == "__main__":
    main() 