import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from src.database.session import Base, load_vec_extension


@pytest.fixture
def rds_session():
    """테스트용 메모리 RDS (SQLite) 세션"""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def vector_session():
    """테스트용 메모리 Vector DB 세션"""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    event.listen(engine, "connect", load_vec_extension)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
