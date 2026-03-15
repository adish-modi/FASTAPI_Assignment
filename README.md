# Address Book API

A RESTful API application built with FastAPI for managing addresses with geographic coordinates. The application allows users to create, read, update, and delete addresses, as well as search for addresses within a specified distance from given coordinates.

## Features

- **CRUD Operations**: Create, read, update, and delete addresses
- **Coordinate Validation**: Ensures latitude (-90 to 90) and longitude (-180 to 180) are valid
- **Distance Search**: Find all addresses within a specified distance (in kilometers) from given coordinates
- **SQLite Database**: Persistent storage using SQLite
- **Automatic API Documentation**: Interactive Swagger UI and ReDoc documentation
- **Comprehensive Logging**: Logging for all operations and errors
- **Input Validation**: Pydantic models ensure data integrity

## Project Structure

```
personal_project/
├── main.py              # FastAPI application and endpoints
├── database.py          # Database configuration and setup
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── crud.py              # Database CRUD operations
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone or download the repository**

2. **Create a virtual environment (recommended)**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

   The `--reload` flag enables auto-reload on code changes (useful for development).

2. **Access the API**:
   - API Base URL: http://localhost:8000
   - Interactive API Documentation (Swagger UI): http://localhost:8000/docs
   - Alternative API Documentation (ReDoc): http://localhost:8000/redoc

## API Endpoints

### Health Check
- **GET** `/` - Check if the API is running

### Address Management

- **POST** `/addresses` - Create a new address
- **GET** `/addresses` - Get all addresses (with pagination)
- **GET** `/addresses/{address_id}` - Get a specific address by ID
- **PUT** `/addresses/{address_id}` - Update an existing address
- **DELETE** `/addresses/{address_id}` - Delete an address
- **POST** `/addresses/search` - Find addresses within a distance from coordinates

## Example Usage

### Create an Address

```bash
curl -X POST "http://localhost:8000/addresses" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home",
    "street": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "country": "USA",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

### Get All Addresses

```bash
curl -X GET "http://localhost:8000/addresses"
```

### Get Address by ID

```bash
curl -X GET "http://localhost:8000/addresses/1"
```

### Update an Address

```bash
curl -X PUT "http://localhost:8000/addresses/1" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Brooklyn",
    "latitude": 40.6782,
    "longitude": -73.9442
  }'
```

### Delete an Address

```bash
curl -X DELETE "http://localhost:8000/addresses/1"
```

### Search Addresses Within Distance

```bash
curl -X POST "http://localhost:8000/addresses/search" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "distance_km": 10.0
  }'
```

## Database

The application uses SQLite and automatically creates a database file named `address_book.db` in the project directory when first run. The database schema includes:

- **id**: Primary key (auto-incrementing)
- **name**: Address name/label
- **street**: Street address
- **city**: City name
- **state**: State/province
- **zip_code**: ZIP/postal code
- **country**: Country name
- **latitude**: Latitude coordinate (-90 to 90)
- **longitude**: Longitude coordinate (-180 to 180)

## Distance Calculation

The application uses the Haversine formula to calculate the great-circle distance between two points on Earth. This provides accurate distance calculations for addresses anywhere on the globe.

## Validation

All input data is validated using Pydantic models:
- Coordinates must be within valid ranges (latitude: -90 to 90, longitude: -180 to 180)
- String fields have minimum and maximum length constraints
- Distance must be greater than 0

## Logging

The application logs all operations, including:
- Database initialization
- CRUD operations
- Errors and exceptions
- Search queries

Logs are output to the console with timestamps and log levels.

## Best Practices Implemented

- **Separation of Concerns**: Models, schemas, CRUD operations, and API endpoints are separated
- **Type Hints**: Full type annotations throughout the codebase
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Documentation**: Docstrings for all functions and classes
- **Logging**: Structured logging for debugging and monitoring
- **Validation**: Input validation using Pydantic
- **Database Abstraction**: SQLAlchemy ORM for database operations
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Testing the API

You can test the API using:
1. **Swagger UI**: Visit http://localhost:8000/docs for an interactive interface
2. **curl**: Use the examples above
3. **Postman**: Import the OpenAPI schema from http://localhost:8000/openapi.json
4. **Python requests**: Use the `requests` library in Python scripts

## Notes

- The database file (`address_book.db`) will be created automatically on first run
- For production use, consider using PostgreSQL or another production-grade database
- For large datasets, consider implementing spatial indexing for better search performance
- The `--reload` flag is for development only; remove it for production

## License

This project is provided as-is for demonstration purposes.
