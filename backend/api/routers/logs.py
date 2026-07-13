from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

import core.models as models
from core.dependencies import get_current_user, get_db
from core import schemas
from repositories.log_repository import LogRepository
from services.log_service import LogService

router = APIRouter(tags=["logs"])


@router.post("/upload-logs")
async def upload_logs(
    file: UploadFile = File(...),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = LogService(LogRepository(db))
    return await service.upload_logs(file, user)


@router.get("/logs", response_model=list[schemas.LogEntryResponse])
def get_logs(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    endpoints: Optional[List[str]] = Query(default=None),
    status_code: Optional[int] = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = LogService(LogRepository(db))
    return service.get_logs(
        user_id=user.id,
        page=page,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        endpoints=endpoints,
        status_code=status_code,
    )


@router.get("/endpoints", response_model=List[str])
def get_unique_endpoints(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = LogService(LogRepository(db))
    return service.get_unique_endpoints(user.id)
