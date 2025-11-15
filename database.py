from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    major = Column(String, nullable=False)

engine = create_engine("sqlite:///students.db")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
