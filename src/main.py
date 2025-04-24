"""
PyPzza - A simple CLI pizza order management system.

What is this file?
-----------------
This is the main entry point of our pizza ordering system. It:
1. Shows menus and gets user input
2. Manages orders (create, update, view, delete)
3. Displays results in a nice format
4. Controls the program flow

We use the Rich library to make our terminal output look nice,
similar to how CSS styles web pages.
"""

# Import standard Python tools
# --------------------------
from typing import List  # Like types in TypeScript

# Rich library for fancy terminal output
# -----------------------------------
from rich.console import Console    # Main output tool
from rich.table import Table       # Creates formatted tables
from rich.prompt import Prompt     # Input with validation
from rich.prompt import Confirm    # Yes/no questions
from rich import print as rprint   # Fancy print with colors

# Our custom modules
# ----------------
from order import (
    create_order, update_order_status,
    PIZZA_SIZES, AVAILABLE_TOPPINGS, ORDER_STATES
)
import storage

# Create console for fancy output (shared across functions)
console = Console()

def print_menu() -> None:
    """
    Shows the main menu options to the user.
    Uses Rich's color syntax: [color]text[/color]
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
    Interactive topping selection.
    
    Returns:
        List of chosen topping names
    
    Note: Uses enumerate(list, start=1) to show:
    1. cheese
    2. pepperoni
    etc.
    """
    console.print("\n[bold]Available toppings:[/bold]")
    
    # enumerate is a special Python function that gives us both the position and value
    # when we write: for position, topping in enumerate(AVAILABLE_TOPPINGS, start=1)
    # it's like doing:
    #   position = 1
    #   for topping in AVAILABLE_TOPPINGS:
    #       print(f"{position}. {topping}")
    #       position += 1
    for position, topping in enumerate(AVAILABLE_TOPPINGS, start=1):
        console.print(f"{position}. {topping}")
    
    # This will store our chosen toppings
    selected_toppings = []
    
    while True:  # This is an infinite loop - it keeps going until we 'break'
        # Prompt.ask is a fancy input function that:
        # 1. Shows the message in a nice format
        # 2. Gets user input
        # 3. If default="", pressing Enter returns an empty string
        topping_number = Prompt.ask(
            "\nEnter topping number (or press Enter to finish)",
            default=""
        )
        
        # If user just pressed Enter (empty string), exit the loop
        if not topping_number:
            break
        
        try:
            # Convert string to number and adjust for 0-based index
            # We subtract 1 because lists start at 0, but we showed numbers starting at 1
            # Example: User enters "1", we need index 0 to get first topping
            index = int(topping_number) - 1
            
            # Check if index is valid (between 0 and number of toppings)
            # This is like: if (index >= 0 && index < AVAILABLE_TOPPINGS.length)
            if 0 <= index < len(AVAILABLE_TOPPINGS):
                chosen_topping = AVAILABLE_TOPPINGS[index]
                
                # not in checks if something isn't in a list
                # It's like: !array.includes(item) in JavaScript
                if chosen_topping not in selected_toppings:
                    selected_toppings.append(chosen_topping)  # Add to end of list
                    rprint(f"[green]Added {chosen_topping}[/green]")
                else:
                    rprint(f"[yellow]'{chosen_topping}' already added[/yellow]")
            else:
                rprint("[red]Invalid topping number[/red]")
        except ValueError:
            # This happens when int(topping_number) fails
            # (when user types something that's not a number)
            rprint("[red]Please enter a valid number[/red]")
    
    return selected_toppings

def create_new_order() -> None:
    """
    Creates a new pizza order:
    1. Gets customer info
    2. Shows size options
    3. Gets toppings
    4. Saves order
    
    Note: Uses Rich's Prompt for validated input
    """
    console.print("\n[bold]Create New Order[/bold]")
    
    # Simple input with no validation
    customer_name = Prompt.ask("Customer name")
    
    console.print("\n[bold]Available sizes:[/bold]")
    # items() gives us both keys and values from a dictionary
    # It's like Object.entries() in JavaScript
    # Example: for ('small', 10.99) in PIZZA_SIZES.items():
    for size, price in PIZZA_SIZES.items():
        # f-strings (f"...") let us put variables inside strings
        # Example: f"small: $10.99"
        console.print(f"- {size}: ${price}")
    
    # Prompt.ask with choices ensures user can only enter valid sizes
    # choices=list(...) converts dict_keys to a list
    # Example: choices=['small', 'medium', 'large']
    size = Prompt.ask(
        "Pizza size",
        choices=list(PIZZA_SIZES.keys())
    )
    
    toppings = get_toppings()
    
    try:
        # create_order might raise ValueError if something's invalid
        new_order = create_order(customer_name, size, toppings)
        storage.add_order(new_order)
        rprint(f"\n[green]Order created successfully! Order ID: {new_order['id']}[/green]")
    except ValueError as error:
        # If create_order raised an error, show it in red
        rprint(f"\n[red]Error: {error}[/red]")

def display_orders(orders: List[dict]) -> None:
    """
    Shows orders in a formatted table.
    
    Args:
        orders: List of order dictionaries
    
    Note: Uses Rich's Table with colored columns
    """
    if not orders:  # Empty list is considered False in Python
        console.print("[yellow]No orders found[/yellow]")
        return
    
    # Create a Rich table with a title
    table = Table(title="Pizza Orders")
    
    # Add columns with different styles
    # Each column can have its own color
    table.add_column("ID", style="cyan")
    table.add_column("Customer", style="magenta")
    table.add_column("Size", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Price", style="yellow")
    
    # Add each order as a row
    for order in orders:
        table.add_row(
            # String slicing: [start:end]
            # [:8] means "from start to position 8"
            # So "123456789" becomes "12345678"
            order["id"][:8] + "...",  # Show first 8 chars of ID
            order["customer_name"],
            order["pizza_size"],
            order["status"],
            f"${order['price']}"  # Format price with $ sign
        )
    
    console.print(table)

def list_orders() -> None:
    """
    Displays all orders in the system.
    Loads from storage and formats in a table.
    """
    console.print("\n[bold]All Orders[/bold]")
    # Get orders from storage and display them
    orders = storage.load_orders()
    display_orders(orders)

def update_status() -> None:
    """
    Updates an order's status.
    
    Flow:
    PENDING -> PREPARING -> READY -> DELIVERED
    
    Note: Validates current status before updating
    """
    order_id = Prompt.ask("Enter order ID")
    order = storage.get_order(order_id)
    
    if not order:
        rprint("[red]Order not found[/red]")
        return
    
    current_status = order["status"]
    # index() finds the position of an item in a list
    # Example: ['a', 'b', 'c'].index('b') returns 1
    current_idx = ORDER_STATES.index(current_status)
    
    # Check if we're at the last status
    # len(list) - 1 is the last valid index
    if current_idx == len(ORDER_STATES) - 1:
        rprint("[yellow]Order is already in final state (DELIVERED)[/yellow]")
        return
    
    # Get next status from the list
    # list[index] gets item at position
    next_status = ORDER_STATES[current_idx + 1]
    
    # Ask for confirmation
    if Confirm.ask(f"Update order status to {next_status}?"):
        try:
            updated_order = update_order_status(order, next_status)
            storage.update_order(order_id, updated_order)
            rprint(f"[green]Status updated to {next_status}[/green]")
        except ValueError as error:
            rprint(f"[red]Error: {error}[/red]")

def view_order_details() -> None:
    """
    Shows complete details for one order.
    
    Note: Uses join() to format toppings list:
    "cheese, pepperoni, mushrooms"
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
    # join() combines list items with a separator
    # Example: ', '.join(['a', 'b', 'c']) becomes "a, b, c"
    # or 'No toppings' if the list is empty (which is False in Python)
    console.print(f"Toppings: {', '.join(order['toppings']) or 'No toppings'}")
    console.print(f"Status: {order['status']}")
    console.print(f"Price: ${order['price']}")
    console.print(f"Created: {order['created_at']}")

def delete_order_by_id() -> None:
    """
    Removes an order from the system.
    Confirms successful deletion.
    """
    # Get order ID from user
    order_id = Prompt.ask("Enter order ID")
    
    # Try to delete the order
    # delete_order returns True if successful, False if not found
    if storage.delete_order(order_id):
        rprint("[green]Order deleted successfully[/green]")
    else:
        rprint("[red]Order not found[/red]")

def main() -> None:
    """
    Main program loop.
    
    Flow:
    1. Show menu
    2. Get valid choice
    3. Execute chosen action
    4. Repeat until exit
    """
    while True:  # Keep running until we break the loop
        # Show menu and get choice
        print_menu()
        choice = Prompt.ask(
            "\nSelect an option",
            # User can only enter these numbers
            choices=["1", "2", "3", "4", "5", "6"]
        )
        
        # Do different things based on user's choice
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
        else:  # choice must be "6" because of our choices parameter
            # Ask for confirmation before exiting
            if Confirm.ask("\nAre you sure you want to exit?"):
                console.print("[bold blue]Thank you for using PyPzza![/bold blue]")
                break  # Exit the loop, ending the program

# Program entry point check
# Similar to checking if this is the main module
if __name__ == "__main__":
    main() 