import os
from database import create_tables
from load_data import main as load_data_main

def setup_project():
    """Setup the project with database and sample data"""
    print("Creating database tables...")
    create_tables()
    
    print("Loading sample data...")
    load_data_main()
    
    print("Setup complete!")

if __name__ == "__main__":
    setup_project()