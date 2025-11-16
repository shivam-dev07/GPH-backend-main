"""
JWT Authentication Setup Script
Run this script to set up JWT authentication for your Flask backend

Prerequisites:
1. Activate conda environment: conda activate d:\envs\tf
2. Ensure MySQL credentials are in .env file
3. Have PyJWT installed: pip install PyJWT==2.8.0
"""

import os
import sys
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")

def print_success(message):
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")

def check_environment():
    """Check if all required environment variables are set"""
    print_header("Step 1: Checking Environment Configuration")
    
    required_vars = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'DB_NAME': os.getenv('DB_NAME'),
        'SECRET_KEY': os.getenv('SECRET_KEY')
    }
    
    all_set = True
    for var, value in required_vars.items():
        if value:
            print_success(f"{var} is set")
        else:
            print_error(f"{var} is NOT set")
            all_set = False
    
    if not all_set:
        print_error("\nSome required environment variables are missing!")
        print_info("Please check your .env file and ensure all variables are set.")
        return False
    
    # Check SECRET_KEY strength
    secret_key = required_vars['SECRET_KEY']
    if secret_key == 'your-secret-key-change-this-in-production':
        print_warning("\nSECRET_KEY is set to default value!")
        print_info("For production, generate a strong key:")
        print_info("  python -c \"import secrets; print(secrets.token_hex(32))\"")
    
    return True

def test_database_connection():
    """Test connection to MySQL database"""
    print_header("Step 2: Testing Database Connection")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl_mode': 'REQUIRED'}
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print_success(f"Connected to MySQL {version[0]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print_error(f"Database connection failed: {str(e)}")
        return False

def check_tables_exist():
    """Check if required tables exist"""
    print_header("Step 3: Checking Database Tables")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl_mode': 'REQUIRED'}
        )
        
        with connection.cursor() as cursor:
            # Check for officers/officer table
            cursor.execute("SHOW TABLES LIKE 'officers'")
            if cursor.fetchone():
                print_success("'officers' table exists")
                table_name = 'officers'
            else:
                cursor.execute("SHOW TABLES LIKE 'officer'")
                if cursor.fetchone():
                    print_success("'officer' table exists")
                    table_name = 'officer'
                else:
                    print_error("Neither 'officers' nor 'officer' table exists")
                    return False, None
            
            # Check if phone_number column exists
            cursor.execute(f"DESCRIBE {table_name}")
            columns = [row[0] for row in cursor.fetchall()]
            
            if 'phone_number' in columns:
                print_success(f"'phone_number' column exists in {table_name}")
            else:
                print_warning(f"'phone_number' column does NOT exist in {table_name}")
                print_info("Migration script will add this column")
            
            # Check for otp_codes table
            cursor.execute("SHOW TABLES LIKE 'otp_codes'")
            if cursor.fetchone():
                print_success("'otp_codes' table exists")
            else:
                print_warning("'otp_codes' table does NOT exist")
                print_info("Migration script will create this table")
        
        connection.close()
        return True, table_name
        
    except Exception as e:
        print_error(f"Error checking tables: {str(e)}")
        return False, None

def run_migration():
    """Run the JWT authentication migration"""
    print_header("Step 4: Running Database Migration")
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl_mode': 'REQUIRED'}
        )
        
        # Read migration file
        with open('migration_jwt_auth.sql', 'r') as f:
            migration_sql = f.read()
        
        # Execute migration
        with connection.cursor() as cursor:
            # Split by semicolon and execute each statement
            statements = [s.strip() for s in migration_sql.split(';') if s.strip()]
            
            for statement in statements:
                # Skip comments
                if statement.startswith('--') or not statement:
                    continue
                
                try:
                    cursor.execute(statement)
                    print_success(f"Executed: {statement[:60]}...")
                except Exception as e:
                    # Some statements might fail if already exists, that's okay
                    if "Duplicate" in str(e) or "already exists" in str(e):
                        print_info(f"Skipped (already exists): {statement[:60]}...")
                    else:
                        print_warning(f"Warning: {str(e)}")
            
            connection.commit()
        
        print_success("\nMigration completed successfully!")
        connection.close()
        return True
        
    except Exception as e:
        print_error(f"Migration failed: {str(e)}")
        return False

def verify_setup():
    """Verify the JWT setup is complete"""
    print_header("Step 5: Verifying Setup")
    
    checks = {
        'config.py exists': os.path.exists('config.py'),
        'utils/decorators.py exists': os.path.exists('utils/decorators.py'),
        'models/auth_model.py exists': os.path.exists('models/auth_model.py'),
        'controllers/auth_controller.py exists': os.path.exists('controllers/auth_controller.py'),
        'routes/auth_routes.py exists': os.path.exists('routes/auth_routes.py')
    }
    
    all_good = True
    for check, result in checks.items():
        if result:
            print_success(check)
        else:
            print_error(check)
            all_good = False
    
    return all_good

def add_test_data():
    """Add test phone numbers to officers table"""
    print_header("Step 6: Adding Test Data (Optional)")
    
    response = input("Do you want to add test phone numbers to officers? (y/n): ")
    
    if response.lower() != 'y':
        print_info("Skipping test data insertion")
        return
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            ssl={'ssl_mode': 'REQUIRED'}
        )
        
        with connection.cursor() as cursor:
            # Check which table exists
            cursor.execute("SHOW TABLES LIKE 'officers'")
            table_name = 'officers' if cursor.fetchone() else 'officer'
            
            # Get first 5 officers without phone numbers
            cursor.execute(f"""
                SELECT id, staff_name 
                FROM {table_name} 
                WHERE phone_number IS NULL 
                LIMIT 5
            """)
            officers = cursor.fetchall()
            
            if not officers:
                print_info("All officers already have phone numbers")
                return
            
            # Add test phone numbers
            for i, (officer_id, staff_name) in enumerate(officers, start=1):
                phone = f"98765432{i:02d}"
                cursor.execute(f"""
                    UPDATE {table_name} 
                    SET phone_number = %s 
                    WHERE id = %s
                """, (phone, officer_id))
                print_success(f"Added phone {phone} to officer {staff_name} (ID: {officer_id})")
            
            connection.commit()
            print_success(f"\nAdded test phone numbers to {len(officers)} officers")
        
        connection.close()
        
    except Exception as e:
        print_error(f"Error adding test data: {str(e)}")

def print_next_steps():
    """Print next steps for the developer"""
    print_header("Setup Complete! Next Steps:")
    
    print(f"{Colors.BOLD}1. Test the Authentication API:{Colors.ENDC}")
    print("   - Start your Flask server: python run.py")
    print("   - Send OTP: POST /api/auth/send-otp")
    print("   - Verify OTP: POST /api/auth/verify-otp")
    print("   - Test secure endpoint: GET /api/auth/test-secure")
    print()
    
    print(f"{Colors.BOLD}2. Protect Your Routes:{Colors.ENDC}")
    print("   - Review: EXAMPLE_duty_routes_with_jwt.py")
    print("   - Add @jwt_required decorator to protected routes")
    print("   - Update controllers to use request.current_user")
    print()
    
    print(f"{Colors.BOLD}3. Update React Native App:{Colors.ENDC}")
    print("   - Install expo-secure-store: expo install expo-secure-store")
    print("   - Configure axios with JWT interceptor")
    print("   - Implement OTP login screen")
    print("   - See JWT_IMPLEMENTATION_GUIDE.md for complete examples")
    print()
    
    print(f"{Colors.BOLD}4. Security Checklist:{Colors.ENDC}")
    print("   - Change SECRET_KEY to a strong random value")
    print("   - Remove OTP from send_otp response (production)")
    print("   - Integrate real SMS service")
    print("   - Enable HTTPS in production")
    print("   - Add rate limiting for OTP requests")
    print()
    
    print(f"{Colors.BOLD}5. Documentation:{Colors.ENDC}")
    print("   - Read: JWT_IMPLEMENTATION_GUIDE.md")
    print("   - Read: AUTH_README.md")
    print("   - Run: python route_protection_guide.py")
    print()

def main():
    """Main setup function"""
    print_header("JWT Authentication Setup for Goa Police Patrolling App")
    
    # Step 1: Check environment
    if not check_environment():
        print_error("\nSetup aborted due to missing environment variables")
        sys.exit(1)
    
    # Step 2: Test database connection
    if not test_database_connection():
        print_error("\nSetup aborted due to database connection failure")
        sys.exit(1)
    
    # Step 3: Check tables
    tables_ok, table_name = check_tables_exist()
    if not tables_ok:
        print_error("\nSetup aborted due to missing tables")
        sys.exit(1)
    
    # Step 4: Run migration
    print_info(f"\nUsing table name: '{table_name}' for officers")
    if not run_migration():
        print_error("\nMigration failed, but you can continue manually")
    
    # Step 5: Verify setup
    if not verify_setup():
        print_warning("\nSome files are missing, but setup can continue")
    
    # Step 6: Add test data
    add_test_data()
    
    # Print next steps
    print_next_steps()
    
    print_success("\n🎉 JWT Authentication setup completed!")
    print_info("Start your server with: python run.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_error("\n\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
