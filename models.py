from urllib.parse import urlparse

from pydantic import BaseModel, field_validator


class CreateLinkRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("URL must start with http:// or https://")
        return v


class LinkResponse(BaseModel):
    name: str
    url: str


class LinkDetailResponse(BaseModel):
    name: str
    url: str
    created_at: str
