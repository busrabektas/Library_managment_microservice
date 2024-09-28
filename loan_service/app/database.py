from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Veritabanı bağlantı dizesi
SQLALCHEMY_DATABASE_URL ="mysql+pymysql://root:@mysql:3306/library_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()




def get_db():
    db=  SessionLocal()
    try:
        yield db
    finally:
        db.close()
