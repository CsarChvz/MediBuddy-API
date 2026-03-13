from core.database import Base
from sqlalchemy import Column, Integer


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
