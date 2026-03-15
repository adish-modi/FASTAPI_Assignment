"""
SQLAlchemy database models.

This module defines the database schema using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Float
from database import Base


class Address(Base):
    """
    Address model representing an address entry in the database.
    
    Attributes:
        id: Primary key, auto-incrementing integer
        name: Name or label for the address
        street: Street address
        city: City name
        state: State or province
        zip_code: ZIP or postal code
        country: Country name
        latitude: Latitude coordinate (-90 to 90)
        longitude: Longitude coordinate (-180 to 180)
    """
    
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    def __repr__(self):
        """String representation of the Address model."""
        return (
            f"<Address(id={self.id}, name='{self.name}', "
            f"city='{self.city}', lat={self.latitude}, lon={self.longitude})>"
        )
