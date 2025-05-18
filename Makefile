
# Install dependencies from requirements.txt
# Assumes pip is available in the current environment/PATH
install:
	@echo "Installing dependencies using pip..."
	pip install -r requirements.txt
	@echo "Dependencies installed."

# Start the database container using docker-compose
db-up:
	@echo "Starting database container..."
	docker-compose up -d db
	@echo "Database container started. Wait a few moments for it to be ready."

# Stop and remove the database container using docker-compose
db-down:
	@echo "Stopping database container..."
	docker-compose down db
	@echo "Database container stopped."

# Run database migrations
# Requires database to be running and dependencies installed (e.g., alembic in PATH)
migrate: install db-up
	@echo "Running database migrations..."
	# Note: Ensure DATABASE_URL env var is correctly set
	alembic upgrade head
	@echo "Migrations applied."

# Run the FastAPI application
# Requires migrations to be applied and dependencies installed (e.g., uvicorn in PATH)
run: migrate install
	@echo "Starting FastAPI application..."
	# Note: Ensure DATABASE_URL env var is correctly set
	uvicorn app.main:app --reload
	@echo "Application stopped."

# Run the test suite
# Requires dependencies installed (e.g., pytest in PATH)
test: install
	@echo "Running tests..."
	pytest
	@echo "Tests finished."

# Clean up cache files
clean:
	@echo "Cleaning up cache files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "Cleanup complete."
