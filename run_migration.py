"""
Database Migration Runner
Simple script to run the JWT authentication migration
"""

import os
import sys

def print_header(msg):
    print("\n" + "="*70)
    print(msg)
    print("="*70 + "\n")

def main():
    print_header("JWT Authentication Database Migration")
    
    # Check if migration file exists
    if not os.path.exists('migration_jwt_auth.sql'):
        print("❌ Error: migration_jwt_auth.sql not found!")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    print("📋 This migration will:")
    print("   1. Add phone_number column to officers table")
    print("   2. Create otp_codes table")
    print("   3. Create refresh_tokens table (optional)")
    print("   4. Create jwt_blacklist table (optional)")
    print()
    
    print("⚠️  IMPORTANT:")
    print("   - Make sure you have a database backup")
    print("   - Verify your .env file has correct credentials")
    print("   - Migration uses 'IF NOT EXISTS' so it's safe to re-run")
    print()
    
    # Load .env to check credentials
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT')
        db_user = os.getenv('DB_USER')
        db_name = os.getenv('DB_NAME')
        
        print("📊 Database Configuration:")
        print(f"   Host: {db_host}")
        print(f"   Port: {db_port}")
        print(f"   User: {db_user}")
        print(f"   Database: {db_name}")
        print()
        
    except Exception as e:
        print(f"⚠️  Warning: Could not load .env file: {e}")
        print()
    
    print("🔧 Migration Methods:")
    print()
    print("Method 1: MySQL Command Line (Recommended)")
    print("-" * 70)
    print("Run this command in PowerShell:")
    print()
    print("mysql -h goa12-sv520413-a84d.k.aivencloud.com `")
    print("      -P 20063 `")
    print("      -u avnadmin `")
    print("      -p `")
    print("      --ssl-mode=REQUIRED `")
    print("      defaultdb < migration_jwt_auth.sql")
    print()
    print("Then enter password when prompted.")
    print()
    
    print("Method 2: MySQL Workbench")
    print("-" * 70)
    print("1. Open MySQL Workbench")
    print("2. Connect to your database")
    print("3. Open migration_jwt_auth.sql")
    print("4. Click Execute")
    print()
    
    print("Method 3: Python Script")
    print("-" * 70)
    print("If you have pymysql installed, I can try to run it now.")
    print()
    
    response = input("Would you like to try running the migration with Python? (y/n): ")
    
    if response.lower() != 'y':
        print("\n✓ No problem! Use one of the methods above.")
        print("\n📖 For detailed instructions, see: DATABASE_MIGRATION_GUIDE.md")
        sys.exit(0)
    
    # Try to run migration with Python
    try:
        import pymysql
        from dotenv import load_dotenv
        
        load_dotenv()
        
        print("\n🔄 Connecting to database...")
        
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl_mode': 'REQUIRED'}
        )
        
        print("✓ Connected successfully!")
        print("\n🔄 Reading migration file...")
        
        with open('migration_jwt_auth.sql', 'r') as f:
            migration_sql = f.read()
        
        print("✓ Migration file loaded")
        print("\n🔄 Executing migration...")
        
        with connection.cursor() as cursor:
            # Split statements and execute
            statements = migration_sql.split(';')
            executed = 0
            
            for statement in statements:
                statement = statement.strip()
                
                # Skip empty statements and comments
                if not statement or statement.startswith('--'):
                    continue
                
                try:
                    cursor.execute(statement)
                    executed += 1
                    print(f"✓ Executed statement {executed}")
                except Exception as e:
                    # Some errors are OK (like "already exists")
                    if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                        print(f"ℹ️  Skipped (already exists): {statement[:50]}...")
                    else:
                        print(f"⚠️  Warning: {e}")
        
        connection.commit()
        print("\n✅ Migration completed successfully!")
        print(f"\n📊 Executed {executed} statements")
        
        # Verify migration
        print("\n🔍 Verifying migration...")
        
        with connection.cursor() as cursor:
            # Check for phone_number column
            cursor.execute("SHOW TABLES LIKE 'officers'")
            if cursor.fetchone():
                cursor.execute("DESCRIBE officers")
                columns = [row[0] for row in cursor.fetchall()]
                if 'phone_number' in columns:
                    print("✓ phone_number column added to officers table")
                else:
                    print("⚠️  phone_number column not found in officers table")
            else:
                # Try 'officer' table
                cursor.execute("SHOW TABLES LIKE 'officer'")
                if cursor.fetchone():
                    print("ℹ️  Note: Using 'officer' table instead of 'officers'")
                    cursor.execute("DESCRIBE officer")
                    columns = [row[0] for row in cursor.fetchall()]
                    if 'phone_number' in columns:
                        print("✓ phone_number column added to officer table")
            
            # Check for otp_codes table
            cursor.execute("SHOW TABLES LIKE 'otp_codes'")
            if cursor.fetchone():
                print("✓ otp_codes table created")
            else:
                print("⚠️  otp_codes table not found")
        
        connection.close()
        
        print("\n" + "="*70)
        print("🎉 Migration Complete!")
        print("="*70)
        print("\n📋 Next Steps:")
        print("1. Add phone numbers to officers:")
        print("   UPDATE officers SET phone_number = '9876543210' WHERE id = 'officer_id';")
        print("\n2. Test authentication:")
        print("   python run.py")
        print("\n3. Read documentation:")
        print("   JWT_IMPLEMENTATION_SUMMARY.md")
        print()
        
    except ImportError:
        print("\n❌ Error: pymysql not installed")
        print("\nInstall it with: pip install pymysql")
        print("\nOr use Method 1 or 2 above instead.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        print("\n💡 Tip: Try using Method 1 or 2 instead")
        print("See DATABASE_MIGRATION_GUIDE.md for detailed instructions")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
        sys.exit(1)
