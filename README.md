# 🛒 E-Commerce Backend API

## 📌 What is this project?

This project is the **backend system for an online shopping application**.

Think about websites such as Amazon or Daraz. When a customer opens an online store, they can:

1. Create an account
2. Log in
3. Browse products
4. Search for products
5. Filter products by category and price
6. Add products to a shopping cart
7. Place an order
8. View their previous orders

Behind all of those actions, a backend system is needed to receive requests, validate information, communicate with the database, manage users, calculate orders, update stock, and protect private data.

**This project is that backend system.**

It provides a REST API that a frontend application, mobile application, or other client can communicate with.

---

## 🎯 What does the system actually do?

Imagine a customer wants to buy a laptop.

### Step 1 — Customer creates an account

The customer sends their information to:

```text
POST /auth/register
```

The backend:

* Validates the information
* Checks whether the username already exists
* Checks whether the email already exists
* Hashes the password
* Stores the user in MySQL

The password is **not stored as plain text**.

---

### Step 2 — Customer logs in

The customer sends their username and password:

```text
POST /auth/login
```

The backend verifies the credentials.

If they are correct, the backend creates a **JWT access token**.

```text
Customer
   ↓
Username + Password
   ↓
FastAPI
   ↓
Verify password
   ↓
JWT Token
```

The customer then uses that token when accessing protected features.

---

### Step 3 — Customer browses products

The customer can request:

```text
GET /products/
```

The backend gets products from MySQL and returns them as JSON.

For example:

```json
[
    {
        "id": 1,
        "name": "Laptop",
        "price": 85000,
        "stock": 10,
        "category_id": 1
    }
]
```

---

## 🔎 Product Search and Filtering

The customer doesn't always want to see every product.

They can search:

```text
GET /products/?search=laptop
```

They can filter by category:

```text
GET /products/?category_id=1
```

They can filter by price:

```text
GET /products/?min_price=50000&max_price=100000
```

They can also use pagination:

```text
GET /products/?page=1&limit=10
```

This makes the API more practical for a real online store.

---

## 🛍️ Step 4 — Customer adds a product to the cart

The customer sends:

```text
POST /cart/items
```

with a product and quantity.

The backend checks:

* Does the product exist?
* Is the quantity greater than zero?
* Is there enough stock?

If everything is valid, the product is added to the customer's cart.

The database structure is:

```text
User
 ↓
Cart
 ↓
CartItem
 ↓
Product
```

Each customer has their own cart.

---

## 📦 Step 5 — Customer places an order

When the customer is ready to buy, they send:

```text
POST /orders/
```

The backend then:

1. Gets the customer's cart
2. Checks that the cart isn't empty
3. Checks product stock
4. Calculates the total price
5. Creates an order
6. Creates order items
7. Reduces product stock
8. Removes the purchased items from the cart

For example:

```text
Laptop        $800 × 1
Mouse          $20 × 2
----------------------
Total         $840
```

The order is initially created with:

```text
PENDING
```

---

## 🚚 Step 6 — Admin manages the order

An administrator can see all orders:

```text
GET /orders/admin
```

The admin can update the order status:

```text
PENDING
      ↓
PROCESSING
      ↓
SHIPPED
      ↓
DELIVERED
```

An order can also be:

```text
CANCELLED
```

Regular customers cannot access admin-only operations.

---

# 👨‍💼 What can an Admin do?

The project has **role-based authorization**.

### Customer

A normal customer can:

* Register
* Login
* View their profile
* Browse products
* Search products
* Filter products
* Manage their cart
* Place orders
* View their order history

### Admin

An admin can additionally:

* Create categories
* Update categories
* Delete categories
* Create products
* Update products
* Delete products
* View all orders
* Update order status

The backend checks the user's role before allowing admin operations.

```text
Request
   ↓
JWT Authentication
   ↓
Current User
   ↓
Check Role
   ↓
Customer → Customer operations
Admin    → Admin operations
```

---

# 🏗️ How the Backend Works

The overall system looks like this:

```text
                    Internet
                       ↓
                  Client / Frontend
                       ↓
                    FastAPI
                       ↓
              Authentication Layer
                       ↓
                 Business Logic
                       ↓
                  SQLAlchemy
                       ↓
                     MySQL
```

The API is built with FastAPI.

SQLAlchemy is used to communicate with MySQL.

Alembic manages database structure changes.

Docker packages the application and database into containers.

---

# 🗄️ Main Database Structure

The project contains several connected tables:

```text
Users
  │
  ├──────────→ Carts
  │              │
  │              └──→ Cart Items ──→ Products
  │
  └──────────→ Orders
                 │
                 └──→ Order Items ──→ Products

Categories
     │
     └──────────→ Products
```

This allows the backend to represent real relationships between customers, products, carts, and orders.

---

# 🔐 Security

Security is an important part of the project.

The API includes:

* Password hashing
* JWT authentication
* Protected routes
* Role-based authorization
* Environment variables
* Secret protection with `.gitignore`

Sensitive values such as database credentials and JWT secrets are kept outside the source code.

---

# 🧪 Testing

The project also includes automated API tests using **Pytest**.

Tests cover basic functionality such as:

```text
Home endpoint
Protected routes
Invalid login
Product endpoint
```

The purpose is to verify that important API behavior continues to work as the project grows.

---

# 🐳 Docker

The complete application can also run using Docker.

The architecture is:

```text
Docker Compose
      │
      ├── FastAPI Container
      │
      └── MySQL Container
              │
              └── Persistent Volume
```

Instead of requiring someone to manually configure Python, FastAPI, and MySQL on their computer, Docker provides a consistent development environment.

---

# 💡 Why I built this project

I built this project to practice and demonstrate **real-world backend engineering concepts**, rather than only creating small CRUD APIs.

It combines:

* REST API development
* Authentication
* Authorization
* Database design
* SQLAlchemy
* Database relationships
* Business logic
* Search and filtering
* Pagination
* Shopping cart functionality
* Order processing
* Stock management
* Error handling
* Automated testing
* Docker
* Database migrations

The project is designed as a portfolio backend that could serve as the foundation for a real e-commerce frontend or mobile application.
