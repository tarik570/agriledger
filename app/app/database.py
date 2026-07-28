from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# رابط الاتصال بقاعدة البيانات (سنقوم بربطه لاحقاً عند الاستضافة)
SQLALCHEMY_DATABASE_URL = "sqlite:///./agriledger.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# دالة للحصول على الاتصال بقاعدة البيانات عند الحاجة
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
