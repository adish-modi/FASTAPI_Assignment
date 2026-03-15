"""
FastAPI Address Book Application

This module contains the main FastAPI application with all API endpoints
for managing addresses in an address book.
"""

import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db, init_db
from schemas import AddressCreate, AddressUpdate, AddressResponse, AddressSearch
from crud import (
    create_address,
    get_address,
    get_all_addresses,
    update_address,
    delete_address,
    get_addresses_within_distance
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with coordinates",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"message": "Address Book API is running"}


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Address Book API is running"}


@app.post(
    "/addresses",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Addresses"]
)
async def create_address_endpoint(
    address: AddressCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new address in the address book.
    
    - **name**: Name or label for the address
    - **street**: Street address
    - **city**: City name
    - **state**: State or province
    - **zip_code**: ZIP or postal code
    - **country**: Country name
    - **latitude**: Latitude coordinate (must be between -90 and 90)
    - **longitude**: Longitude coordinate (must be between -180 and 180)
    """
    try:
        logger.info(f"Creating new address: {address.name}")
        db_address = create_address(db=db, address=address)
        logger.info(f"Address created successfully with ID: {db_address.id}")
        return db_address
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create address"
        )


@app.get(
    "/addresses",
    response_model=List[AddressResponse],
    tags=["Addresses"]
)
async def get_addresses_endpoint(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all addresses from the address book.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    try:
        logger.info(f"Retrieving addresses (skip={skip}, limit={limit})")
        addresses = get_all_addresses(db=db, skip=skip, limit=limit)
        logger.info(f"Retrieved {len(addresses)} addresses")
        return addresses
    except Exception as e:
        logger.error(f"Error retrieving addresses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve addresses"
        )


@app.get(
    "/addresses/{address_id}",
    response_model=AddressResponse,
    tags=["Addresses"]
)
async def get_address_endpoint(
    address_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific address by ID.
    
    - **address_id**: The unique identifier of the address
    """
    try:
        logger.info(f"Retrieving address with ID: {address_id}")
        address = get_address(db=db, address_id=address_id)
        if address is None:
            logger.warning(f"Address with ID {address_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with ID {address_id} not found"
            )
        return address
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve address"
        )


@app.put(
    "/addresses/{address_id}",
    response_model=AddressResponse,
    tags=["Addresses"]
)
async def update_address_endpoint(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing address.
    
    - **address_id**: The unique identifier of the address to update
    - All fields in the request body are optional (only provided fields will be updated)
    """
    try:
        logger.info(f"Updating address with ID: {address_id}")
        db_address = update_address(db=db, address_id=address_id, address=address)
        if db_address is None:
            logger.warning(f"Address with ID {address_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with ID {address_id} not found"
            )
        logger.info(f"Address with ID {address_id} updated successfully")
        return db_address
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update address"
        )


@app.delete(
    "/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Addresses"]
)
async def delete_address_endpoint(
    address_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an address from the address book.
    
    - **address_id**: The unique identifier of the address to delete
    """
    try:
        logger.info(f"Deleting address with ID: {address_id}")
        success = delete_address(db=db, address_id=address_id)
        if not success:
            logger.warning(f"Address with ID {address_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Address with ID {address_id} not found"
            )
        logger.info(f"Address with ID {address_id} deleted successfully")
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting address: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete address"
        )


@app.post(
    "/addresses/search",
    response_model=List[AddressResponse],
    tags=["Addresses"]
)
async def search_addresses_within_distance(
    search: AddressSearch,
    db: Session = Depends(get_db)
):
    """
    Find all addresses within a specified distance from given coordinates.
    
    - **latitude**: Latitude of the center point (must be between -90 and 90)
    - **longitude**: Longitude of the center point (must be between -180 and 180)
    - **distance_km**: Maximum distance in kilometers from the center point
    """
    try:
        logger.info(
            f"Searching addresses within {search.distance_km}km of "
            f"({search.latitude}, {search.longitude})"
        )
        addresses = get_addresses_within_distance(
            db=db,
            latitude=search.latitude,
            longitude=search.longitude,
            distance_km=search.distance_km
        )
        logger.info(f"Found {len(addresses)} addresses within distance")
        return addresses
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error searching addresses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search addresses"
        )
