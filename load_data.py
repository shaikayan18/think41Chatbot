import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal, Product, Customer, Order, create_tables
import os

def load_products_from_csv(db: Session, csv_path: str):
    """Load products from CSV file"""
    if not os.path.exists(csv_path):
        # Create sample data if CSV doesn't exist
        sample_products = [
            {"name": "Laptop", "description": "High-performance laptop", "price": 999.99, "category": "Electronics", "stock_quantity": 50},
            {"name": "Smartphone", "description": "Latest smartphone", "price": 699.99, "category": "Electronics", "stock_quantity": 100},
            {"name": "Coffee Mug", "description": "Ceramic coffee mug", "price": 12.99, "category": "Home", "stock_quantity": 200},
        ]
        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
    else:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            product = Product(
                name=row['name'],
                description=row.get('description', ''),
                price=float(row['price']),
                category=row.get('category', ''),
                stock_quantity=int(row.get('stock_quantity', 0))
            )
            db.add(product)

def load_customers_from_csv(db: Session, csv_path: str):
    """Load customers from CSV file"""
    if not os.path.exists(csv_path):
        # Create sample data
        sample_customers = [
            {"name": "John Doe", "email": "john@example.com", "phone": "123-456-7890", "address": "123 Main St"},
            {"name": "Jane Smith", "email": "jane@example.com", "phone": "098-765-4321", "address": "456 Oak Ave"},
        ]
        for customer_data in sample_customers:
            customer = Customer(**customer_data)
            db.add(customer)
    else:
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            customer = Customer(
                name=row['name'],
                email=row['email'],
                phone=row.get('phone', ''),
                address=row.get('address', '')
            )
            db.add(customer)

def main():
    create_tables()
    db = SessionLocal()
    
    try:
        # Load data from CSV files or create sample data
        load_products_from_csv(db, "data/products.csv")
        load_customers_from_csv(db, "data/customers.csv")
        
        db.commit()
        print("Data loaded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error loading data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()