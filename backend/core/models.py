from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="analyst")

    uploaded_logs = relationship("LogEntry", back_populates="uploader")

class LogEntry(Base):
    __tablename__ = "log_entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    ip_address: Mapped[str] = mapped_column(String(50), index=True)
    status_code: Mapped[int] = mapped_column(Integer, index=True)
    endpoint: Mapped[str] = mapped_column(String(255))
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)

    uploaded_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    uploader = relationship("User", back_populates="uploaded_logs")
