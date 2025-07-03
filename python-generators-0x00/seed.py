#!/usr/bin/env python3
"""
Database seeding script for ALX_prodev MySQL database.
This script reads user data from CSV file and populates the user_data table.
"""

import csv
import mysql.connector
from mysql.connector import Error
import uuid
import os
import sys
from typing import List, Tuple, Optional


class DatabaseSeeder:
    """Class to handle database seeding operations."""

    def __init__(self, host: str = 'localhost', port: int = 3306,
                 user: str = 'alx_user', password: str = 'alx_password',
                 database: str = 'ALX_prodev'):
        """
        Initialize database connection parameters.

        Args:
            host: Database host
            port: Database port
            user: Database username
            password: Database password
            database: Database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """
        Establish database connection.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=False
            )
            self.cursor = self.connection.cursor()
            print(f"✓ Successfully connected to MySQL database: {self.database}")
            return True
        except Error as e:
            print(f"✗ Error connecting to MySQL database: {e}")
            return False

    def disconnect(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Database connection closed")

    def create_table_if_not_exists(self) -> bool:
        """
        Create user_data table if it doesn't exist.

        Returns:
            bool: True if table created/exists, False otherwise
        """
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX idx_user_id (user_id),
                INDEX idx_email (email)
            )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("✓ Table 'user_data' verified/created successfully")
            return True
        except Error as e:
            print(f"✗ Error creating table: {e}")
            return False

    def email_exists(self, email: str) -> bool:
        """
        Check if email already exists in database.

        Args:
            email: Email to check

        Returns:
            bool: True if email exists, False otherwise
        """
        try:
            query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
            self.cursor.execute(query, (email,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"✗ Error checking email existence: {e}")
            return False

    def insert_user_data(self, user_data: List[Tuple[str, str, str, int]]) -> Tuple[int, int]:
        """
        Insert user data into database.

        Args:
            user_data: List of tuples containing (user_id, name, email, age)

        Returns:
            Tuple[int, int]: (inserted_count, skipped_count)
        """
        inserted_count = 0
        skipped_count = 0

        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """

        for user_id, name, email, age in user_data:
            try:
                if self.email_exists(email):
                    print(f"⚠ Skipping duplicate email: {email}")
                    skipped_count += 1
                    continue

                self.cursor.execute(insert_query, (user_id, name, email, age))
                inserted_count += 1

                if inserted_count % 50 == 0:
                    print(f"✓ Processed {inserted_count} records...")

            except Error as e:
                print(f"✗ Error inserting user {email}: {e}")
                skipped_count += 1
                continue

        try:
            self.connection.commit()
            print(f"✓ Transaction committed successfully")
        except Error as e:
            print(f"✗ Error committing transaction: {e}")
            self.connection.rollback()

        return inserted_count, skipped_count

    def get_table_count(self) -> int:
        """
        Get total count of records in user_data table.

        Returns:
            int: Number of records in table
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM user_data")
            return self.cursor.fetchone()[0]
        except Error as e:
            print(f"✗ Error getting table count: {e}")
            return 0


def read_csv_data(csv_file_path: str) -> List[Tuple[str, str, str, int]]:
    """
    Read user data from CSV file.

    Args:
        csv_file_path: Path to CSV file

    Returns:
        List of tuples containing (user_id, name, email, age)
    """
    user_data = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                try:
                    # Generate UUID for user_id
                    user_id = str(uuid.uuid4())

                    # Clean and validate data
                    name = row['name'].strip()
                    email = row['email'].strip()
                    age = int(row['age'])

                    # Basic validation
                    if not name or not email or age < 0 or age > 150:
                        print(f"⚠ Invalid data for {email}, skipping...")
                        continue

                    user_data.append((user_id, name, email, age))

                except (ValueError, KeyError) as e:
                    print(f"⚠ Error processing row: {e}")
                    continue

        print(f"✓ Successfully read {len(user_data)} valid records from CSV")
        return user_data

    except FileNotFoundError:
        print(f"✗ CSV file not found: {csv_file_path}")
        return []
    except Exception as e:
        print(f"✗ Error reading CSV file: {e}")
        return []


def main():
    """Main function to execute database seeding."""
    print("🌱 Starting database seeding process...")
    print("=" * 50)

    # Get CSV file path
    csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'user_data.csv')

    if not os.path.exists(csv_file_path):
        print(f"✗ CSV file not found at: {csv_file_path}")
        sys.exit(1)

    # Read CSV data
    user_data = read_csv_data(csv_file_path)

    if not user_data:
        print("✗ No valid user data found in CSV file")
        sys.exit(1)

    # Initialize database seeder
    seeder = DatabaseSeeder()

    try:
        # Connect to database
        if not seeder.connect():
            sys.exit(1)

        # Create table if not exists
        if not seeder.create_table_if_not_exists():
            sys.exit(1)

        # Get initial count
        initial_count = seeder.get_table_count()
        print(f"📊 Initial record count: {initial_count}")

        # Insert user data
        print(f"🔄 Inserting {len(user_data)} records...")
        inserted, skipped = seeder.insert_user_data(user_data)

        # Get final count
        final_count = seeder.get_table_count()

        # Summary
        print("\n" + "=" * 50)
        print("📊 SEEDING SUMMARY")
        print("=" * 50)
        print(f"📥 Records from CSV: {len(user_data)}")
        print(f"✅ Records inserted: {inserted}")
        print(f"⏭️  Records skipped: {skipped}")
        print(f"📊 Initial DB count: {initial_count}")
        print(f"📊 Final DB count: {final_count}")
        print(f"📈 Net increase: {final_count - initial_count}")

        if inserted > 0:
            print("✅ Database seeding completed successfully!")
        else:
            print("ℹ️  No new records were inserted")

    except KeyboardInterrupt:
        print("\n⚠️  Seeding process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)
    finally:
        seeder.disconnect()


if __name__ == "__main__":
    main()
