from enum import Enum

from pydantic import BaseModel, Field


class HealthStatus(str, Enum):
    """The status of the service."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class HealthCheck(BaseModel):
    """Response model for health check."""

    status: HealthStatus = Field(
        ...,
        title="Health check status",
        description="Shows whether the service is available or not.",
    )
