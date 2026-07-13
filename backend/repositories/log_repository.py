from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

import core.models as models


class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def bulk_create(self, logs: list[models.LogEntry]) -> int:
        self.db.bulk_save_objects(logs)
        self.db.commit()
        return len(logs)

    def list_logs(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        endpoints: Optional[List[str]] = None,
        status_code: Optional[int] = None,
    ):
        query = self.db.query(models.LogEntry).filter(models.LogEntry.uploaded_by_id == user_id)

        if start_date:
            query = query.filter(models.LogEntry.timestamp >= start_date)

        if end_date:
            query = query.filter(models.LogEntry.timestamp <= end_date)

        if endpoints:
            query = query.filter(models.LogEntry.endpoint.in_(endpoints))

        if status_code:
            query = query.filter(models.LogEntry.status_code == status_code)

        offset = (page - 1) * limit
        return query.offset(offset).limit(limit).all()

    def list_unique_endpoints(self, user_id: int) -> list[str]:
        endpoints = (
            self.db.query(models.LogEntry.endpoint)
            .filter(models.LogEntry.uploaded_by_id == user_id)
            .distinct()
            .all()
        )
        return [endpoint[0] for endpoint in endpoints]
