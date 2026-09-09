import ipaddress
import socket
from urllib.parse import urlparse

from pydantic import BaseModel, field_validator

MAX_URL_LENGTH = 2048
BLOCKED_HOSTNAMES = {"localhost"}


def _is_private_host(hostname: str) -> bool:
    """Return True if a hostname resolves to a loopback, private, or link-local address."""
    try:
        ip = ipaddress.ip_address(hostname)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        pass
    try:
        resolved = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(resolved)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except (socket.gaierror, ValueError):
        return False


class CreateLinkRequest(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if len(v) > MAX_URL_LENGTH:
            raise ValueError(f"URL must be {MAX_URL_LENGTH} characters or fewer")
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValueError("URL must start with http:// or https://")
        hostname = (parsed.hostname or "").lower()
        if hostname in BLOCKED_HOSTNAMES or _is_private_host(hostname):
            raise ValueError("URLs pointing to local or private network addresses are not allowed")
        return v


class LinkResponse(BaseModel):
    name: str
    url: str


class LinkDetailResponse(BaseModel):
    name: str
    url: str
    created_at: str
