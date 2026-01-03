from sqlalchemy.orm import Session
from .models import MessageReference
from .schemas import MessageReferenceCreate


def create_message_reference(db: Session, ref: MessageReferenceCreate):
    db_ref = MessageReference(**ref.model_dump())
    db.add(db_ref)
    db.commit()
    db.refresh(db_ref)
    return db_ref


def get_message_references(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MessageReference).offset(skip).limit(limit).all()


def get_message_reference(db: Session, reference_id: int):
    return db.query(MessageReference).filter(MessageReference.id == reference_id).first()
