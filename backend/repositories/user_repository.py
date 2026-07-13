from sqlalchemy.orm import Session

import core.models as models

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def create(self, username: str, password: str, role: str):
        db_user = models.User(username=username, password=password, role=role)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
