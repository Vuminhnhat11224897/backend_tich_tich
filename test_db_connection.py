"""
Test database connection
"""
from database import engine, DATABASE_URL
from sqlalchemy import text
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_database_connection():
    """Kiểm tra kết nối database"""
    print("🔍 Testing Database Connection")
    print("="*50)
    
    # Hiển thị thông tin kết nối (không hiển thị password)
    print(f"Host: {os.getenv('DB_HOST')}")
    print(f"Port: {os.getenv('DB_PORT')}")
    print(f"Database: {os.getenv('DB_NAME')}")
    print(f"User: {os.getenv('DB_USER')}")
    print(f"Password: {(os.getenv('DB_PASSWORD'))}")  # Hide password
    print(f"Echo SQL: {os.getenv('ECHO_SQL')}")
    
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful!")
            print(f"PostgreSQL Version: {version}")
            
            # Test if tables exist
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                print(f"📋 Existing tables: {', '.join(tables)}")
            else:
                print("📋 No tables found - database is empty")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Make sure:")
        print("1. Docker PostgreSQL is running: docker-compose up -d")
        print("2. Environment variables are set correctly in .env file")
        print("3. Database credentials are correct")

if __name__ == "__main__":
    test_database_connection()
