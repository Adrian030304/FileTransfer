from typing import Optional
import sqlalchemy as sql
import sqlalchemy.orm as orm
from datetime import datetime

from app import db

class FileUploads(db.Model):
    __tablename__ = "file_uploads"
    id: orm.Mapped[str] = orm.mapped_column(sql.String(36), primary_key=True)
    file_name: orm.Mapped[str] = orm.mapped_column(sql.String(255), index=True)
    expiration_date: orm.Mapped[Optional[datetime]] = orm.mapped_column(sql.DateTime)