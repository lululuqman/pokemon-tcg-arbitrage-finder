# scripts/init_db.py

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.db_manager import db_manager

if __name__ == "__main__":
    print("Initializing database...")
    db_manager.create_tables()
    print("Database initialized successfully!")