from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

import db

router = APIRouter(tags=["redirect"])


@router.get("/{name}")
def redirect(name: str):
    row = db.get_by_code(name)
    if not row:
        raise HTTPException(status_code=404, detail=f"No link found for name '{name}'")
    return RedirectResponse(url=row["original_url"], status_code=307)
