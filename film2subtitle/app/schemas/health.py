from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """Response model for health check."""

    status: str = Field(
        default="OK",
        title="Health check status",
        description="Shows whether the service is available or not.",
    )
