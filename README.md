# PyPzza

A simple CLI application to manage pizza orders, built with Python.

## Setup

1. Create and activate virtual environment:

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

## Features

- Create and manage pizza orders
- Track order status
- Store orders persistently
- Calculate order prices

## Project Structure

- `src/`: Source code
- `data/`: Data storage
- `requirements.txt`: Project dependencies
- `DESIGN.md`: Detailed design documentation

## Data Flow

```mermaid
graph TD
    A[Start] --> B[Main Menu]
    B --> C1[Create Order]
    B --> C2[List Orders]
    B --> C3[Update Status]
    B --> C4[View Details]
    B --> C5[Delete Order]
    B --> E[Exit]

    C1 --> D1[Get Customer Info]
    D1 --> D2[Select Size]
    D2 --> D3[Select Toppings]
    D3 --> D4[Calculate Price]
    D4 --> D5[Save Order]
    D5 --> B

    C2 --> F1[Load Orders]
    F1 --> F2[Display Table]
    F2 --> B

    C3 --> G1[Get Order ID]
    G1 --> G2[Validate Order]
    G2 --> G3[Check Status]
    G3 --> G4[Update if Valid]
    G4 --> B

    C4 --> H1[Get Order ID]
    H1 --> H2[Load Order]
    H2 --> H3[Display Details]
    H3 --> B

    C5 --> I1[Get Order ID]
    I1 --> I2[Delete if Exists]
    I2 --> B
```
