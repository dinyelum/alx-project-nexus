Ecommerce Backend API
A robust, scalable Django REST Framework backend for modern ecommerce operations, featuring complete product management, shopping cart functionality, and order processing.

🚀 Features
Product Management: Full CRUD operations for products and collections

Shopping Cart: Session-based cart with item management

Order Processing: Complete order lifecycle from cart to fulfillment

Customer Management: User profiles with membership tiers

Review System: Product reviews and ratings

Promotions: Flexible discount and promotion system

RESTful API: Clean, predictable endpoints following REST conventions

🛠 Tech Stack
Backend Framework: Django & Django REST Framework

Authentication: Djoser with JWT (Simple JWT)

Database: SQLite (Development) / PostgreSQL ready

API Features:

DRF Nested Routers

Django Filter for query optimization

Django Debug Toolbar for performance monitoring

Caching: Redis (planned implementation)

📋 API Endpoints
Products
GET    /store/products/          # List all products
POST   /store/products/          # Create product (Admin)
GET    /store/products/{id}/     # Get product details
PUT    /store/products/{id}/     # Update product
DELETE /store/products/{id}/     # Delete product

Collections
GET    /store/collections/       # List product categories
POST   /store/collections/       # Create collection
GET    /store/collections/{id}/  # Get collection details

Shopping Cart
POST   /store/carts/             # Create new cart
GET    /store/carts/{uuid}/      # Get cart contents
DELETE /store/carts/{uuid}/      # Delete cart
GET    /store/carts/{uuid}/items/ # List cart items
POST   /store/carts/{uuid}/items/ # Add item to cart
PUT    /store/carts/{uuid}/items/{id}/ # Update item quantity
DELETE /store/carts/{uuid}/items/{id}/ # Remove item from cart

Customers & Orders
GET    /store/customers/me/      # Manage my profile
GET    /store/customers/         # List customers (Admin)
POST   /store/orders/            # Create order from cart
GET    /store/orders/            # List orders
GET    /store/orders/{id}/       # Get order details

🗄 Database Schema
Key Relationships
Collections → Products: One-to-Many (categories contain products)

Products ↔ Promotions: Many-to-Many (flexible discount system)

Customers → Orders: One-to-Many (purchase history)

Orders → OrderItems: One-to-Many (order composition)

Carts → CartItems: One-to-Many (shopping sessions)

🏗 Architecture
Project Structure
project/
├── store/          # Reusable ecommerce engine
│   ├── models/     # Core business models
│   ├── api/        # Generic API endpoints
│   └── services/   # Business logic
└── core/           # Project-specific implementations
    ├── signals/    # Event handlers
    └── utils/      # Project utilities

Design Principles
Separation of Concerns: Clear boundaries between generic and project-specific code

Command-Query Separation: Optimized data access patterns

RESTful Design: Consistent API conventions

Performance First: Optimized queries and caching-ready architecture

🔧 Installation
1. Clone the repository
git clone <git@github.com:dinyelum/alx-project-nexus.git>
cd ecommerce-api

2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run migrations
python manage.py migrate

5. Start development server
python manage.py runserver

🚀 Usage
Authentication
The API uses JWT authentication. Include the token in your requests:
Authorization: Bearer <your_token>

Example Request
bash
# Get all products
curl -X GET http://127.0.0.1:8000/store/products/

# Create a new cart
curl -X POST http://127.0.0.1:8000/store/carts/


🧪 Testing
python manage.py test


🔮 Future Enhancements
Redis caching implementation

Payment gateway integration

Email notifications

Advanced search with Elasticsearch

Inventory management webhooks

Admin dashboard


📝 API Documentation
Full API documentation available via:

Swagger UI: /swagger/

ReDoc: /redoc/

👨‍💻 Developer
Johaness Ndidika
FullStack Developer (PHP | Python)