from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Veritabanı bağlantı dizesi
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/library_db"

# Veritabanı motorunu oluştur
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Temel sınıf
Base = declarative_base()

# Oturum oluşturma fonksiyonu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı oturumu almak için bağımlılık
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
