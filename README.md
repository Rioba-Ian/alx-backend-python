# ALX Backend Python - Database Project

This project sets up a MySQL database with Docker Compose and provides a Python script to seed the database with user data from a CSV file.

## Project Structure

```
alx-backend-python/
├── docker-compose.yml          # Docker Compose configuration for MySQL
├── init.sql                    # SQL initialization script
├── requirements.txt            # Python dependencies
├── user_data.csv              # CSV file with user data
├── python-generators-0x00/
│   └── seed.py                # Python script for seeding database
└── README.md                  # This file
```

## Database Schema

The project creates a MySQL database named `ALX_prodev` with the following table:

### user_data Table

- **user_id**: CHAR(36) PRIMARY KEY (UUID, Indexed)
- **name**: VARCHAR(255) NOT NULL
- **email**: VARCHAR(255) NOT NULL (Indexed for faster lookups)
- **age**: DECIMAL(3,0) NOT NULL

## Prerequisites

- Docker and Docker Compose
- Python 3.7+
- pip (Python package manager)

## Setup Instructions

### 1. Clone/Navigate to Project Directory

```bash
cd alx-backend-python
```

### 2. Start MySQL Database with Docker Compose

```bash
docker-compose up -d
```

This will:

- Start a MySQL 8.0 container
- Create the `ALX_prodev` database
- Create the `user_data` table
- Set up proper indexing

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Database is Running

```bash
docker-compose ps
```

You should see the MySQL container running and healthy.

### 5. Run the Database Seeding Script

```bash
cd python-generators-0x00
python3 seed.py
```

## Database Connection Details

- **Host**: localhost
- **Port**: 3306
- **Database**: ALX_prodev
- **Username**: alx_user
- **Password**: alx_password
- **Root Password**: root_password

## Features

### Docker Compose Configuration

- MySQL 8.0 with persistent data storage
- Health checks for database readiness
- Automatic database and table creation
- Custom user and database setup

### Python Seeding Script

- **Duplicate Prevention**: Checks for existing emails before insertion
- **UUID Generation**: Automatically generates unique UUIDs for user_id
- **Data Validation**: Validates age ranges and required fields
- **Progress Tracking**: Shows progress during bulk insertion
- **Error Handling**: Graceful handling of connection and data errors
- **Transaction Management**: Uses transactions for data integrity

## Usage Examples

### Start the Database

```bash
docker-compose up -d
```

### Seed the Database

```bash
cd python-generators-0x00
python3 seed.py
```

### Connect to Database (using MySQL client)

```bash
mysql -h localhost -u alx_user -p ALX_prodev
# Password: alx_password
```

### View Data

```sql
USE ALX_prodev;
SELECT COUNT(*) FROM user_data;
SELECT * FROM user_data LIMIT 10;
```

### Stop the Database

```bash
docker-compose down
```

### Stop and Remove All Data

```bash
docker-compose down -v
```

## Script Output

The seeding script provides detailed feedback:

```
🌱 Starting database seeding process...
==================================================
✓ Successfully read 1000 valid records from CSV
✓ Successfully connected to MySQL database: ALX_prodev
✓ Table 'user_data' verified/created successfully
📊 Initial record count: 0
🔄 Inserting 1000 records...
✓ Processed 50 records...
✓ Processed 100 records...
...
✓ Transaction committed successfully

==================================================
📊 SEEDING SUMMARY
==================================================
📥 Records from CSV: 1000
✅ Records inserted: 1000
⏭️  Records skipped: 0
📊 Initial DB count: 0
📊 Final DB count: 1000
📈 Net increase: 1000
✅ Database seeding completed successfully!
```

## Data Validation

The script includes several validation checks:

- **Email Uniqueness**: Prevents duplicate email entries
- **Age Range**: Validates age is between 0 and 150
- **Required Fields**: Ensures name and email are not empty
- **Data Types**: Validates age is a valid integer

## Troubleshooting

### Database Connection Issues

1. Ensure Docker is running: `docker ps`
2. Check if MySQL container is healthy: `docker-compose ps`
3. Wait for database to be fully initialized (may take 30-60 seconds)

### Permission Issues

```bash
# If you get permission denied errors
sudo docker-compose up -d
```

### Reset Database

```bash
# Remove all data and start fresh
docker-compose down -v
docker-compose up -d
```

### View Logs

```bash
# Check MySQL logs
docker-compose logs mysql

# Follow logs in real-time
docker-compose logs -f mysql
```

## Development

### Modify Database Schema

Edit `init.sql` file and restart containers:

```bash
docker-compose down -v
docker-compose up -d
```

### Modify Seeding Logic

Edit `python-generators-0x00/seed.py` and run:

```bash
python3 seed.py
```

### Add New Dependencies

Add to `requirements.txt` and install:

```bash
pip install -r requirements.txt
```

## Security Notes

- The database credentials are for development only
- In production, use environment variables for sensitive data
- Consider using Docker secrets for password management
- The database is exposed on localhost:3306 for development convenience

## License

This project is part of the ALX Backend Python curriculum.
