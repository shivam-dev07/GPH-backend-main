"""
JWT Authentication Verification Script
Verifies that all JWT authentication files are in place
"""

import os

def check_file_exists(filepath, description):
    """Check if a file exists and print status"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def main():
    print("\n" + "="*80)
    print("JWT AUTHENTICATION SETUP VERIFICATION")
    print("="*80 + "\n")
    
    all_good = True
    
    print("📁 Configuration Files:")
    all_good &= check_file_exists("config.py", "Configuration module")
    all_good &= check_file_exists(".env", "Environment variables")
    print()
    
    print("🔐 Authentication Files:")
    all_good &= check_file_exists("utils/decorators.py", "JWT decorator")
    all_good &= check_file_exists("models/auth_model.py", "Auth model")
    all_good &= check_file_exists("controllers/auth_controller.py", "Auth controller")
    all_good &= check_file_exists("routes/auth_routes.py", "Auth routes")
    print()
    
    print("🗄️ Database Migration:")
    all_good &= check_file_exists("migration_jwt_auth.sql", "JWT migration SQL")
    print()
    
    print("📚 Documentation:")
    all_good &= check_file_exists("JWT_IMPLEMENTATION_GUIDE.md", "Complete implementation guide")
    all_good &= check_file_exists("JWT_QUICK_REFERENCE.md", "Quick reference card")
    all_good &= check_file_exists("AUTH_README.md", "Auth README")
    print()
    
    print("🛠️ Helper Scripts:")
    all_good &= check_file_exists("setup_jwt_auth.py", "Setup script")
    all_good &= check_file_exists("route_protection_guide.py", "Route protection guide")
    print()
    
    print("📝 Examples:")
    all_good &= check_file_exists("EXAMPLE_duty_routes_with_jwt.py", "Example protected routes")
    print()
    
    print("="*80)
    if all_good:
        print("✓ ALL FILES PRESENT - JWT Authentication is ready!")
        print("\n📋 NEXT STEPS:")
        print("1. Run database migration: See migration_jwt_auth.sql")
        print("2. Update .env with strong SECRET_KEY")
        print("3. Add @jwt_required to protected routes")
        print("4. Test with: python run.py")
        print("5. Read: JWT_IMPLEMENTATION_GUIDE.md")
    else:
        print("✗ SOME FILES MISSING - Please review the setup")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
