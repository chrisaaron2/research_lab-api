from pydantic import BaseModel


class SeedResponse(BaseModel):
    message: str
    inserted: bool
