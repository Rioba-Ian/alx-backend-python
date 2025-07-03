# ALX Backend Python - Database Project Makefile

.PHONY: help setup start stop restart clean seed test logs shell status install

# Default target
help:
	@echo "🚀 ALX Backend Python - Database Project"
	@echo "========================================"
	@echo ""
	@echo "Available commands:"
	@echo "  setup     - Initial project setup (install dependencies)"
	@echo "  start     - Start MySQL database with Docker Compose"
	@echo "  stop      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  clean     - Stop services and remove volumes (⚠️  removes all data)"
	@echo "  seed      - Run database seeding script"
	@echo "  test      - Test database connection"
	@echo "  logs      - View MySQL container logs"
	@echo "  shell     - Open MySQL shell"
	@echo "  status    - Check service status"
	@echo "  install   - Install Python dependencies"
	@echo ""
	@echo "Quick start:"
	@echo "  make setup && make start && make seed"

# Initial project setup
setup: install start
	@echo "✅ Project setup complete!"
	@echo "💡 Run 'make seed' to populate the database with sample data"

# Install Python dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Start services
start:
	@echo "🚀 Starting MySQL database..."
	docker-compose up -d
	@echo "⏳ Waiting for database to be ready..."
	@sleep 10
	@echo "✅ Database started successfully"

# Stop services
stop:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped"

# Restart services
restart: stop start
	@echo "✅ Services restarted"

# Clean up (removes all data)
clean:
	@echo "🧹 Cleaning up (this will remove all data)..."
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete"

# Run database seeding
seed:
	@echo "🌱 Seeding database..."
	cd python-generators-0x00 && python3 seed.py
	@echo "✅ Database seeding complete"

# Test database connection
test:
	@echo "🧪 Testing database connection..."
	python3 test_connection.py

# View logs
logs:
	@echo "📋 MySQL container logs:"
	docker-compose logs mysql

# Follow logs in real-time
logs-follow:
	@echo "📋 Following MySQL logs (Ctrl+C to exit):"
	docker-compose logs -f mysql

# Open MySQL shell
shell:
	@echo "🐚 Opening MySQL shell..."
	@echo "💡 Use password: alx_password"
	docker-compose exec mysql mysql -u alx_user -p ALX_prodev

# Open MySQL root shell
shell-root:
	@echo "🐚 Opening MySQL root shell..."
	@echo "💡 Use password: root_password"
	docker-compose exec mysql mysql -u root -p

# Check service status
status:
	@echo "📊 Service status:"
	docker-compose ps

# Show database info
info:
	@echo "📊 Database information:"
	@echo "  Host: localhost"
	@echo "  Port: 3306"
	@echo "  Database: ALX_prodev"
	@echo "  Username: alx_user"
	@echo "  Password: alx_password"
	@echo ""
	@echo "🐚 Quick connect command:"
	@echo "  mysql -h localhost -u alx_user -p ALX_prodev"

# Backup database
backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker-compose exec mysql mysqldump -u alx_user -palx_password ALX_prodev > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

# Reset database (clean + setup)
reset: clean setup
	@echo "🔄 Database reset complete"

# Development mode (start with logs)
dev:
	@echo "🔧 Starting in development mode..."
	docker-compose up

# Production mode (start detached)
prod: start
	@echo "🏭 Started in production mode"

# Health check
health:
	@echo "🏥 Checking service health..."
	@docker-compose ps | grep healthy && echo "✅ Services are healthy" || echo "❌ Services are not healthy"

# Quick setup for new developers
onboard:
	@echo "👋 Welcome to ALX Backend Python!"
	@echo "🚀 Setting up your development environment..."
	@make setup
	@echo ""
	@echo "🎉 Setup complete! Here's what you can do:"
	@echo "  • View data: make shell"
	@echo "  • Check status: make status"
	@echo "  • View logs: make logs"
	@echo "  • Reset everything: make reset"
	@echo ""
	@echo "📚 For more commands, run: make help"
