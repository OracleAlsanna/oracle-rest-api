from fastapi import APIRouter, HTTPException

import db
import shortener
from models import CreateLinkRequest, LinkResponse, LinkDetailResponse

router = APIRouter(prefix="/links", tags=["links"])


@router.post("", response_model=LinkResponse, status_code=201)
def create_link(body: CreateLinkRequest):
    existing = db.get_by_url(body.url)
    if existing:
        return LinkResponse(name=existing["code"], url=existing["original_url"])

    try:
        code = shortener.generate_code(db.code_exists)
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="All codes are taken. Delete some links to free up codes.",
        )

    row = db.insert(code, body.url)
    if row is None:
        raise HTTPException(status_code=409, detail="Name collision could not be resolved.")

    return LinkResponse(name=row["code"], url=row["original_url"])


@router.get("", response_model=list[LinkDetailResponse])
def list_links():
    rows = db.list_all()
    return [
        LinkDetailResponse(name=r["code"], url=r["original_url"], created_at=r["created_at"])
        for r in rows
    ]


@router.get("/{name}", response_model=LinkDetailResponse)
def get_link(name: str):
    row = db.get_by_code(name)
    if not row:
        raise HTTPException(status_code=404, detail=f"No link found for name '{name}'")
    return LinkDetailResponse(name=row["code"], url=row["original_url"], created_at=row["created_at"])


@router.delete("/{name}", status_code=204)
def delete_link(name: str):
    removed = db.delete(name)
    if not removed:
        raise HTTPException(status_code=404, detail=f"No link found for name '{name}'")
