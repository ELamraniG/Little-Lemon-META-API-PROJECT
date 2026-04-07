# Little Lemon Restaurant System API

API-only backend for the Little Lemon project using Django, Django REST Framework, and Djoser token authentication.

## Stack

- Python
- Django
- Django REST Framework
- Djoser
- SQLite

## Project Structure

```
backend/
  manage.py
  littlelemon/
    settings.py
    urls.py
  menu/
    models.py
    serializers.py
    views.py
    urls.py
  orders/
    models.py
    serializers.py
    views.py
    urls.py
  users/
    permissions.py
    serializers.py
    views.py
    urls.py
```

## Setup

Run these commands from the project root on Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install django djangorestframework djoser
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Server base URL:

- http://127.0.0.1:8000/

## Authentication

Token authentication is enabled.

Djoser endpoints:

- POST /auth/users/
- POST /auth/token/login/
- POST /auth/token/logout/
- GET /auth/users/me/

After login, include this header:

- Authorization: Token <your_token>

## Models

### MenuItem

- id
- title
- price
- inventory

### Cart

- user
- menuitem
- quantity
- unit_price
- price

### Order

- user
- delivery_crew (nullable)
- status (0 or 1)
- total
- date

### OrderItem

- order
- menuitem
- quantity
- unit_price
- price

## API Endpoints

### Menu

- GET /api/menu-items
- GET /api/menu-items/{id}
- POST /api/menu-items
- PUT /api/menu-items/{id}
- PATCH /api/menu-items/{id}
- DELETE /api/menu-items/{id}

### Groups

- GET /api/groups/manager/users
- POST /api/groups/manager/users
- DELETE /api/groups/manager/users/{userId}
- GET /api/groups/delivery-crew/users
- POST /api/groups/delivery-crew/users
- DELETE /api/groups/delivery-crew/users/{userId}

### Cart

- GET /api/cart/menu-items
- POST /api/cart/menu-items
- DELETE /api/cart/menu-items

### Orders

- GET /api/orders
- POST /api/orders
- GET /api/orders/{id}
- PUT /api/orders/{id}
- PATCH /api/orders/{id}
- DELETE /api/orders/{id}

## Roles and Permissions

### Customer

- Can view menu
- Can use cart
- Can create orders
- Can only view own orders

### Manager

- Full access to menu
- Can manage manager and delivery crew groups
- Can view all orders
- Can assign delivery crew and update order status
- Can delete orders

### Delivery Crew

- Can view only assigned orders
- Can update assigned order status

## Business Logic

When POST /api/orders is called by a customer:

1. A new order is created.
2. All items from that user cart are copied into OrderItem.
3. Order total is calculated from cart item prices.
4. The cart is cleared.

## Filtering and Pagination

### Menu list

- Search by title: /api/menu-items?search=pizza
- Ordering: /api/menu-items?ordering=price or /api/menu-items?ordering=-price
- Page size override: /api/menu-items?perpage=10

### Orders list

- Page size override: /api/orders?perpage=10

Default page size is 5.
