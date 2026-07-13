import io
from datetime import datetime
from typing import List, Optional

import pandas as pd
from fastapi import HTTPException, status

import core.models as models
from repositories.log_repository import LogRepository


class LogService:
    def __init__(self, log_repository: LogRepository):
        self.log_repository = log_repository

    async def upload_logs(self, file, user: models.User):
        filename = file.filename or ""
        if not filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas arquivos .csv são permitidos.",
            )

        try:
            content = await file.read()
            df = pd.read_csv(io.BytesIO(content))
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.drop_duplicates()

            logs = []
            for _, row in df.iterrows():
                logs.append(
                    models.LogEntry(
                        timestamp=row["timestamp"],
                        ip_address=row["ip_address"],
                        status_code=row["status_code"],
                        endpoint=row["endpoint"],
                        user_agent=row.get("user_agent", None),
                        uploaded_by_id=user.id,
                    )
                )

            created_count = self.log_repository.bulk_create(logs)
            return {"message": f"{created_count} registros de log foram carregados com sucesso."}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar o arquivo: {str(exc)}",
            ) from exc

    def get_logs(
        self,
        user_id: int,
        page: int = 1,
        limit: int = 20,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        endpoints: Optional[List[str]] = None,
        status_code: Optional[int] = None,
    ):
        return self.log_repository.list_logs(
            user_id=user_id,
            page=page,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            endpoints=endpoints,
            status_code=status_code,
        )

    def get_unique_endpoints(self, user_id: int) -> list[str]:
        return self.log_repository.list_unique_endpoints(user_id)
