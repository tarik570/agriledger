from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class AnimalRecord(Base):
    __tablename__ = "animal_records"

    id = Column(Integer, primary_key=True, index=True)
    tag_number = Column(String, unique=True, index=True)  # رقم التعريف الخاص بالحيوان
    species = Column(String)                               # النوع (مثل: أغنام، أبقار)
    breed = Column(String)                                 # السلالة
    weight = Column(Float)                                 # الوزن الحالي
    health_status = Column(String)                         # الحالة الصحية
    blockchain_hash = Column(String, nullable=True)        # بصمة التوثيق على البلوكشين
    created_at = Column(DateTime, default=datetime.utcnow) # تاريخ التسجيل
