from src.schemas import BaseSchema


class HealthCheckSchema(BaseSchema):
    message: str
