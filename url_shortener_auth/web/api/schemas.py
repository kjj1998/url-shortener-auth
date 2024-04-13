"""Schemas for the API"""

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for the JWT token response"""

    access_token: str
    token_type: str
