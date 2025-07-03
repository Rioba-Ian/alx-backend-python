#!/usr/bin/env python3
"""
Database connection test script for ALX_prodev MySQL database.
This script tests the database connection and displays basic information.
"""

import mysql.connector
from mysql.connector import Error
import sys


def test_database_connection():
    """Test database connection and display basic information."""

    # Database configuration
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'alx_user',
        'password': 'alx_password',
        'database': 'ALX_prodev'
    }

    connection = None
    cursor = None

    try:
        print("🔍 Testing database connection...")
        print("=" * 50)

        # Establish connection
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("✅ Database connection successful!")
        print(f"📊 Connected to: {config['host']}:{config['port']}")
        print(f"🗄️  Database: {config['database']}")
        print(f"👤 User: {config['user']}")

        # Test database version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"🔢 MySQL Version: {version}")

        # Test if table exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'user_data'
        """, (config['database'],))

        table_exists = cursor.fetchone()[0] > 0
        print(f"📋 Table 'user_data' exists: {'✅ Yes' if table_exists else '❌ No'}")

        if table_exists:
            # Get table structure
            cursor.execute("DESCRIBE user_data")
            columns = cursor.fetchall()
            print("\n📊 Table Structure:")
            print("-" * 50)
            for column in columns:
                print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]}")

            # Get record count
            cursor.execute("SELECT COUNT(*) FROM user_data")
            count = cursor.fetchone()[0]
            print(f"\n📈 Total records: {count}")

            if count > 0:
                # Show sample data
                cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT 5")
                sample_data = cursor.fetchall()
                print("\n📋 Sample Data (first 5 records):")
                print("-" * 70)
                for row in sample_data:
                    print(f"  ID: {row[0][:8]}... | Name: {row[1][:20]} | Email: {row[2][:30]} | Age: {row[3]}")

        print("\n" + "=" * 50)
        print("✅ Connection test completed successfully!")

    except Error as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("  1. Make sure Docker container is running: docker-compose ps")
        print("  2. Check if MySQL is ready: docker-compose logs mysql")
        print("  3. Wait a moment for database to initialize")
        print("  4. Verify credentials in docker-compose.yml")
        return False

    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False

    finally:
        # Clean up connections
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("🔌 Database connection closed")

    return True


def main():
    """Main function to run connection test."""
    print("🧪 ALX_prodev Database Connection Test")
    print("=" * 50)

    if test_database_connection():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
