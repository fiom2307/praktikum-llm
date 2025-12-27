from sqlalchemy import Column, Integer, Boolean
from database import Base

class FormSettings(Base):
    __tablename__ = "form_settings"

    id = Column(Integer, primary_key=True)
    pretest_enabled = Column(Boolean, nullable=False, default=False)
    posttest_enabled = Column(Boolean, nullable=False, default=False)