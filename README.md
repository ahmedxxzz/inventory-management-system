# Inventory Management System V3 (Elbahgy لادارة المخازن)

## Overview

This is a comprehensive desktop application designed for managing inventory, sales, and financial operations. It features a modern dark-themed GUI built with CustomTkinter and follows the MVC (Model-View-Controller) architectural pattern.

## Features

The application includes the following main modules:

- **Factories (المصانع):** Manage factory details and interactions.
- **Offices/Customers (المكاتب):** Manage customer offices and their orders.
- **Inventory (المخزن):** Track product stock, incoming, and outgoing items.
- **Distributors (الموزعين):** Manage distributor profiles and relationships.
- **Wallet (الخزنة):** Track financial transactions, income, and expenses.
- **Extra Costs (المصاريف):** Record and monitor additional operational costs.
- **Notifications (الاشعارات):** Real-time alerts for important events (e.g., low stock, payment due).

## Technical Architecture

- **Language:** Python
- **GUI:** CustomTkinter
- **Database:** SQLite (`IMS.db`)
- **Pattern:** Model-View-Controller (MVC)

## Installation & Usage

### Prerequisites

Ensure you have Python installed. You will need to install the following dependencies:

```bash
pip install customtkinter Pillow
```

### Running the Application

To start the application, run the `main.py` file located in the `src` directory:

```bash
python src/main.py
```

## Project Structure

```
src/
├── controller/       # Application logic and orchestration
├── model/           # Database interactions and data logic
├── view/            # GUI components and layout
├── Z_Files/         # Assets (images, resources)
├── IMS.db           # SQLite Database file
└── main.py          # Application entry point
```

## Credits

Developed for **Elbahgy**.
