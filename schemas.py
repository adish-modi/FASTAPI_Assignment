"""
Pydantic schemas for request/response validation.

This module defines the data models used for API request validation
and response serialization.
"""

from typing import Optional
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    """Base schema with common address fields."""
    
    name: str = Field(..., min_length=1, max_length=200, description="Name or label for the address")
    street: str = Field(..., min_length=1, max_length=200, description="Street address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: str = Field(..., min_length=1, max_length=100, description="State or province")
    zip_code: str = Field(..., min_length=1, max_length=20, description="ZIP or postal code")
    country: str = Field(..., min_length=1, max_length=100, description="Country name")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")


class AddressCreate(AddressBase):
    """Schema for creating a new address."""
    pass


class AddressUpdate(BaseModel):
    """Schema for updating an existing address (all fields optional)."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    street: Optional[str] = Field(None, min_length=1, max_length=200)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    zip_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class AddressResponse(AddressBase):
    """Schema for address response (includes ID)."""
    
    id: int
    
    class Config:
        """Pydantic configuration."""
        from_attributes = True  # Pydantic v2 uses from_attributes instead of orm_mode


class AddressSearch(BaseModel):
    """Schema for searching addresses within a distance."""
    
    latitude: float = Field(..., ge=-90, le=90, description="Latitude of the center point")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude of the center point")
    distance_km: float = Field(..., gt=0, description="Maximum distance in kilometers")
