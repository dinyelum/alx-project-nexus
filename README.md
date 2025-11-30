# Ecommerce Backend API
A robust and scalable **Django REST Framework** backend for modern ecommerce operations. Includes complete product management, shopping cart functionality, and order processing.

---

## 🚀 Features
- **Product Management** – Full CRUD for products and collections
- **Shopping Cart** – Session-based cart with item management
- **Order Processing** – Complete lifecycle from cart to fulfillment
- **Customer Management** – User profiles with membership tiers
- **Review System** – Product reviews and ratings
- **Promotions** – Flexible discount and promotion system
- **RESTful API** – Clean, predictable endpoints following REST conventions

---

## 🛠 Tech Stack
**Backend:** Django, Django REST Framework  
**Authentication:** Djoser + JWT (Simple JWT)  
**Database:** SQLite (Dev) / PostgreSQL (Ready)  
**API Tools:** DRF Nested Routers, Django Filter, Debug Toolbar  
**Caching:** Redis *(planned)*

---

## 📋 API Endpoints
### **Products**
```
GET    /store/products/              # List all products
POST   /store/products/              # Create product (Admin)
GET    /store/products/{id}/         # Product details
PUT    /store/products/{id}/         # Update product
DELETE /store/products/{id}/         # Delete product
```

### **Collections**
```
GET    /store/collections/           # List categories
POST   /store/collections/           # Create collection
GET    /store/collections/{id}/      # Collection details
```

### **Shopping Cart**
```
POST   /store/carts/                 # Create cart
GET    /store/carts/{uuid}/          # Retrieve cart
DELETE /store/carts/{uuid}/          # Delete cart
GET    /store/carts/{uuid}/items/    # List cart items
POST   /store/carts/{uuid}/items/    # Add item
PUT    /store/carts/{uuid}/items/{id}/ # Update quantity
DELETE /store/carts/{uuid}/items/{id}/ # Remove item
```

### **Customers & Orders**
```
GET    /store/customers/me/          # My profile
GET    /store/customers/             # List customers (Admin)
POST   /store/orders/                # Create order
GET    /store/orders/                # List orders
GET    /store/orders/{id}/           # Order details
```

---

## 🗄 Database Schema
### **Key Relationships**
- **Collections → Products** (1–Many)
- **Products ↔ Promotions** (Many–Many)
- **Customers → Orders** (1–Many)
- **Orders → OrderItems** (1–Many)
- **Carts → CartItems** (1–Many)

---

## 🏗 Architecture
```
project/
├── app/                     # Main store application
│   ├── admin.py             # Admin configs
│   ├── filters.py           # Custom filters
│   ├── models.py            # Core models
│   ├── permissions.py       # Permissions
│   ├── serializers.py       # DRF serializers
│   ├── signals.py           # Event logic
│   ├── urls.py              # Routing
│   └── views.py             # API views
└── core/                    # Project-level logic
    ├── models.py
    ├── serializers.py
    ├── tests.py
    └── views.py
```

### **Design Principles**
- Separation of Concerns
- Command-Query Responsibility Separation (CQRS)
- RESTful conventions
- Performance-first architecture

---

## 🔧 Installation
### **1. Clone repository**
```
git clone git@github.com:dinyelum/alx-project-nexus.git
cd ecommerce-api
```

### **2. Create virtual environment**
```
python -m venv venv
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### **3. Install dependencies**
```
pip install -r requirements.txt
```

### **4. Run migrations**
```
python manage.py migrate
```

### **5. Start server**
```
python manage.py runserver
```

---

## 🚀 Usage
### **Authentication (JWT)**
Include JWT token in requests:
```
Authorization: Bearer <token>
```

### **Example Requests**
```
# Get products
curl -X GET http://127.0.0.1:8000/store/products/

# Create new cart
curl -X POST http://127.0.0.1:8000/store/carts/
```

---

## 🧪 Testing
```
python manage.py test
```

---

## 🔮 Future Enhancements
- Redis caching
- Payment gateway integration
- Email notifications
- Elasticsearch search
- Inventory webhooks
- Admin dashboard

---

## 📝 API Documentation
- **Swagger UI:** `/swagger/`
- **ReDoc:** `/redoc/`

---

## 👨‍💻 Developer
**Johaness Ndidika**  
Full‑Stack Developer (PHP | Python)

