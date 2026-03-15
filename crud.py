"""
CRUD operations for addresses.

This module contains all database operations for managing addresses,
including distance calculations using the Haversine formula.
"""

import logging
import math
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import Address
from schemas import AddressCreate, AddressUpdate

# Configure logging
logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth
    using the Haversine formula.
    
    Args:
        lat1: Latitude of first point in degrees
        lon1: Longitude of first point in degrees
        lat2: Latitude of second point in degrees
        lon2: Longitude of second point in degrees
    
    Returns:
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = (
        math.sin(dlat / 2) ** 2 +
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address in the database.
    
    Args:
        db: Database session
        address: Address data to create
    
    Returns:
        Created Address object
    
    Raises:
        ValueError: If coordinates are invalid
    """
    # Validate coordinates
    if not (-90 <= address.latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= address.longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    
    db_address = Address(
        name=address.name,
        street=address.street,
        city=address.city,
        state=address.state,
        zip_code=address.zip_code,
        country=address.country,
        latitude=address.latitude,
        longitude=address.longitude
    )
    
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    
    logger.info(f"Created address with ID {db_address.id}")
    return db_address


def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Retrieve an address by ID.
    
    Args:
        db: Database session
        address_id: ID of the address to retrieve
    
    Returns:
        Address object if found, None otherwise
    """
    return db.query(Address).filter(Address.id == address_id).first()


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """
    Retrieve all addresses with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
    
    Returns:
        List of Address objects
    """
    return db.query(Address).offset(skip).limit(limit).all()


def update_address(
    db: Session,
    address_id: int,
    address: AddressUpdate
) -> Optional[Address]:
    """
    Update an existing address.
    
    Args:
        db: Database session
        address_id: ID of the address to update
        address: Address data to update (only provided fields will be updated)
    
    Returns:
        Updated Address object if found, None otherwise
    
    Raises:
        ValueError: If coordinates are invalid
    """
    db_address = db.query(Address).filter(Address.id == address_id).first()
    
    if db_address is None:
        return None
    
    # Update only provided fields
    update_data = address.model_dump(exclude_unset=True)
    
    # Validate coordinates if provided
    if 'latitude' in update_data:
        if not (-90 <= update_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
    if 'longitude' in update_data:
        if not (-180 <= update_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180")
    
    for field, value in update_data.items():
        setattr(db_address, field, value)
    
    db.commit()
    db.refresh(db_address)
    
    logger.info(f"Updated address with ID {address_id}")
    return db_address


def delete_address(db: Session, address_id: int) -> bool:
    """
    Delete an address from the database.
    
    Args:
        db: Database session
        address_id: ID of the address to delete
    
    Returns:
        True if address was deleted, False if not found
    """
    db_address = db.query(Address).filter(Address.id == address_id).first()
    
    if db_address is None:
        return False
    
    db.delete(db_address)
    db.commit()
    
    logger.info(f"Deleted address with ID {address_id}")
    return True


def get_addresses_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float
) -> List[Address]:
    """
    Find all addresses within a specified distance from given coordinates.
    
    This function uses the Haversine formula to calculate distances.
    For better performance with large datasets, consider using spatial
    database extensions or indexing.
    
    Args:
        db: Database session
        latitude: Latitude of the center point
        longitude: Longitude of the center point
        distance_km: Maximum distance in kilometers
    
    Returns:
        List of Address objects within the specified distance
    
    Raises:
        ValueError: If coordinates are invalid
    """
    # Validate coordinates
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180")
    if distance_km <= 0:
        raise ValueError("Distance must be greater than 0")
    
    # Get all addresses (for small datasets this is fine)
    # For larger datasets, consider using spatial indexing or database extensions
    all_addresses = db.query(Address).all()
    
    # Filter addresses within distance
    addresses_within_distance = []
    for addr in all_addresses:
        distance = haversine_distance(
            latitude, longitude,
            addr.latitude, addr.longitude
        )
        if distance <= distance_km:
            addresses_within_distance.append(addr)
    
    logger.info(
        f"Found {len(addresses_within_distance)} addresses within "
        f"{distance_km}km of ({latitude}, {longitude})"
    )
    
    return addresses_within_distance
