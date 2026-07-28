from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import hashlib
from datetime import datetime

from .database import engine, Base, get_db
from .models import AnimalRecord
from .schemas import AnimalCreate, AnimalResponse

# إنشاء جداول قاعدة البيانات تلقائياً عند تشغيل التطبيق
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgriLedger API",
    description="نظام إدارة وتوثيق الثروة الحيوانية والزراعية بالبلوكشين",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "مرحباً بك في نظام AgriLedger للثروة الحيوانية والزراعية!"}

@app.post("/animals/", response_model=AnimalResponse)
def create_animal(animal: AnimalCreate, db: Session = Depends(get_db)):
    # التحقق مما إذا كان رقم التعريف موجود مسبقاً
    existing = db.query(AnimalRecord).filter(AnimalRecord.tag_number == animal.tag_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="رقم التعريف (Tag Number) موجود مسبقاً في النظام!")

    # إنشاء بصمة مشفرة وهمية لتمثيل توثيق البلوكشين (Blockchain Hash)
    data_string = f"{animal.tag_number}-{animal.species}-{animal.weight}-{datetime.utcnow()}"
    b_hash = hashlib.sha256(data_string.encode()).hexdigest()

    # إنشاء سجلاً جديداً بقاعدة البيانات
    db_animal = AnimalRecord(
        tag_number=animal.tag_number,
        species=animal.species,
        breed=animal.breed,
        weight=animal.weight,
        health_status=animal.health_status,
        blockchain_hash=b_hash
    )
    
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

@app.get("/animals/", response_model=list[AnimalResponse])
def get_animals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    animals = db.query(AnimalRecord).offset(skip).limit(limit).all()
    return animals
