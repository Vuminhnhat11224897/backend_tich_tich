from sqlalchemy import create_engine

# User admin là user DUY NHẤT trong container
DATABASE_URL = "postgresql://admin:password123@127.0.0.1:5432/tich_tich_db"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    with engine.connect() as conn:
        # Test connection
        result = conn.execute("SELECT current_user, current_database()")
        row = result.fetchone()
        print(f"✅ SUCCESS!")
        print(f"Connected as user: {row[0]}")
        print(f"Connected to database: {row[1]}")
        
        # Test tạo table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50)
            )
        """)
        print("✅ Table creation successful!")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")